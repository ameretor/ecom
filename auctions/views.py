import datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Comments, User, listing, Gender, watchList, category
from .forms import Add_listing


def index(request):
    user = request.user
    listings = listing.objects.all()
    list_of_genders = Gender.objects.all()
    content = {
        "user": user,
        "listings": listings,
        "genders": list_of_genders,
        "form": Add_listing(),
    }
    if request.method == "POST":
        return render(request, "auctions/index.html", content)
    return render(request, "auctions/index.html", content)


def login_view(request):
    if request.method != "POST":
        return render(request, "auctions/login.html")

    # Attempt to sign user in
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    # Check if authentication successful
    if user is None:
        return render(
            request,
            "auctions/login.html",
            {"message": "Invalid username and/or password."},
        )
    login(request, user)
    return HttpResponseRedirect(reverse("index"))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method != "POST":
        return render(request, "auctions/register.html")
    username = request.POST["username"]
    email = request.POST["email"]

    # Ensure password matches confirmation
    password = request.POST["password"]
    confirmation = request.POST["confirmation"]
    if password != confirmation:
        return render(
            request, "auctions/register.html", {"message": "Passwords must match."}
        )

    # Attempt to create new user
    try:
        user = User.objects.create_user(username, email, password)
        user.save()
    except IntegrityError:
        return render(
            request, "auctions/register.html", {"message": "Username already taken."}
        )
    login(request, user)
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url="/login")
def create_listing(request):
    """Create Auction listing"""
    if request.method != "POST":

        return render(request, "auctions/create_listing.html", {"form": Add_listing()})
    form = Add_listing(request.POST)

    if not form.is_valid():
        print("Wrong")
        return HttpResponseRedirect(reverse("create_listing"))
    print("congratulation! I did a bit")
    title = form.cleaned_data["title"]
    description = form.cleaned_data["description"]
    stock = form.cleaned_data["stock"]
    category = form.cleaned_data["category"]
    sex = form.cleaned_data["sex"]
    end_date = form.cleaned_data["end_date"]
    latest_bid = form.cleaned_data["latest_bid"]
    image = request.POST.get("image")

    # Populate data into database
    listing.objects.create(
        user=request.user,
        title=title,
        description=description,
        stock=stock,
        category=category,
        sex=sex,
        end_date=end_date,
        latest_bid=latest_bid,
        image=image,
    )
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url="/login")
def view_listing(request, listing_id):

    """View listing individually"""

    item = listing.objects.get(id=listing_id)
    form = Add_listing(request.POST)
    user = request.user
    if request.method == "POST":
        if not form.is_valid():
            print("Error")
        new_bid = form.cleaned_data["latest_bid"]

        if new_bid <= item.latest_bid:
            return render(
                request,
                "auctions/view_listing.html",
                {
                    "item": item,
                    "message": "Your bid must be greater than previous latest bid",
                    "form": form,
                },
            )
        item.latest_bid = new_bid
        item.save()

    return render(
        request,
        "auctions/view_listing.html",
        {"item": item, "form": form, "user": user},
    )


@login_required(login_url="/login")
def watch_listing(request, user_name, listing_id):
    """Add items to watchlist and display it on site"""
    this_item = listing.objects.get(id=listing_id)
    check_added = watchList.objects.filter(watching=this_item)
    this_user = request.user

    if check_added:
        print("Added")
        check_added.delete()
    watchList.objects.create(user=this_user, watching=this_item)
    listings = watchList.objects.all()
    return render(
        request,
        "auctions/watch_list.html",
        {"user_name": user_name, "this_item": this_item, "listings": listings},
    )


@login_required(login_url="/login")
def remove_item_from_watchlist(request, user_name, listing_id):
    this_user = request.user
    this_item = listing.objects.get(id=listing_id)
    print(f"{this_item.title}")
    item_in_watchlist = watchList.objects.filter(watching=this_item)

    if this_user != this_item.user:
        item_in_watchlist.delete()
        print("Did the remove in watchList")
    else:
        this_item.delete()
        print("Did the remove in listing")
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url="/login")
def close_listing(request, listing_id):
    this_item = listing.objects.get(id=listing_id)

    if request.user == this_item.user:
        this_item.closed = True
        this_item.save()
        closed_listings = listing.objects.filter(user=request.user, closed=True)
        return render(
            request, "auctions/close_listing.html", {"closed_listings": closed_listings}
        )

    return HttpResponseRedirect(reverse("index"))


@login_required(login_url="/login")
def comments(request, listing_id):
    if request.method == "POST":
        this_comment = Comments.objects.filter(listing=listing_id)
        this_comment.content = request.POST.get("comment_text")
        this_comment.user = request.user
        this_comment.time = datetime.datetime.now()
        this_comment.listing = listing.objects.get(id=listing_id)
        Comments.objects.create(
            user=this_comment.user,
            content=this_comment.content,
            listing=this_comment.listing,
            time=this_comment.time,
        )
        all_comments = Comments.objects.filter(listing=listing_id)
        return render(
            request,
            "auctions/view_listing.html",
            {"item": this_comment.listing, "all_comments": all_comments},
        )
    return render(request, "auctions/index.html")


def category_view(request, listing_id, cgt_name):

    cgt_name = listing.objects.get(id=listing_id)
    all_listings = listing.objects.filter(category=cgt_name.category)

    return render(
        request,
        "auctions/category_view.html",
        {"all_listings": all_listings, "listing_category": cgt_name},
    )
