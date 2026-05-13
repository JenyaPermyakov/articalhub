from django.db import migrations


CATEGORIES = [
    'Новости',
    'Технологии',
    'Наука',
    'Бизнес',
    'Образование',
    'Культура',
]


def create_categories(apps, schema_editor):
    Category = apps.get_model('articles', 'Category')
    for name in CATEGORIES:
        Category.objects.get_or_create(name=name)


def remove_empty_seed_categories(apps, schema_editor):
    Category = apps.get_model('articles', 'Category')
    for name in CATEGORIES:
        Category.objects.filter(name=name, articles__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_alter_category_options_alter_article_author'),
    ]

    operations = [
        migrations.RunPython(create_categories, remove_empty_seed_categories),
    ]
