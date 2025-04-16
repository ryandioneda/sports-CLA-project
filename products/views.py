from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Equipment, Review, Rental, Borrow_Request
from .forms import *
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, UpdateView, ListView
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib import messages
from productCollections.models import Collection
from django.contrib.auth.mixins import LoginRequiredMixin


def product_catalog(request):
    form = EquipmentFilterForm(request.GET)
    private_collections = Collection.objects.filter(collection_privacy="private")
    queryset = Equipment.objects.filter(status="available").exclude(
        collections__in=private_collections
    )

    if form.is_valid():
        if form.cleaned_data["search"]:
            search_query = form.cleaned_data["search"]
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(location__icontains=search_query)
                | Q(brand__icontains=search_query)
            )

        if form.cleaned_data["category"]:
            queryset = queryset.filter(category=form.cleaned_data["category"])

        if form.cleaned_data["condition"]:
            queryset = queryset.filter(condition=form.cleaned_data["condition"])

        if form.cleaned_data["min_price"]:
            queryset = queryset.filter(
                price_per_day__gte=form.cleaned_data["min_price"]
            )

        if form.cleaned_data["max_price"]:
            queryset = queryset.filter(
                price_per_day__lte=form.cleaned_data["max_price"]
            )

        context = {"form": form, "equipment_list": queryset}
        return render(request, "products/catalog.html", context)


def my_products(request, pk):
    if request.user.has_perm("login.lender_perms"):
        user = get_object_or_404(User, pk=pk)
        equipment_list = Equipment.objects.filter(owner=user)
        context = {"equipment_list": equipment_list}
        return render(request, "products/my_equipment.html", context)
    else:
        return redirect("/login/")


class ProductDetailView(generic.DetailView):
    model = Equipment
    template_name = "products/detail.html"

    def get_queryset(self):
        return Equipment.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.has_perm("login.borrower_perms") or user.has_perm(
            "borrower.borrower_perms"
        ):
            context["requested"] = Borrow_Request.objects.filter(
                user=self.request.user, equipment=self.get_object()
            )
        context["reviews"] = self.object.reviews.all()  # fetch related reviews
        return context

    def edit_product(request, pk):
        product = Equipment.objects.get(pk=pk)
        if request.method == "POST":
            pass

    def delete_product(request, pk):
        product = Equipment.objects.get(pk=pk)
        # print("delete button")
        if request.method == "POST":
            product.delete()
            return redirect("/products")

    def request_product(request, pk):
        product = Equipment.objects.get(pk=pk)
        Borrow_Request.objects.create(user=request.user, equipment=product)
        return redirect(f"/products/{pk}/details/")


class ReviewCreate(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "products/review_form.html"
    success_url = reverse_lazy("products:product_catalog")
    # redirect if not logged in
    login_url = "/login/"
    redirect_field_name = "next"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["equipment"] = Equipment.objects.get(
            pk=self.kwargs["pk"]
        )  # Pass equipment to template
        return data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user  # Assign user
        self.object.equipment = Equipment.objects.get(
            pk=self.kwargs["pk"]
        )  # Assign equipment
        self.object.created_at = timezone.now()
        self.object.save()
        return super().form_valid(form)


class EquipmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Equipment
    fields = [
        "name",
        "description",
        "location",
        "price_per_day",
        "condition",
        "category",
        "brand",
        "image",
    ]
    template_name = "products/equipment_form.html"
    # redirect if not logged in
    login_url = "/login/"
    redirect_field_name = "next"

    def get_success_url(self):
        # After successful update, redirect to product detail page
        return reverse_lazy("products:product_detail", kwargs={"pk": self.object.pk})


class ReviewUpdate(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "products/review_form.html"
    success_url = reverse_lazy("products:product_catalog")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["equipment"] = Equipment.objects.get(
            pk=self.kwargs["pk"]
        )  # Pass equipment to template
        return data

    def get_object(self, queryset=None):
        # retrieve URL based on primary key and check if review belongs to user
        return get_object_or_404(Review, pk=self.kwargs["pk"], user=self.request.user)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_at = timezone.now()
        self.object.save()
        return super().form_valid(form)


class EquipmentCreateView(LoginRequiredMixin, CreateView):
    model = Equipment
    fields = [
        "name",
        "description",
        "location",
        "price_per_day",
        "condition",
        "category",
        "brand",
        "image",
    ]
    # redirect if not logged in
    login_url = "/login/"
    redirect_field_name = "next"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.created_at = timezone.now()
        self.object.save()
        return redirect(reverse("products:product_catalog"))

from allauth.account.models import EmailAddress
from django.core.mail import send_mail

def rent_equipment(request, borrow_request_id):
    """Handles borrow request approval"""
    if not request.user.is_authenticated:
        return redirect("/login/")
    borrow_request = get_object_or_404(Borrow_Request, id=borrow_request_id)
    equipment = borrow_request.equipment
    borrower = borrow_request.user
    borrower_email = EmailAddress.objects.get(user=borrower).email

    if equipment.status != "available":
        return render(
            request,
            "products/rental_failure.html",
            {"error": "Equipment is unavailable"},
        )

    equipment.status = "unavailable"
    equipment.save()

    # create rental record
    Rental.objects.create(user=borrower, equipment=equipment)
    borrow_request.delete()


    #! SEND MAIL HERE 
    send_mail(
        "A-17 Renting Request Approval",
        "Thank you for using A-17! You're request has been approved!",
        "a17cla3240@gmail.com",
        [borrower_email],
        fail_silently=False,
    )
    print("successfully sent mail")
    return redirect(reverse("products:manage_requests"))


def deny_equipment(request, borrow_request_id):
    borrow_request = get_object_or_404(Borrow_Request, id=borrow_request_id)
    borrow_request.delete()
    return redirect(reverse("products:manage_requests"))


class RequestsView(DetailView):
    model = Equipment
    template_name = "products/requests.html"
    pk_url_kwarg = "equipment_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipment = self.get_object()
        context["rental_requests"] = Rental.objects.filter(equipment=equipment)
        return context


class ManageRequests(LoginRequiredMixin, ListView):
    model = Borrow_Request
    template_name = "products/manage_requests.html"
    # redirect if not logged in
    login_url = "/login/"
    redirect_field_name = "next"

def my_rentals(request):
    if not request.user.is_authenticated:
        return redirect("login")
    rentals = Rental.objects.filter(user=request.user, active=True)
    context = {"rentals": rentals}
    return render(request, "products/my_rentals.html", context)


def return_rental(request, rental_id):

    if not request.user.is_authenticated:
        return redirect("login")


    rental = get_object_or_404(Rental, id=rental_id, user=request.user, active=True)

    if request.method == "POST":
        rental.active = False
        rental.return_date = timezone.now()
        rental.save()

        equipment = rental.equipment
        equipment.status = "available"
        equipment.save()

        messages.success(request, "Equipment returned successfully.")
        return redirect("products:my_rentals")

    return redirect("products:my_rentals")