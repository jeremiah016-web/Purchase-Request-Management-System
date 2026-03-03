"""
Email Notification System
Sends automated emails for PR status changes, payments, and deliveries
"""
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)


class EmailNotification:
    """Handle email notifications"""
    
    @staticmethod
    def send_email(subject, message, recipient_list, html_message=None):
        """
        Send email notification
        
        Args:
            subject: Email subject
            message: Plain text message
            recipient_list: List of recipient emails
            html_message: HTML version of message (optional)
        """
        try:
            from_email = settings.EMAIL_HOST_USER
            
            if html_message:
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=message,
                    from_email=from_email,
                    to=recipient_list
                )
                email.attach_alternative(html_message, "text/html")
                email.send()
            else:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=recipient_list,
                    fail_silently=False,
                )
            
            logger.info(f"Email sent to {recipient_list}: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"Email sending failed: {str(e)}")
            return False
    
    @staticmethod
    def notify_pr_created(pr, requester):
        """Notify when PR is created"""
        subject = f"Purchase Request Created: {pr.pr_number}"
        
        message = f"""
        Hello {requester.username},
        
        Your purchase request {pr.pr_number} has been created successfully.
        
        Details:
        - Category: {pr.category}
        - Item Type: {pr.item_type}
        - Description: {pr.items_description}
        - Quantity: {pr.quantity}
        - Status: {pr.status}
        
        You will be notified when the buyer reviews your request.
        
        View PR: {settings.SITE_URL}/pr/{pr.id}/
        
        Best regards,
        Purchase Request Management System
        """
        
        return EmailNotification.send_email(
            subject=subject,
            message=message,
            recipient_list=[requester.email]
        )
    
    @staticmethod
    def notify_pr_status_change(pr, recipients):
        """Notify when PR status changes"""
        subject = f"PR Status Update: {pr.pr_number} - {pr.status}"
        
        message = f"""
        Purchase Request Status Update
        
        PR Number: {pr.pr_number}
        New Status: {pr.status}
        Category: {pr.category}
        Item: {pr.item_type}
        
        View PR: {settings.SITE_URL}/pr/{pr.id}/
        
        Best regards,
        Purchase Request Management System
        """
        
        recipient_emails = [r.email for r in recipients if r.email]
        
        return EmailNotification.send_email(
            subject=subject,
            message=message,
            recipient_list=recipient_emails
        )
    
    @staticmethod
    def notify_quotation_submitted(pr, vendor, buyer_emails):
        """Notify buyer when vendor submits quotation"""
        subject = f"New Quotation Received: {pr.pr_number}"
        
        message = f"""
        A vendor has submitted a quotation for PR {pr.pr_number}.
        
        Vendor: {vendor.name}
        Estimated Price: ${pr.estimated_price}
        
        PR Details:
        - Category: {pr.category}
        - Item: {pr.item_type}
        - Description: {pr.items_description}
        
        Please review and approve the quotation.
        
        View PR: {settings.SITE_URL}/pr/{pr.id}/
        
        Best regards,
        Purchase Request Management System
        """
        
        return EmailNotification.send_email(
            subject=subject,
            message=message,
            recipient_list=buyer_emails
        )
    
    @staticmethod
    def notify_vendor_selected(pr, vendor, requester):
        """Notify vendor and requester when vendor is selected"""
        # Notify vendor
        vendor_subject = f"You've been selected for PR: {pr.pr_number}"
        vendor_message = f"""
        Congratulations!
        
        You have been selected as the vendor for PR {pr.pr_number}.
        
        Approved Price: ${pr.total}
        
        PR Details:
        - Item: {pr.item_type}
        - Description: {pr.items_description}
        - Quantity: {pr.quantity}
        
        Please proceed with delivery arrangements.
        
        View PR: {settings.SITE_URL}/pr/{pr.id}/
        
        Best regards,
        Purchase Request Management System
        """
        
        EmailNotification.send_email(
            subject=vendor_subject,
            message=vendor_message,
            recipient_list=[vendor.email] if vendor.email else []
        )
        
        # Notify requester
        requester_subject = f"Vendor Selected for PR: {pr.pr_number}"
        requester_message = f"""
        Good news!
        
        A vendor has been selected for your purchase request {pr.pr_number}.
        
        Vendor: {vendor.name}
        Approved Price: ${pr.total}
        Status: {pr.status}
        
        You will be notified when the items are shipped.
        
        View PR: {settings.SITE_URL}/pr/{pr.id}/
        
        Best regards,
        Purchase Request Management System
        """
        
        return EmailNotification.send_email(
            subject=requester_subject,
            message=requester_message,
            recipient_list=[requester.email]
        )
    
    @staticmethod
    def notify_payment_processed(payment, pr, recipients):
        """Notify when payment is processed"""
        subject = f"Payment Processed: {pr.pr_number}"
        
        message = f"""
        Payment has been processed for PR {pr.pr_number}.
        
        Payment Details:
        - Amount: ${payment.amount}
        - Method: {payment.payment_method}
        - Date: {payment.payment_date}
        - Reference: {payment.reference_number}
        - Status: {payment.status}
        
        PR Details:
        - Total Amount: ${pr.total}
        - Payment Status: {pr.payment_status}
        
        View PR: {settings.SITE_URL}/pr/{pr.id}/
        
        Best regards,
        Purchase Request Management System
        """
        
        recipient_emails = [r.email for r in recipients if r.email]
        
        return EmailNotification.send_email(
            subject=subject,
            message=message,
            recipient_list=recipient_emails
        )
    
    @staticmethod
    def notify_shipment_update(delivery, pr, recipients):
        """Notify when shipment status changes"""
        subject = f"Shipment Update: {pr.pr_number} - {delivery.status}"
        
        message = f"""
        Shipment status update for PR {pr.pr_number}.
        
        Delivery Details:
        - Status: {delivery.status}
        - Tracking Number: {delivery.tracking_number}
        - Carrier: {delivery.carrier}
        - Expected Delivery: {delivery.expected_delivery_date}
        
        Track your shipment: {settings.SITE_URL}/delivery/{delivery.id}/track/
        
        View PR: {settings.SITE_URL}/pr/{pr.id}/
        
        Best regards,
        Purchase Request Management System
        """
        
        recipient_emails = [r.email for r in recipients if r.email]
        
        return EmailNotification.send_email(
            subject=subject,
            message=message,
            recipient_list=recipient_emails
        )
    
    @staticmethod
    def notify_delivery_completed(delivery, pr, requester):
        """Notify when delivery is completed"""
        subject = f"Delivery Completed: {pr.pr_number}"
        
        message = f"""
        Your order has been delivered!
        
        PR Number: {pr.pr_number}
        Delivery Date: {delivery.actual_delivery_date}
        Tracking Number: {delivery.tracking_number}
        
        If you have any issues with the delivery, please contact support.
        
        View PR: {settings.SITE_URL}/pr/{pr.id}/
        
        Thank you for using our Purchase Request Management System!
        
        Best regards,
        Purchase Request Management System
        """
        
        return EmailNotification.send_email(
            subject=subject,
            message=message,
            recipient_list=[requester.email]
        )
    
    @staticmethod
    def notify_payment_approval_required(pr, approvers):
        """Notify approvers when payment needs approval"""
        subject = f"Payment Approval Required: {pr.pr_number}"
        
        message = f"""
        A payment requires your approval.
        
        PR Number: {pr.pr_number}
        Amount: ${pr.total}
        Vendor: {pr.vendor.name if pr.vendor else 'N/A'}
        
        PR Details:
        - Category: {pr.category}
        - Item: {pr.item_type}
        - Requester: {pr.author.username}
        
        Please review and approve/reject the payment.
        
        View PR: {settings.SITE_URL}/pr/{pr.id}/
        
        Best regards,
        Purchase Request Management System
        """
        
        approver_emails = [a.email for a in approvers if a.email]
        
        return EmailNotification.send_email(
            subject=subject,
            message=message,
            recipient_list=approver_emails
        )


# Convenience functions
def send_pr_created_notification(pr):
    """Send notification when PR is created"""
    return EmailNotification.notify_pr_created(pr, pr.author)


def send_status_change_notification(pr, recipients):
    """Send notification when PR status changes"""
    return EmailNotification.notify_pr_status_change(pr, recipients)


def send_quotation_notification(pr, vendor, buyers):
    """Send notification when quotation is submitted"""
    buyer_emails = [b.email for b in buyers if b.email]
    return EmailNotification.notify_quotation_submitted(pr, vendor, buyer_emails)


def send_vendor_selected_notification(pr):
    """Send notification when vendor is selected"""
    if pr.vendor:
        return EmailNotification.notify_vendor_selected(pr, pr.vendor, pr.author)


def send_payment_notification(payment, pr, recipients):
    """Send notification when payment is processed"""
    return EmailNotification.notify_payment_processed(payment, pr, recipients)


def send_shipment_notification(delivery, pr, recipients):
    """Send notification for shipment updates"""
    return EmailNotification.notify_shipment_update(delivery, pr, recipients)


def send_delivery_completed_notification(delivery, pr):
    """Send notification when delivery is completed"""
    return EmailNotification.notify_delivery_completed(delivery, pr, pr.author)


def send_payment_approval_notification(pr, approvers):
    """Send notification when payment needs approval"""
    return EmailNotification.notify_payment_approval_required(pr, approvers)
