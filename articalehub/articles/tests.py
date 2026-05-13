from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Article, Category


class ArticleViewTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='author', password='StrongPass123')
        self.other_user = User.objects.create_user(username='reader', password='StrongPass123')
        self.category = Category.objects.create(name='Django')

    def create_article(self, title='Article title', author=None, is_published=True):
        article = Article.objects.create(
            title=title,
            content='Article content',
            author=author or self.author,
            is_published=is_published,
        )
        article.categories.add(self.category)
        return article

    def test_article_list_renders_for_anonymous_users(self):
        article = self.create_article(title='Public article')

        response = self.client.get(reverse('article_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, article.title)
        self.assertContains(response, reverse('login'))

    def test_article_list_hides_drafts_from_anonymous_users(self):
        draft = self.create_article(title='Private draft', is_published=False)

        response = self.client.get(reverse('article_list'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, draft.title)

    def test_article_list_shows_current_users_drafts(self):
        draft = self.create_article(title='My draft', is_published=False)
        self.client.login(username='author', password='StrongPass123')

        response = self.client.get(reverse('article_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, draft.title)

    def test_article_detail_hides_draft_from_other_users(self):
        draft = self.create_article(title='Hidden draft', is_published=False)
        self.client.login(username='reader', password='StrongPass123')

        response = self.client.get(reverse('article_detail', args=[draft.pk]))

        self.assertEqual(response.status_code, 404)

    def test_article_create_requires_login(self):
        response = self.client.get(reverse('article_create'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response['Location'])

    def test_author_can_edit_own_article(self):
        article = self.create_article(title='Old title')
        self.client.login(username='author', password='StrongPass123')

        response = self.client.post(
            reverse('article_edit', args=[article.pk]),
            {
                'title': 'New title',
                'content': article.content,
                'is_published': 'on',
                'categories': [self.category.pk],
            },
        )

        article.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(article.title, 'New title')

    def test_other_user_cannot_edit_article(self):
        article = self.create_article()
        self.client.login(username='reader', password='StrongPass123')

        response = self.client.get(reverse('article_edit', args=[article.pk]))

        self.assertEqual(response.status_code, 404)


class CategorySeedTests(TestCase):
    def test_default_categories_exist(self):
        expected_categories = {
            'Новости',
            'Технологии',
            'Наука',
            'Бизнес',
            'Образование',
            'Культура',
        }

        existing_categories = set(Category.objects.values_list('name', flat=True))

        self.assertTrue(expected_categories.issubset(existing_categories))
