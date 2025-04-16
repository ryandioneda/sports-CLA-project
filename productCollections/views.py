from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from .models import Collection, Collection_Request
from .forms import CollectionFilterForm, EditCollectionForm
from .forms import *
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, UpdateView, ListView

from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User, Permission
from login.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from products.models import Equipment


def view_collection(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)

    # if request.method == "POST":

    #     if "update_collection" in request.POST:
    #         form = EditCollectionForm(request.POST, instance=collection)
    #         if form.is_valid():
    #             form.save()
    #             messages.success(request, "Collection updated successfully.")
    #             return redirect(
    #                 "productCollections:edit_collection", collection_id=collection.id
    #             )
    #         else:
    #             messages.error(request, "Please correct the errors below.")

    #     elif "delete_collection" in request.POST:
    #         collection.delete()
    #         messages.success(request, "Collection deleted successfully.")
    #         return redirect("productCollections:my_collections")

    #     elif "add_product" in request.POST:
    #         product_id = request.POST.get("product_id")
    #         product = get_object_or_404(Equipment, id=product_id)

    #         private_collections = product.collections.filter(
    #             collection_privacy="private"
    #         )
    #         if private_collections.exists() and collection not in private_collections:
    #             messages.error(
    #                 request,
    #                 "This product is already in a private collection and cannot be added to another collection.",
    #             )
    #             return redirect(
    #                 "productCollections:edit_collection", collection_id=collection.id
    #             )
    #         product.collections.add(collection)
    #         messages.success(request, "Product added successfully.")
    #         return redirect(
    #             "productCollections:edit_collection", collection_id=collection.id
    #         )

    #     elif "remove_product" in request.POST:
    #         product_id = request.POST.get("product_id")
    #         product = get_object_or_404(Equipment, id=product_id)
    #         product.collections.remove(collection)
    #         messages.success(request, "Product removed successfully.")
    #         return redirect(
    #             "productCollections:edit_collection", collection_id=collection.id
    #         )
    # else:
    #
    form = EditCollectionForm(instance=collection)

    search_query = request.GET.get("search", "")
    # products = Equipment.objects.none()
    collection_products = Equipment.objects.filter(collections=collection)
    products = collection_products
    if search_query:
        products = Equipment.objects.filter(
            Q(name__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(location__icontains=search_query)
            | Q(brand__icontains=search_query)
        )

    context = {
        "form": form,
        "collection": collection,
        "products": products,
        "collection_products": collection_products,
        "search_query": search_query,
    }
    return render(request, "productCollections/view_collection.html", context)


@login_required
def edit_collection(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)

    if request.method == "POST":

        if "update_collection" in request.POST:
            form = EditCollectionForm(request.POST, instance=collection)
            if form.is_valid():
                form.save()
                messages.success(request, "Collection updated successfully.")
                return redirect(
                    "productCollections:edit_collection", collection_id=collection.id
                )
            else:
                messages.error(request, "Please correct the errors below.")

        elif "delete_collection" in request.POST:
            collection.delete()
            messages.success(request, "Collection deleted successfully.")
            return redirect("productCollections:my_collections")

        elif "add_product" in request.POST:
            product_id = request.POST.get("product_id")
            product = get_object_or_404(Equipment, id=product_id)

            private_collections = product.collections.filter(
                collection_privacy="private"
            )
            if private_collections.exists() and collection not in private_collections:
                messages.error(
                    request,
                    "This product is already in a private collection and cannot be added to another collection.",
                )
                return redirect(
                    "productCollections:edit_collection", collection_id=collection.id
                )
            if collection.collection_privacy == "private":
                # print("private, try remove")
                public_collections = product.collections.filter(
                    collection_privacy="public"
                )
                for public_collection in public_collections:
                    product.collections.remove(public_collection)
            product.collections.add(collection)
            messages.success(request, "Product added successfully.")

            return redirect(
                "productCollections:edit_collection", collection_id=collection.id
            )

        elif "remove_product" in request.POST:
            product_id = request.POST.get("product_id")
            product = get_object_or_404(Equipment, id=product_id)
            product.collections.remove(collection)
            messages.success(request, "Product removed successfully.")
            return redirect(
                "productCollections:edit_collection", collection_id=collection.id
            )
    else:
        form = EditCollectionForm(instance=collection)

    search_query = request.GET.get("search", "")
    # products = Equipment.objects.none()
    collection_products = Equipment.objects.filter(collections=collection)
    products = collection_products
    if search_query:
        products = Equipment.objects.filter(
            Q(name__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(location__icontains=search_query)
            | Q(brand__icontains=search_query)
        )

    user = request.user
    if user.has_perm("login.borrower_perms"):
        form.fields.pop("collection_privacy")
        form.fields.pop("collection_private_userlist")

    context = {
        "form": form,
        "collection": collection,
        "products": products,
        "collection_products": collection_products,
        "search_query": search_query,
    }
    return render(request, "productCollections/edit_collection.html", context)


def collection_catalog(request):
    form = CollectionFilterForm(request.GET)
    queryset = Collection.objects.all()
    user = request.user
    if request.user.has_perm("login.lender_perms") or request.user.has_perm(
        "login.borrower_perms"
    ):
        queryset = Collection.objects.get_queryset()
    else:
        queryset = Collection.objects.filter(Q(collection_privacy="public"))

    if form.is_valid():
        if form.cleaned_data["search"]:
            search_query = form.cleaned_data["search"]
            queryset = queryset.filter(
                Q(collection_name__icontains=search_query)
                | Q(collection_description__icontains=search_query)
            )

        if form.cleaned_data["collection_privacy"]:
            queryset = queryset.filter(
                collection_privacy=form.cleaned_data["collection_privacy"]
            )

        context = {
            "form": form,
            "collection_list": queryset,
        }
        return render(request, "productCollections/view_collections.html", context)


class MakeCollectionsCreateView(LoginRequiredMixin, CreateView):
    model = Collection
    fields = [
        "collection_name",
        "collection_description",
        "collection_privacy",
        "collection_private_userlist",
    ]
    # redirect if not logged in
    login_url = "/login/"
    redirect_field_name = "next"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user

        if user.has_perm("login.borrower_perms"):
            form.fields.pop("collection_privacy")
            form.fields.pop("collection_private_userlist")

        elif user.has_perm("login.lender_perms"):
            form.fields["collection_privacy"].choices = (
                Collection.LENDER_PRIVACY_CHOICES
            )

        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.owner = self.request.user

        self.object.created_at = timezone.now()

        self.object.save()
        if self.request.user.has_perm("login.lender_perms"):
            form.save_m2m()

        return redirect(reverse("productCollections:make_collections"))


def my_collections(request):
    form = CollectionFilterForm(request.GET)

    if request.user.has_perm("login.lender_perms"):
        queryset = Collection.objects.get_queryset()
    elif request.user.has_perm("login.borrower_perms"):
        queryset = Collection.objects.filter(owner=request.user)

    if form.is_valid():
        if form.cleaned_data["search"]:
            search_query = form.cleaned_data["search"]
            queryset = queryset.filter(
                Q(collection_name__icontains=search_query)
                | Q(collection_description__icontains=search_query)
            )

        context = {"form": form, "collection_list": queryset}
        return render(request, "productCollections/catalog.html", context)


def approve_collection(request, collection_request_id):
    if not request.user.is_authenticated:
        return redirect("login")
    borrow_request = get_object_or_404(Collection_Request, id=collection_request_id)
    collection_to_borrow = borrow_request.collection
    collection_to_borrow.collection_private_userlist.add(borrow_request.user)
    collection_to_borrow.save()
    borrow_request.delete()
    return redirect(reverse("productCollections:manage_collection_requests"))


def deny_collection(request, collection_request_id):
    borrow_request = get_object_or_404(Collection_Request, id=collection_request_id)
    borrow_request.delete()
    return redirect(reverse("productCollections:manage_collection_requests"))

class ManageCollectionRequests(LoginRequiredMixin, ListView):
    model = Collection_Request
    template_name = "productCollections/manage_collection_requests.html"
    # redirect if not logged in
    login_url = "/login/"
    redirect_field_name = "next"
    def post(self, request, *args, **kwargs):
        collection_id = request.POST.get("collection_id")
        collection = get_object_or_404(Collection, id=collection_id)
        Collection_Request.objects.get_or_create(
            collection=collection, user=request.user
        )
        return redirect(reverse("productCollections:view_collections"))