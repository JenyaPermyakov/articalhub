from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
# from django import get_object_or_404

def article_list(request):
    search_query = request.GET.get('search')
    context = {
        'search_query': search_query,
    }
    return render(request,'articles/article_list.html', context)

def article_detail(request, artical_id):
    if artical_id == 1:
        return HttpResponse(f"это страница с айди {artical_id}")

    raise Http404(f"statya not found {artical_id}")

def author_detail(request, author_id):
    search_query = request.GET.get('search')
    context = {
        'search_query': search_query,
    }

    return HttpResponse(f" это страница автора {author_id}")

def article_create(request):
    request_post = request.POST
    if request.method == "POST":
        title = request_post.get('title')
        content = request_post.get('content')
        return HttpResponse(f"poluchena statya{title}")

    return render(request,'articles/article_create.html')

