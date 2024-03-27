from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import SignUpForm, ProfileForm, FuelQuoteForm
from .models import Profile, FuelQuote

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

def FQF(request):
    profile = Profile.objects.first()
    if request.method == 'POST':
        fuel_quote_form = FuelQuoteForm(request.POST)
        if fuel_quote_form.is_valid():
            FQF = fuel_quote_form.save()
            FQF.delivery_address = profile.address1
            FQF.save()
            return redirect('FQF')
    else:
        fuel_quote_form = FuelQuoteForm(initial={'delivery_address': profile.address1})
    return render(request, 'core/FQF.html' , {'fuel_quote_form': fuel_quote_form})

def FQH(request):
    fuel_quotes = FuelQuote.objects.all()
    return render(request, 'core/FQH.html', {'fuel_quotes': fuel_quotes})
