from django.shortcuts import render
from .models import Plan # Import the Plan model

# Create your views here.

def plan_list_view(request):
    """
    Displays the list of available subscription plans.
    """
    """
    Displays the list of available subscription plans.
    """
    # Fetch active plans from the database, ordered by price
    plans = Plan.objects.filter(is_active=True).order_by('price')

    context = {
        'plans': plans
    }
    return render(request, 'payments/plans.html', context)
