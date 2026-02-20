from django.shortcuts import render
from django.http import HttpResponse

def article_list(request):
    return render(request,'articles/article_list.html')

def article_detail(request, artical_id):
    return HttpResponse(f"это страница с айди {artical_id}")


def author_detail(request, author_id):
    return HttpResponse(f" это страница автора {author_id}")

