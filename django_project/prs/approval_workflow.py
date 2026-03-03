"""
Payment Approval Workflow
Multi-level approval system for payments
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .models import PR, Payment
import logging

logger = logging.getLogger(__name__)


class ApprovalLevel(models.Model):
    """Define approval levels and thresholds"""
    
    name = models.CharField(max_length=100)
    min_amount = models.FloatField(default=0.0, help_text="Minimum amount requiring this approval")
    max_amount = models.FloatField(null=True, blank=True, help_text="Maximum amount (None for unlimited)")
    order = models.IntegerField(default=1, help_text="Order of approval (1 = first)")
    approvers = models.ManyToManyField(User, related_name='approval_levels')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.name} (${self.min_amount:,.2f} - {f'${self.max_amount:,.2f}' if self.max_amount else 'Unlimited'})"
    
    @classmethod
    def get_required_levels(cls, amount):
        """Get all approval levels required for an amount"""
        levels = cls.objects.filter(
            is_active=True,
            min_amount__lte=amount
        )
        
        if amount:
            levels = levels.filter(
                models.Q(max_amount__gte=amount) | models.Q(max_amount__isnull=True)
            )
        
        return levels.order_by('order')


class PaymentApproval(models.Model):
    """Track payment approval requests"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled')
    )
    
    pr = models.ForeignKey(PR, on_delete=models.CASCADE, related_name='payment_approvals')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True, related_name='approvals')
    
    amount = models.FloatField()
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='payment_requests')
    requested_date = models.DateTimeField(default=timezone.now)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-requested_date']
    
    def __str__(self):
        return f"Payment Approval for {self.pr.pr_number} - ${self.amount:,.2f}"
    
    def get_pending_approvers(self):
        """Get list of users who still need to approve"""
        approved_levels = self.approval_steps.filter(status='approved').values_list('approval_level', flat=True)
        required_levels = ApprovalLevel.get_required_levels(self.amount)
        
        pending_approvers = []
        for level in required_levels:
            if level.id not in approved_levels:
                pending_approvers.extend(level.approvers.all())
        
        return list(set(pending_approvers))
    
    def is_fully_approved(self):
        """Check if all required approvals are complete"""
        required_levels = ApprovalLevel.get_required_levels(self.amount)
        approved_count = self.approval_steps.filter(status='approved').count()
        
        return approved_count >= required_levels.count()
    
    def is_rejected(self):
        """Check if any approval was rejected"""
        return self.approval_steps.filter(status='rejected').exists()
    
    def update_status(self):
        """Update approval status based on approval steps"""
        if self.is_rejected():
            self.status = 'rejected'
        elif self.is_fully_approved():
            self.status = 'approved'
        else:
            self.status = 'pending'
        
        self.save()
        return self.status


class ApprovalStep(models.Model):
    """Individual approval step in the workflow"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    )
    
    payment_approval = models.ForeignKey(PaymentApproval, on_delete=models.CASCADE, related_name='approval_steps')
    approval_level = models.ForeignKey(ApprovalLevel, on_delete=models.CASCADE)
    
    approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approval_steps')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    approved_date = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(blank=True)
    
    class Meta:
        ordering = ['approval_level__order']
        unique_together = ['payment_approval', 'approval_level']
    
    def __str__(self):
        return f"{self.approval_level.name} - {self.status}"
    
    def approve(self, approver, comments=''):
        """Approve this step"""
        self.approver = approver
        self.status = 'approved'
        self.approved_date = timezone.now()
        self.comments = comments
        self.save()
        
        # Update parent approval status
        self.payment_approval.update_status()
        
        logger.info(f"Approval step approved by {approver.username}: {self}")
    
    def reject(self, approver, comments=''):
        """Reject this step"""
        self.approver = approver
        self.status = 'rejected'
        self.approved_date = timezone.now()
        self.comments = comments
        self.save()
        
        # Update parent approval status
        self.payment_approval.update_status()
        
        logger.info(f"Approval step rejected by {approver.username}: {self}")


class ApprovalWorkflow:
    """Manage approval workflow"""
    
    @staticmethod
    def create_approval_request(pr, amount, requested_by, notes=''):
        """
        Create a new payment approval request
        
        Args:
            pr: Purchase Request object
            amount: Payment amount
            requested_by: User requesting approval
            notes: Additional notes
            
        Returns:
            PaymentApproval: Created approval request
        """
        # Create approval request
        approval = PaymentApproval.objects.create(
            pr=pr,
            amount=amount,
            requested_by=requested_by,
            notes=notes
        )
        
        # Get required approval levels
        required_levels = ApprovalLevel.get_required_levels(amount)
        
        # Create approval steps
        for level in required_levels:
            ApprovalStep.objects.create(
                payment_approval=approval,
                approval_level=level
            )
        
        logger.info(f"Approval request created: {approval}")
        
        return approval
    
    @staticmethod
    def approve_step(approval_id, level_id, approver, comments=''):
        """
        Approve a specific step
        
        Args:
            approval_id: PaymentApproval ID
            level_id: ApprovalLevel ID
            approver: User approving
            comments: Approval comments
            
        Returns:
            bool: Success status
        """
        try:
            step = ApprovalStep.objects.get(
                payment_approval_id=approval_id,
                approval_level_id=level_id,
                status='pending'
            )
            
            # Check if approver is authorized
            if approver not in step.approval_level.approvers.all():
                logger.warning(f"Unauthorized approval attempt by {approver.username}")
                return False
            
            step.approve(approver, comments)
            return True
            
        except ApprovalStep.DoesNotExist:
            logger.error(f"Approval step not found: approval={approval_id}, level={level_id}")
            return False
    
    @staticmethod
    def reject_step(approval_id, level_id, approver, comments=''):
        """
        Reject a specific step
        
        Args:
            approval_id: PaymentApproval ID
            level_id: ApprovalLevel ID
            approver: User rejecting
            comments: Rejection comments
            
        Returns:
            bool: Success status
        """
        try:
            step = ApprovalStep.objects.get(
                payment_approval_id=approval_id,
                approval_level_id=level_id,
                status='pending'
            )
            
            # Check if approver is authorized
            if approver not in step.approval_level.approvers.all():
                logger.warning(f"Unauthorized rejection attempt by {approver.username}")
                return False
            
            step.reject(approver, comments)
            return True
            
        except ApprovalStep.DoesNotExist:
            logger.error(f"Approval step not found: approval={approval_id}, level={level_id}")
            return False
    
    @staticmethod
    def get_pending_approvals_for_user(user):
        """
        Get all pending approvals for a user
        
        Args:
            user: User object
            
        Returns:
            QuerySet: Pending approval steps
        """
        return ApprovalStep.objects.filter(
            approval_level__approvers=user,
            status='pending',
            payment_approval__status='pending'
        ).select_related('payment_approval', 'payment_approval__pr')
    
    @staticmethod
    def cancel_approval(approval_id, cancelled_by):
        """
        Cancel an approval request
        
        Args:
            approval_id: PaymentApproval ID
            cancelled_by: User cancelling
            
        Returns:
            bool: Success status
        """
        try:
            approval = PaymentApproval.objects.get(id=approval_id)
            
            if approval.status != 'pending':
                logger.warning(f"Cannot cancel non-pending approval: {approval_id}")
                return False
            
            approval.status = 'cancelled'
            approval.save()
            
            logger.info(f"Approval cancelled by {cancelled_by.username}: {approval}")
            return True
            
        except PaymentApproval.DoesNotExist:
            logger.error(f"Approval not found: {approval_id}")
            return False


# Convenience functions
def request_payment_approval(pr, amount, requested_by, notes=''):
    """Request payment approval"""
    return ApprovalWorkflow.create_approval_request(pr, amount, requested_by, notes)


def approve_payment(approval_id, level_id, approver, comments=''):
    """Approve a payment"""
    return ApprovalWorkflow.approve_step(approval_id, level_id, approver, comments)


def reject_payment(approval_id, level_id, approver, comments=''):
    """Reject a payment"""
    return ApprovalWorkflow.reject_step(approval_id, level_id, approver, comments)


def get_my_pending_approvals(user):
    """Get pending approvals for a user"""
    return ApprovalWorkflow.get_pending_approvals_for_user(user)
