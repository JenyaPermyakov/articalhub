from django import forms
from articles.models import Article, Author



class ArticleModelForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'is_published', 'categories']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }