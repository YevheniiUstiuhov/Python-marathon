from django.db import models
from django.forms.models import model_to_dict


class Author(models.Model):
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)

    def __str__(self):
        return f"'id': {self.pk}, 'name': '{self.name}', 'surname': '{self.surname}', 'patronymic': '{self.patronymic}'"

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.pk})"

    @staticmethod
    def get_by_id(author_id):
        try:
            return Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(author_id):
        try:
            author = Author.objects.get(id=author_id)

            if author:
                author.delete()
                return True
            return False
        except:
            print(f"Author with id {author_id} not found")

    @staticmethod
    def create(name=None, surname=None, patronymic=None):
        if len(name) > 20 or len(surname) > 20 or len(patronymic) > 20:
            return None
        try:
            return Author.objects.create(name=name, surname=surname, patronymic=patronymic)
        except ValueError:
            return None

    def to_dict(self):
        return model_to_dict(self)

    def update(self,
               name=None,
               surname=None,
               patronymic=None):

        if name is not None and len(name) > 20:
            return False

        if name is not None:
            self.name = name
        if surname is not None:
            self.surname = surname
        if patronymic is not None:
            self.patronymic = patronymic
        self.save()

    @staticmethod
    def get_all():
        return Author.objects.all()

