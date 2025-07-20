from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse # Added JsonResponse if needed for webhook
import stripe # Keep import for now, but comment out usage
from django.http import HttpResponse # Added for webhook placeholder

from .models import SubscriptionPlan, CompanySubscription

# Set Stripe API key
# stripe.api_key = settings.STRIPE_SECRET_KEY # Commented out until configured

# Create your views here.

@login_required
def plan_list(request):
    plans = SubscriptionPlan.objects.filter(is_active=True).order_by('price')
    context = {'plans': plans}
    return render(request, 'payments/plans.html', context)

# --- Stripe Integration Views (Commented Out Temporarily) ---

# @login_required
# def create_checkout_session(request, plan_id):

   # Ensure the user is a company representative
    if not hasattr(request.user, 'companyprofile') or not request.user.is_company:
        messages.error(request, "Doar companiile pot achiziționa abonamente.")
        return redirect('plati:planuri')

    try:
        plan = get_object_or_404(SubscriptionPlan, pk=plan_id)
    except SubscriptionPlan.DoesNotExist:
        messages.error(request, "Planul selectat nu a fost găsit.")
        return redirect('plati:planuri')

    # Check if the plan is free
    if plan.price == 0:
        messages.info(request, "Acesta este un plan gratuit și nu necesită plată.")
        # Optionally, activate the free plan directly here if needed
        return redirect('plati:planuri')

    # Build success and cancel URLs
    success_url = request.build_absolute_uri(reverse('plati:plata_reusita'))
    cancel_url = request.build_absolute_uri(reverse('plati:plata_anulata'))

    try:
        # Create Stripe Checkout Session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': plan.currency.lower(),
                        'product_data': {
                            'name': plan.name,
                            'description': f"Abonament {plan.name} pentru JoburiExpress",
                        },
                        'unit_amount': int(plan.price * 100), # Stripe expects amount in cents
                    },
                    'quantity': 1,
                },
            ],
            mode='payment', # Use 'subscription' for recurring payments
            success_url=success_url + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=cancel_url,
            client_reference_id=request.user.id, # Associate session with user
            metadata={
                'plan_id': plan.id,
                'user_id': request.user.id,
                'company_id': request.user.companyprofile.id
            }
        )
        # Redirect to Stripe Checkout
        return HttpResponseRedirect(checkout_session.url)

    except stripe.error.StripeError as e:
        messages.error(request, f"A apărut o eroare la procesarea plății: {e}")
        return redirect('plati:planuri')
    except Exception as e:
        messages.error(request, f"A apărut o eroare neașteptată: {e}")
        # return redirect('plati:planuri')


# @login_required
# def payment_success(request):
    # session_id = request.GET.get('session_id')
    if not session_id:
        messages.warning(request, "Sesiunea de plată nu a fost găsită.")
        return redirect('plati:planuri')

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        # TODO: Implement logic to fulfill the order based on session data
        # Example: Retrieve metadata, find plan, update CompanySubscription
        plan_id = session.metadata.get('plan_id')
        user_id = session.metadata.get('user_id')
        company_id = session.metadata.get('company_id')

        if not all([plan_id, user_id, company_id]):
             messages.error(request, "Informații incomplete în sesiunea de plată.")
             return redirect('plati:planuri')

        # --- Add logic here to activate the subscription for the company --- 
        # Example (needs refinement based on your CompanySubscription model):
        # plan = SubscriptionPlan.objects.get(pk=plan_id)
        # company_profile = CompanyProfile.objects.get(pk=company_id)
        # CompanySubscription.objects.update_or_create(
        #     company=company_profile,
        #     defaults={'plan': plan, 'is_active': True, 'stripe_session_id': session_id}
        # )
        # ------------------------------------------------------------------

        messages.success(request, "Plata a fost efectuată cu succes! Abonamentul dumneavoastră este activ.")
        # Redirect to a relevant page, like the company dashboard
        return render(request, 'payments/payment_success.html')

    except stripe.error.StripeError as e:
        messages.error(request, f"Eroare la verificarea sesiunii de plată: {e}")
        return redirect('plati:planuri')
    except Exception as e:
        # Log the error e
        messages.error(request, "A apărut o eroare la procesarea confirmării plății.")
        # return redirect('plati:planuri')


# @login_required
# def payment_cancel(request):
    # messages.warning(request, "Procesul de plată a fost anulat.")
    return render(request, 'payments/payment_cancel.html')

# Optional: Stripe Webhook View (Requires CSRF exemption)
# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
#     endpoint_secret = settings.STRIPE_WEBHOOK_SECRET # Define this in your settings
#     event = None
#
#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#     except ValueError as e:
#         # Invalid payload
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return HttpResponse(status=400)
#
#     # Handle the checkout.session.completed event
#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']
#         # Fulfill the purchase based on session data
#         # Retrieve metadata, find plan, update CompanySubscription etc.
#         print('Payment was successful!')
#         # Add your fulfillment logic here
#
#     # ... handle other event types
#
#     return HttpResponse(status=200)
