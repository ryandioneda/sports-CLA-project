from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.views import generic
from .models import Profile
from django.contrib.auth.models import User, Group, Permission

# Create your views here.


def index(request):
    return render(request, "login/login.html")


def logout_view(request):
    logout(request)
    return redirect("/")


# class ProfileView(generic.DetailView):
# model = Profile
#  template_name = "login/profile.html"

##    def get


def profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method == "POST":
        if "main_submit" in request.POST:
            profile.fname = request.POST.get("fname")
            profile.lname = request.POST.get("lname")
            birth_date = request.POST.get("birth_date")
            profile.birth_date = birth_date if birth_date else None 
            profile.address = request.POST.get("address")
            profile.city = request.POST.get("city")
            profile.state = request.POST.get("state")
            profile.zip_code = request.POST.get("zip_code")
            profile.image = request.FILES.get("image")
            profile.save()
            ##return redirect() redirect to main page?
        elif "email_submit" in request.POST:
            input_email = request.POST.get("email")
            other_user = User.objects.get(email=input_email.lower())

            if other_user is not None:
                other_user.user_permissions.add(
                    Permission.objects.get(name="Global lender permissions")
                )
                other_user.user_permissions.remove(
                    Permission.objects.get(name="Global borrower permissions")
                )

    return render(request, "login/profile.html", {"profile": profile})
