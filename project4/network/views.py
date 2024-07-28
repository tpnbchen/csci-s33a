import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView

from .models import User, Post, Like, Follower


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    

# display user profile
def profile(request, username):

    user = User.objects.get(username=username)
    following = user.followees.all().count()
    followers = user.followers.all().count()
    posts = get_posts(request, username)
    try:
        Follower.objects.get(followee=request.user,follower__username=profile)
        is_following = True
    except Follower.DoesNotExist:
        is_following = False
    
    return render(request, "network/profile.html", {
        "profile": user.username,
        "following": following,
        "followers": followers,
        "posts": posts,
        "is_following": is_following
    })


# submit new post
@login_required
def post(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    content = data.get("content","")
    post = Post(
        user = request.user,
        content = content
    )

    post.save()

    return JsonResponse({"message": "Post submitted successfully."}, status=201)


# return posts
def get_posts(request, filter):

    # filer posts
    if filter == "all":
        posts = Post.objects.all()
    elif filter == "following":
        posts = Post.objects.filter(user__followers=request.user)
    else:
        try:
            posts = Post.objects.filter(user__username=filter)
        except:
            print(filter+" user not found")
            return JsonResponse({"error": "Invalid filter."}, status=400)
    
    posts = posts.order_by("-timestamp").all()

    return posts

    # paginator = Paginator(posts, 10)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    
    # return render(request, 'network/page.html', {'page_obj': page_obj})
    

# toggle follower status or retreive follower status   
@login_required
def follow_status(request):

    if request.method == "GET":
        profile = request.GET.get("profile")
        try:
            Follower.objects.get(follower=request.user,followee__username=profile)
            is_following = True
        except Follower.DoesNotExist:
            is_following = False
        print("GET")
        return JsonResponse({"is_following": is_following})        
    elif request.method == "POST":
        data = json.loads(request.body)
        profile = data.get("profile")
        try:
            record = Follower.objects.get(follower=request.user,followee__username=profile)
            record.delete()
        except Follower.DoesNotExist:
            followee = User.objects.get(username=profile)
            record = Follower(follower=request.user,followee=followee)
            record.save()
        print("POST")
        return JsonResponse({"message": "Follower added"}, status=201)
    else: 
        return JsonResponse({"error": "GET or POST request only."}, status=400)
        

        

