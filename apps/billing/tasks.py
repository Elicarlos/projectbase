from celery import shared_task

from apps.saas.models import Organization


@shared_task
def process_stripe_webhook_event(event_type, event_data):
    """
    Processes Stripe webhook events asynchronously.
    """
    if event_type == "checkout.session.completed":
        session = event_data
        try:
            organization = Organization.objects.get(
                stripe_customer_id=session["customer"]
            )
            if session["mode"] == "subscription":
                organization.stripe_subscription_id = session["subscription"]
                organization.is_active = True
                organization.is_trial = False
                organization.trial_ends_at = None
                organization.save()
                print(f"Organization {organization.name} subscription updated.")
        except Organization.DoesNotExist:
            print(
                f"Organization with stripe_customer_id {session['customer']} not found for checkout.session.completed."
            )

    elif event_type == "customer.subscription.updated":
        subscription = event_data
        try:
            organization = Organization.objects.get(
                stripe_subscription_id=subscription["id"]
            )
            organization.is_active = subscription["status"] == "active"
            organization.trial_ends_at = (
                subscription["trial_end"] if subscription["trial_end"] else None
            )
            organization.save()
            print(f"Organization {organization.name} subscription updated.")
        except Organization.DoesNotExist:
            print(
                f"Organization with stripe_subscription_id {subscription['id']} not found for customer.subscription.updated."
            )

    elif event_type == "customer.subscription.deleted":
        subscription = event_data
        try:
            organization = Organization.objects.get(
                stripe_subscription_id=subscription["id"]
            )
            organization.is_active = False
            organization.save()
            print(f"Organization {organization.name} subscription deleted.")
        except Organization.DoesNotExist:
            print(
                f"Organization with stripe_subscription_id {subscription['id']} not found for customer.subscription.deleted."
            )

    else:
        print(f"Unhandled event type: {event_type}")
