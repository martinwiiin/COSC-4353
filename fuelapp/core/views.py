from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import JsonResponse

from .forms import SignUpForm, ProfileForm, FuelQuoteForm
from .models import Profile, FuelQuote
from .pricing_module import calculate_price

# Create your views here.
def frontpage(request):
    return render(request, 'core/frontpage.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            
            login(request, user)
            return redirect('frontpage')
    else:
        form = SignUpForm()
    
    return render(request, 'core/signup.html', {'form': form})

def profile_view(request):
    profile = Profile.objects.first()  # Assuming there's only one profile
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')  # Redirect to the profile page
    else:
        profile_form = ProfileForm(instance=profile)
    return render(request, 'core/profile.html', {'profile_form': profile_form})

from django.http import JsonResponse

def FQF(request):
    profile = Profile.objects.first()  # Assuming you have a Profile model
    if request.method == 'POST':
        fuel_quote_form = FuelQuoteForm(request.POST)
        if fuel_quote_form.is_valid():
            fuel_quote = fuel_quote_form.save(commit=False)
            fuel_quote.delivery_address = profile.address1


            has_history = FuelQuote.objects.exists()

            if request.POST.get('get_quote'):
                # Calculate suggested price and total amount due
                suggested_price, total_amount_due = calculate_price(
                    fuel_quote.gallons_requested, profile.state, has_history
                )
                return JsonResponse({
                    'suggested_price': suggested_price,
                    'total_amount_due': total_amount_due
                })
            else:
                # Save the form data to the database
                suggested_price, total_amount_due = calculate_price(
                    fuel_quote.gallons_requested, profile.state, has_history
                )
                fuel_quote.suggested_price = suggested_price
                fuel_quote.total_amount_due = total_amount_due
                fuel_quote.save()
                return redirect('FQF')
    else:
        fuel_quote_form = FuelQuoteForm(initial={'delivery_address': profile.address1})
    return render(request, 'core/FQF.html', {'fuel_quote_form': fuel_quote_form})


def FQH(request):
    fuel_quotes = FuelQuote.objects.all()
    return render(request, 'core/FQH.html', {'fuel_quotes': fuel_quotes})


