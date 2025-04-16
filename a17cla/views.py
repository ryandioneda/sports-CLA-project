from django.shortcuts import render


def index(request):
    # if request.user.has_perm('login.lender_perms'):
    #     return render(request, "lender_home.html")
    # elif request.user.has_perm('login.borrower_perms'):
    #     return render(request, "borrower_home.html")
    return render(request, "index.html")
