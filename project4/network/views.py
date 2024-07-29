import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse

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
def profile(request, profile):

    profile = User.objects.get(username=profile)
    following = profile.follows.all().count()
    followers = profile.followed_by.all().count()

    try:
        Follower.objects.get(follower=request.user,followee__username=profile)
        is_following = True
    except Follower.DoesNotExist:
        is_following = False
    
    return render(request, "network/profile.html", {
        "profile": profile.username,
        "following": following,
        "followers": followers,
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
def get_posts(request):
    filter = request.GET.get("filter")
    # filer posts
    if filter == "all":
        posts =  Post.objects.all()
    elif filter == "following":
        posts = Post.objects.filter(user__followed_by=request.user)
    else:
        try:
            posts = Post.objects.filter(user__username=filter)
        except:
            return JsonResponse({"error": "Invalid filter."}, status=400)
    
    posts = posts.annotate(
            likes=Count('like')
        ).order_by(
            "-timestamp"
        ).values(
            "id",
            "user__username",
            "content", 
            "timestamp",
            "likes"
        ).all()
    data = list(posts)
    return JsonResponse(data, safe=False)
    

# toggle follower status or retreive follower status   
@login_required
def follow_status(request):

    # return profile user follower count and if signed in user is a follower
    if request.method == "GET":
        profile = request.GET.get("profile")
        user = User.objects.get(username=profile)
        follower_count = user.followed_by.all().count()
        try:
            Follower.objects.get(follower=request.user,followee__username=profile)
            is_following = True
        except Follower.DoesNotExist:
            is_following = False
        return JsonResponse({
            "is_following": is_following,
            "follower_count": follower_count
            })

    # toggle if signed in user is follower or not of profile user       
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
        return JsonResponse({"message": "Follower added"}, status=201)
    else: 
        return JsonResponse({"error": "GET or POST request only."}, status=400)
    

@login_required
def like(request):
# return like count for post and if signed in user has liked it
    if request.method == "GET":
        post_id = request.GET.get("post_id")
        user = request.user
        like_count = Like.objects.filter(post_id=post_id).count()
        try:
            Like.objects.get(user=user, post_id=post_id)
            liked = True
        except Like.DoesNotExist:
            liked = False
        return JsonResponse({
            "liked": liked,
            "like_count": like_count
            })

    # toggle if signed in user likes post   
    elif request.method == "POST":
        data = json.loads(request.body)
        post = data.get("post")
        try:
            record = Like.objects.get(user=request.user,post_id=post['id'])
            record.delete()
        except Like.DoesNotExist:
            record = Like(user=request.user,post_id=post['id'])
            record.save()
        return JsonResponse({"message": "Post liked added"}, status=201)
    else: 
        return JsonResponse({"error": "GET or POST request only."}, status=400)
         
@login_required
def edit(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    edit = data.get("edit")
    post = data.get("post")
    if str(request.user) != post['user__username']:
        return JsonResponse({"error": "unauthorized."}, status=403)

    record = Post.objects.get(id=post['id'])
    record.content = edit
    record.save()

    updated_content = Post.objects.get(id=post['id']).content
    return JsonResponse({"updated_content": updated_content}, status=201)
