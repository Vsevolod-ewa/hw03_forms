from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .utils import pagination
from .models import Group, Post, User
from .forms import PostForm


def index(request):
    posts = Post.objects.all()
    page_obj = pagination(posts, request)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).select_related('group',)
    page_obj = pagination(posts, request)
    context = {
        'page_obj': page_obj,
        'group': group,
    }

    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts_count = Post.objects.filter(author=author)
    posts = author.author.select_related('group', 'author')
    page_obj = pagination(posts, request)
    context = {
        'author': author,
        'page_obj': page_obj,
        'posts_count': posts_count,
    }

    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    '''Страница для просмотра одного поста'''
    post = get_object_or_404(Post, pk=post_id)
    # Выведено общее количество постов пользователя
    posts_count = Post.objects.filter(author=post.author)
    # В тег <title> выведен текст Пост < Первые 30 символов поста>
    context = {'post': post, 'posts_count': posts_count, }

    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    form = PostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=post.author)
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    '''Это представление редактирует запись по ее идентификатору
   и сохраняет изменения в базе данных.'''

    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST, instance=post)
    if request.method == "POST":
        if post.author == request.user:
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('posts:post_detail', post.id)
    form = PostForm(instance=post)
    return render(request, 'posts/create_post.html', {'form': form,
                                                      'is_edit': True,
                                                      'post': post, })
