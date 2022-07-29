from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from .models import Group, Post, User
from .forms import PostForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Отдаем в словаре контекста
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).select_related('group',)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'group': group,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts_count = Post.objects.filter(author=author).count()
    posts = author.author.select_related('group', 'author')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'page_obj': page_obj,
        'posts_count': posts_count,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    # Страница для просмотра одного поста
    # Здесь код запроса к модели и создание словаря контекста
    # В пост выведен один пост, выбранный по pk
    post = get_object_or_404(Post, pk=post_id)
    # Выведено общее количество постов пользователя
    posts_count = Post.objects.filter(author=post.author).count()
    # В тег <title> выведен текст Пост < Первые 30 символов поста>
    context = {'post': post, 'posts_count': posts_count, }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
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
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post_detail', post.id)
    form = PostForm(instance=post)
    return render(request, 'posts/create_post.html', {'form': form,
                                                      'is_edit': True})
