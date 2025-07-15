from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from . models import Customer
from .services import StripeService
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt



class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        cust_obj, created = Customer.objects.get_or_create(user=user)
        if created:
            stripe_cust = StripeService.create_customer(user)
            cust_obj.stripe_customer_id = stripe_cust.id
            cust_obj.save()



        price_key = request.data.get('price_key')
        price_id = settings.STRIPE_PRICE_IDS[price_key]
        session = StripeService.create_checkout_session(
            customer_id=cust_obj.stripe_customer_id,
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
        event = StripeService.retrieve_event(payload, sig_header)
    except (ValueError, stripe.error.SignatureVerificationError):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # trate os eventos que interessam
    if event.type == "checkout.session.completed":
        session = event.data.object
        # ex.: marque a assinatura como ativa no seu modelo
        Customer.objects.filter(stripe_customer_id=session.customer).update(
            # por exemplo:
            default_payment_method=session.payment_method
        )

    # outros event.types que você quiser…

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_upgrade_session(request):
    user = request.user 
    org = user.organizantion
    customer_id = org.stripe_custumer_id

    price_key = request.data.get('price_key')
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


