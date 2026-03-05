from idlelib import query

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ArticleModelForm
from .models import Author, Article

from django.contrib.auth.models import User


@login_required
def article_create(request):

    if request.method == 'POST':
        form = ArticleModelForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user

            article.save()
            form.save_m2m()

            return redirect('article_list')

    else:
        form = ArticleModelForm()

    return render(request, 'articles/article_create.html', {'form': form, 'title': 'создать статью'})


def article_list(request):
    query = request.GET.get('q')

    articles = Article.objects.all()
    if query:
        articles = articles.filter(title__icontains=query)

    return render(request, 'articles/article_list.html', {'articles': articles})


def article_detail(request, pk):
    article = get_object_or_404(Article, id=pk)

    return render(
        request,
        'articles/article_details.html',
        context={'article': article}
    )

@login_required
def article_edit(request, pk):
    article = get_object_or_404(Article, id=pk, author=request.user)

    if request.method == 'POST':
        form = ArticleModelForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_list')

    else:
        form = ArticleModelForm(instance=article)

    return render(request, 'articles/article_create.html', {'form': form, 'title': 'редактировать статью'})

@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, id=pk, author=request.user)

    if request.method == 'POST':
        article.delete()
        return redirect('article_list')

    return render(
        request,
        'articles/article_confirm_delete.html',
        {'article': article})
