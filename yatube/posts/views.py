from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
from .models import Post, Group
from django.contrib.auth import get_user_model
from .forms import PostForm


LIMIT_POST = 10
User = get_user_model()


def index(request):
    posts = Post.objects.all()
    post_list = Post.objects.order_by('-pub_date')
    paginator = Paginator(post_list, LIMIT_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'posts': posts
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(posts, LIMIT_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'posts': posts,
        'page_obj': page_obj
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author)
    paginator = Paginator(posts, LIMIT_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    post_count = posts.count()
    context = {
        'post_count': post_count,
        'posts': posts,
        'author': author,
        'page_obj': page_obj
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    user = get_object_or_404(User, username=post.author)
    post_number = Post.objects.filter(author=user).count()
    context = {
        'post': post,
        'post_number': post_number
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    user = request.user
    groups = Group.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = user
            post.save()
            return redirect(reverse('posts:profile',
                                    kwargs={'username': user.username}))
    context = {
        'form': PostForm(),
        'groups': groups,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    user = request.user
    groups = Group.objects.all()
    post = Post.objects.get(id=post_id)
    if user != post.author:
        raise HttpResponseNotFound("У вас нет такого поста")
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post.id)
    form = PostForm(instance=post)
    context = {
        'form': form,
        'groups': groups,
        'is_edit': True,
    }
    return render(request, 'posts/create_post.html', context)
