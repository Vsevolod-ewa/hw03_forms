from django.core.paginator import Paginator

from posts.constants import MAX_POST


def make_paginator(posts, request):
    ''' Принимает список постов, возвращает пронумерованный спиок.'''
    paginator = Paginator(posts, MAX_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj
