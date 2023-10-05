import csv

from django.conf import settings
from django.core.management import BaseCommand
from django.db.utils import IntegrityError

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

TABLES = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for model, csv_f in TABLES.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{csv_f}',
                'r',
                encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                for data in reader:
                    try:
                        if model == Title:
                            category_id = data.pop('category')
                            category = Category.objects.get(pk=category_id)
                            data['category'] = category
                        if model == Review:
                            author_id = data.pop('author')
                            author = User.objects.get(pk=author_id)
                            data['author'] = author
                        if model == Comment:
                            author_id = data.pop('author')
                            author = User.objects.get(pk=author_id)
                            data['author'] = author
                            model.objects.create(**data)
                    except IntegrityError:
                        self.stdout.write(self.style.WARNING(
                            'Запись уже существует'))
        self.stdout.write(self.style.SUCCESS('Данные загружены'))
