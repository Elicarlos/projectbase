import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.saas.models import Organization  # Import Organization model

from .services import StripeService


class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        try:
            organization = Organization.objects.get(owner=user)
        except Organization.DoesNotExist:
            return Response(
                {"detail": "Organization not found for this user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not organization.stripe_customer_id:
            stripe_customer = StripeService.create_customer(organization)
            organization.stripe_customer_id = stripe_customer.id
            organization.save()

        price_key = request.data.get("price_key")
        price_id = settings.STRIPE_PRICE_IDS[price_key]
        session = StripeService.create_checkout_session(
            customer_id=organization.stripe_customer_id,
            price_id=price_id,
            success_url=settings.STRIPE_SUCCESS_URL,
            cancel_url=settings.STRIPE_CANCEL_URL,
        )

        return Response({"sessionId": session.id}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def stripe_webhook(request):
    """
    Endpoint para receber webhooks do Stripe.
    Deve estar exposto em projectbase/urls.py como:
        path("api/billing/webhook/", stripe_webhook, name="stripe-webhook")
    """
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    # valida assinatura do webhook
    try:
        event = StripeService.retrive_event(payload, sig_header)
    except (ValueError, stripe.error.SignatureVerificationError):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # trate os eventos que interessam
    if event.type == "checkout.session.completed":
        session = event.data.object
        try:
            organization = Organization.objects.get(
                stripe_customer_id=session.customer
            )
            if session.mode == "subscription":
                organization.stripe_subscription_id = session.subscription
                organization.is_active = True
                organization.is_trial = False
                organization.trial_ends_at = None
                organization.save()
        except Organization.DoesNotExist:
            print(
                f"Organization with stripe_customer_id {session.customer} not found."
            )
            return Response(status=status.HTTP_404_NOT_FOUND)

    # outros event.types que você quiser…

    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_upgrade_session(request):
    user = request.user
    org = user.organization
    customer_id = org.stripe_customer_id

    price_key = request.data.get("price_key")
    price_id = settings.STRIPE_PRICE_IDS.get(price_key)

    if not price_id:
        return Response({"error": "Invalid price key"}, status=400)

    session = StripeService.create_checkout_session(
        customer_id=customer_id,
        price_id=price_id,
        success_url=settings.STRIPE_SUCCESS_URL,
        cancel_url=settings.STRIPE_CANCEL_URL,
    )

    return Response({"checkout_url": session.url})
