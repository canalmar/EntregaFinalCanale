from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    return render(request, 'core/index.html')

def profile_redirect(request):
    """Captura /accounts/profile/ y envía al Home."""
    return redirect("core:home")