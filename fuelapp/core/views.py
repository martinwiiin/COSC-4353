from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import SignUpForm, ProfileForm
from .models import Profile

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
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'core/profile.html', {'form': form})

def FQF(request):
    return render(request, 'core/FQF.html')

def FQH(request):
    return render(request, 'core/FQH.html')
