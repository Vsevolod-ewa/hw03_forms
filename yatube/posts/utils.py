from django.core.paginator import Paginator
from posts.constants import MAX_POST


def pagination(posts, request):
    paginator = Paginator(posts, MAX_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
