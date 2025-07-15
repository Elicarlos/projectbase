import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeService:
    @staticmethod
    def create_customer(user):
        customer = stripe.Customer.create(
            email = user.email,
            name = f"{user.first_name} {user.last_name}",
            metadata = {'user_id': user.id}
        )

        return customer


    @staticmethod
    def create_payment_method(customer_id, price_id, success_url, cancel_url):
        session = stripe.checkout.Session.create(
            customer = customer_id,
            payment_method_types = ['card'],
            line_items = [{price: price_id, quantity: 1}],
            mode = 'payment',
            success_url= success_url,
            cancel_url=cancel_url,
        )

        return session

    @staticmethod
    def retrive_event(payload, sig_header):
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )

        except (ValueError, stripe.error.SignatureVerificationError) as e:
            raise e
        
        return event


    @staticmethod
    def get_last_invoice_date(stripe_customer_id):
        invoices = strip.Invoice.list(customer=stripe_customer_id, limit=1)
        if invoices and invoices.data:
            invoice = invoices.data[0]
            return invoice..created
        
        return None

    @staticmethod
    def create_checkout_session(customer_id, price_id, success_url, cancel_url):
        return stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=["card"],
            line_items=[{
                "price": price_id,
                "quantity": 1,
            }],
            mode="subscription",
            success_url=success_url,
            cancel_url=cancel_url,
        )