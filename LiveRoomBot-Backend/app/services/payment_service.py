import os
import hashlib
import hmac
import json
import uuid
from datetime import datetime
from typing import Dict, Optional
import requests
from sqlalchemy.orm import Session
from app.models.user import User, SubscriptionPlan
from app.core.config import settings

class PaymentService:
    """Service for handling UPI payments and payment gateway integration"""
    
    def __init__(self, db: Session):
        self.db = db
        # In production, you would use actual payment gateway credentials
        self.merchant_id = settings.UPI_MERCHANT_ID if hasattr(settings, 'UPI_MERCHANT_ID') else "LIVEROOM001"
        self.merchant_key = settings.UPI_MERCHANT_KEY if hasattr(settings, 'UPI_MERCHANT_KEY') else "test_key_123"
        self.base_url = settings.PAYMENT_GATEWAY_URL if hasattr(settings, 'PAYMENT_GATEWAY_URL') else "https://api.razorpay.com/v1"
    
    def create_payment_order(self, user_id: int, plan: SubscriptionPlan) -> Dict:
        """Create a payment order for subscription upgrade"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        if plan == SubscriptionPlan.FREE:
            raise ValueError("Cannot create payment for free plan")
        
        # Get plan details
        from app.services.subscription_service import SubscriptionService
        subscription_service = SubscriptionService(self.db)
        plan_info = subscription_service.PLANS[plan]
        
        # Generate unique order ID
        order_id = f"LR_{user_id}_{int(datetime.utcnow().timestamp())}_{uuid.uuid4().hex[:8]}"
        
        # Create payment order (mock implementation)
        # In production, integrate with actual payment gateway like Razorpay, PayU, etc.
        payment_order = {
            "order_id": order_id,
            "amount": plan_info["price"] * 100,  # Amount in paise
            "currency": "INR",
            "receipt": f"receipt_{order_id}",
            "notes": {
                "user_id": str(user_id),
                "plan": plan.value,
                "user_email": user.email
            }
        }
        
        # Generate UPI payment link
        upi_link = self._generate_upi_link(
            amount=plan_info["price"],
            order_id=order_id,
            description=f"LiveRoom {plan_info['name']} Subscription"
        )
        
        return {
            "order_id": order_id,
            "amount": plan_info["price"],
            "currency": "INR",
            "plan": plan.value,
            "plan_name": plan_info["name"],
            "upi_link": upi_link,
            "qr_code_url": f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={upi_link}",
            "payment_methods": ["UPI", "Card", "Net Banking"],
            "expires_at": int((datetime.utcnow().timestamp() + 3600) * 1000),  # 1 hour expiry
            "callback_url": f"{settings.HOST}/api/v1/payments/callback"
        }
    
    def _generate_upi_link(self, amount: float, order_id: str, description: str) -> str:
        """Generate UPI payment link"""
        # Get UPI details from environment
        merchant_upi = os.getenv("UPI_VPA", "technams2002@okhdfcbank")
        merchant_name = os.getenv("UPI_MERCHANT_NAME", "LiveRoom AI")
        transaction_note = f"{description} - Order: {order_id}"

        # UPI link format: upi://pay?pa=merchant@upi&pn=MerchantName&am=amount&tr=transactionId&tn=description
        upi_link = (
            f"upi://pay?"
            f"pa={merchant_upi}&"
            f"pn={merchant_name}&"
            f"am={amount}&"
            f"tr={order_id}&"
            f"tn={transaction_note}&"
            f"cu=INR"
        )

        return upi_link
    
    def verify_payment(self, order_id: str, payment_id: str, signature: str) -> Dict:
        """Verify payment signature and process payment"""
        # In production, verify with actual payment gateway
        # This is a mock implementation
        
        # Extract user_id and plan from order_id
        try:
            parts = order_id.split('_')
            user_id = int(parts[1])
        except (IndexError, ValueError):
            raise ValueError("Invalid order ID format")
        
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        # Mock signature verification (in production, use actual gateway verification)
        expected_signature = self._generate_signature(order_id, payment_id)
        
        if signature != expected_signature:
            return {
                "success": False,
                "error": "Invalid payment signature",
                "order_id": order_id
            }
        
        # Payment verified successfully
        return {
            "success": True,
            "payment_id": payment_id,
            "order_id": order_id,
            "user_id": user_id,
            "verified": True
        }
    
    def _generate_signature(self, order_id: str, payment_id: str) -> str:
        """Generate payment signature for verification"""
        # Mock signature generation (use actual gateway logic in production)
        message = f"{order_id}|{payment_id}"
        signature = hmac.new(
            self.merchant_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def process_successful_payment(self, order_id: str, payment_id: str, plan: SubscriptionPlan) -> Dict:
        """Process successful payment and upgrade user subscription"""
        try:
            # Extract user_id from order_id
            parts = order_id.split('_')
            user_id = int(parts[1])
        except (IndexError, ValueError):
            raise ValueError("Invalid order ID format")
        
        # Upgrade subscription
        from app.services.subscription_service import SubscriptionService
        subscription_service = SubscriptionService(self.db)
        result = subscription_service.upgrade_subscription(user_id, plan, payment_id)
        
        # Store payment record
        self._store_payment_record(user_id, order_id, payment_id, plan)
        
        return result
    
    def _store_payment_record(self, user_id: int, order_id: str, payment_id: str, plan: SubscriptionPlan):
        """Store payment record in database"""
        # In production, you might want a separate payments table
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.last_payment_date = datetime.utcnow()
            from app.services.subscription_service import SubscriptionService
            subscription_service = SubscriptionService(self.db)
            user.total_spent += subscription_service.PLANS[plan]["price"]
            self.db.commit()
    
    def get_payment_history(self, user_id: int) -> Dict:
        """Get user's payment history"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        # Mock payment history (in production, fetch from payments table)
        return {
            "user_id": user_id,
            "total_spent": user.total_spent,
            "last_payment": user.last_payment_date,
            "current_plan": user.subscription_plan.value,
            "subscription_end": user.subscription_end_date,
            "payments": [
                # In production, fetch actual payment records
                {
                    "date": user.last_payment_date,
                    "amount": 100 if user.subscription_plan == SubscriptionPlan.BASIC else 1000,
                    "plan": user.subscription_plan.value,
                    "status": "success",
                    "payment_method": "UPI"
                }
            ] if user.last_payment_date else []
        }
    
    def cancel_subscription(self, user_id: int) -> Dict:
        """Cancel user's subscription (downgrade to free at end of period)"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        if user.subscription_plan == SubscriptionPlan.FREE:
            return {
                "success": False,
                "message": "User is already on free plan"
            }
        
        # Don't immediately downgrade, let them use until subscription ends
        return {
            "success": True,
            "message": "Subscription will not be renewed. You can continue using premium features until your current subscription expires.",
            "expires_on": user.subscription_end_date,
            "plan_after_expiry": "free"
        }
    
    def get_payment_methods(self) -> Dict:
        """Get available payment methods"""
        return {
            "methods": [
                {
                    "id": "upi",
                    "name": "UPI",
                    "description": "Pay using any UPI app",
                    "icon": "upi_icon.png",
                    "enabled": True
                },
                {
                    "id": "card",
                    "name": "Credit/Debit Card",
                    "description": "Visa, Mastercard, RuPay",
                    "icon": "card_icon.png",
                    "enabled": True
                },
                {
                    "id": "netbanking",
                    "name": "Net Banking",
                    "description": "All major banks supported",
                    "icon": "bank_icon.png",
                    "enabled": True
                },
                {
                    "id": "wallet",
                    "name": "Digital Wallets",
                    "description": "Paytm, PhonePe, Google Pay",
                    "icon": "wallet_icon.png",
                    "enabled": True
                }
            ],
            "preferred": "upi",
            "currency": "INR"
        }
    
    def generate_payment_qr(self, order_id: str, amount: float) -> str:
        """Generate QR code for payment"""
        upi_link = self._generate_upi_link(
            amount=amount,
            order_id=order_id,
            description="LiveRoom Subscription"
        )
        
        # Generate QR code URL
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={upi_link}"
        return qr_url
    
    def webhook_handler(self, payload: Dict, signature: str) -> Dict:
        """Handle payment gateway webhooks"""
        # Verify webhook signature
        # Process payment status updates
        # Update subscription status
        
        event_type = payload.get("event")
        
        if event_type == "payment.captured":
            # Payment successful
            order_id = payload.get("payload", {}).get("payment", {}).get("entity", {}).get("order_id")
            payment_id = payload.get("payload", {}).get("payment", {}).get("entity", {}).get("id")
            
            # Process the successful payment
            # This would trigger subscription upgrade
            
            return {"status": "processed"}
        
        elif event_type == "payment.failed":
            # Payment failed
            return {"status": "failed"}
        
        return {"status": "ignored"}
