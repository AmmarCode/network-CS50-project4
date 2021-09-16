import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Following, Post


def index(request):
    posts = Post.objects.order_by('-date')

    post_paginator = Paginator(posts, 10)

    page_num = request.GET.get('page')

    page = post_paginator.get_page(page_num)

    return render(request, "network/index.html", {
        "page": page
    })


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


@login_required
def create_post(request):
    if request.method == "POST":
        content = request.POST.get('content')
        author = request.user

        post = Post(content=content, author=author)

        post.save()

        return HttpResponseRedirect(reverse("index"))
    return render(request, "network/index.html")


@csrf_exempt
@login_required
def edit_post(request, post_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.method == "POST":
        request_body = json.loads(request.body)
        content = request_body['content']

        post = Post.objects.get(pk=post_id)
        if request.user != post.author:
            return JsonResponse({
                "message": "You can only edit your own posts",
                "content": post.content
            })

        post.content = content
        post.save()

    return JsonResponse({
        "message": "Post updated successfully.",
        "content": post.content
    })


@csrf_exempt
@ login_required
def like_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = request.user
    if user not in post.like.all():
        post.like.add(user)
        post.like_status = True
    else:
        post.like.remove(user)
        post.like_status = False

    post.save()
    likes = post.like.all()
    likes_serialized = json.loads(serialize('json', likes))

    return JsonResponse({
        "user": user.username,
        "postId": post_id,
        "likeStatus": post.like_status,
        "likeList": likes_serialized,
        "likeCount": post.like.count(),
    }, status=200)


@login_required
def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    following_num = user.followers.count()
    followers_num = user.followed_users.count()
    posts = Post.objects.filter(author=user_id).order_by('-date')

    following = request.user.followers.filter(followed_id=user.id).exists()

    post_paginator = Paginator(posts, 10)

    page_num = request.GET.get('page')

    page = post_paginator.get_page(page_num)

    return render(request, 'network/profile.html', {
        "profile_user": user,
        "followers": followers_num,
        "followings": following_num,
        "already_following": following,
        "posts": posts,
        "page": page,
    })


@csrf_exempt
@login_required
def follow(request, user_id):
    recieving_user = User.objects.get(pk=user_id)
    acting_user = request.user
    try:
        found = Following.objects.get(
            followed=recieving_user, follower=acting_user)
        if found:
            found.delete()
            message = "deleted"

    except Exception as e:
        print(e)
        new = Following(followed=recieving_user, follower=acting_user)
        new.save()
        message = "added"

    return JsonResponse({
        "message": message,
        "followers": recieving_user.followed_users.count(),
        "following": recieving_user.followers.count(),
    })


@csrf_exempt
@login_required
def following(request):
    user = request.user
    following_list = user.followers.all()

    followed = [follow.followed for follow in following_list]
    posts = Post.objects.filter(author__in=followed).order_by('-date')

    post_paginator = Paginator(posts, 10)

    page_num = request.GET.get('page')

    page = post_paginator.get_page(page_num)

    return render(request, 'network/following.html', {
        "page": page
    })
