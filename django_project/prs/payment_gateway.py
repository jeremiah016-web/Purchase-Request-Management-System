"""
Payment Gateway Integration
Supports Stripe and PayPal
"""
import stripe
import paypalrestsdk
from django.conf import settings
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

# Initialize Stripe
stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')

# Initialize PayPal
paypalrestsdk.configure({
    "mode": getattr(settings, 'PAYPAL_MODE', 'sandbox'),
    "client_id": getattr(settings, 'PAYPAL_CLIENT_ID', ''),
    "client_secret": getattr(settings, 'PAYPAL_CLIENT_SECRET', '')
})


class StripePaymentGateway:
    """Handle Stripe payments"""
    
    @staticmethod
    def create_payment_intent(amount, currency='usd', metadata=None):
        """
        Create a Stripe payment intent
        
        Args:
            amount: Amount in smallest currency unit (cents for USD)
            currency: Currency code (default: usd)
            metadata: Additional data to attach to payment
            
        Returns:
            dict: Payment intent details or error
        """
        try:
            # Convert to cents
            amount_cents = int(float(amount) * 100)
            
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency=currency,
                metadata=metadata or {},
                automatic_payment_methods={'enabled': True},
            )
            
            return {
                'success': True,
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id,
                'amount': amount,
                'currency': currency
            }
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def confirm_payment(payment_intent_id):
        """
        Confirm a payment intent
        
        Args:
            payment_intent_id: Stripe payment intent ID
            
        Returns:
            dict: Payment status
        """
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            return {
                'success': True,
                'status': intent.status,
                'amount': intent.amount / 100,  # Convert back to dollars
                'currency': intent.currency
            }
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def create_refund(payment_intent_id, amount=None):
        """
        Create a refund for a payment
        
        Args:
            payment_intent_id: Stripe payment intent ID
            amount: Amount to refund (None for full refund)
            
        Returns:
            dict: Refund details
        """
        try:
            refund_data = {'payment_intent': payment_intent_id}
            
            if amount:
                refund_data['amount'] = int(float(amount) * 100)
            
            refund = stripe.Refund.create(**refund_data)
            
            return {
                'success': True,
                'refund_id': refund.id,
                'status': refund.status,
                'amount': refund.amount / 100
            }
        except stripe.error.StripeError as e:
            logger.error(f"Stripe refund error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }


class PayPalPaymentGateway:
    """Handle PayPal payments"""
    
    @staticmethod
    def create_payment(amount, currency='USD', description='Purchase Request Payment'):
        """
        Create a PayPal payment
        
        Args:
            amount: Payment amount
            currency: Currency code (default: USD)
            description: Payment description
            
        Returns:
            dict: Payment details or error
        """
        try:
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": f"{settings.SITE_URL}/payment/paypal/success/",
                    "cancel_url": f"{settings.SITE_URL}/payment/paypal/cancel/"
                },
                "transactions": [{
                    "amount": {
                        "total": str(amount),
                        "currency": currency
                    },
                    "description": description
                }]
            })
            
            if payment.create():
                # Get approval URL
                approval_url = None
                for link in payment.links:
                    if link.rel == "approval_url":
                        approval_url = link.href
                        break
                
                return {
                    'success': True,
                    'payment_id': payment.id,
                    'approval_url': approval_url,
                    'amount': amount,
                    'currency': currency
                }
            else:
                logger.error(f"PayPal error: {payment.error}")
                return {
                    'success': False,
                    'error': payment.error
                }
        except Exception as e:
            logger.error(f"PayPal exception: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def execute_payment(payment_id, payer_id):
        """
        Execute an approved PayPal payment
        
        Args:
            payment_id: PayPal payment ID
            payer_id: PayPal payer ID
            
        Returns:
            dict: Execution result
        """
        try:
            payment = paypalrestsdk.Payment.find(payment_id)
            
            if payment.execute({"payer_id": payer_id}):
                return {
                    'success': True,
                    'payment_id': payment.id,
                    'state': payment.state,
                    'amount': payment.transactions[0].amount.total
                }
            else:
                logger.error(f"PayPal execution error: {payment.error}")
                return {
                    'success': False,
                    'error': payment.error
                }
        except Exception as e:
            logger.error(f"PayPal execution exception: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def refund_payment(sale_id, amount=None):
        """
        Refund a PayPal payment
        
        Args:
            sale_id: PayPal sale ID
            amount: Amount to refund (None for full refund)
            
        Returns:
            dict: Refund details
        """
        try:
            sale = paypalrestsdk.Sale.find(sale_id)
            
            refund_data = {}
            if amount:
                refund_data = {
                    "amount": {
                        "total": str(amount),
                        "currency": "USD"
                    }
                }
            
            refund = sale.refund(refund_data)
            
            if refund.success():
                return {
                    'success': True,
                    'refund_id': refund.id,
                    'state': refund.state
                }
            else:
                logger.error(f"PayPal refund error: {refund.error}")
                return {
                    'success': False,
                    'error': refund.error
                }
        except Exception as e:
            logger.error(f"PayPal refund exception: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }


def process_payment(payment_method, amount, pr_number, metadata=None):
    """
    Unified payment processing function
    
    Args:
        payment_method: 'stripe' or 'paypal'
        amount: Payment amount
        pr_number: Purchase request number
        metadata: Additional payment data
        
    Returns:
        dict: Payment result
    """
    metadata = metadata or {}
    metadata['pr_number'] = pr_number
    
    if payment_method.lower() == 'stripe':
        return StripePaymentGateway.create_payment_intent(
            amount=amount,
            metadata=metadata
        )
    elif payment_method.lower() == 'paypal':
        return PayPalPaymentGateway.create_payment(
            amount=amount,
            description=f"Payment for PR {pr_number}"
        )
    else:
        return {
            'success': False,
            'error': f'Unsupported payment method: {payment_method}'
        }
