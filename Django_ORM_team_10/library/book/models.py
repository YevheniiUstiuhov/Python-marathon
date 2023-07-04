from django.db import models
from author.models import Author
from django.http import JsonResponse
from django.core import serializers


class Book(models.Model):
    """
        This class represents an Book. \n
        Attributes:
        -----------
        param name: Describes name of the book
        type name: str max_length=128
        param description: Describes description of the book
        type description: str
        param count: Describes count of the book
        type count: int default=10
        param authors: list of Authors
        type authors: list->Author
    """

    name = models.CharField(blank = True,max_length=128)
    description = models.CharField(blank = True,max_length=200)
    count = models.IntegerField(blank = True,default=10)
    authors = models.ManyToManyField(Author,blank=True,null=True, default=None)



    def __str__(self):
        """
        Magic method is redefined to show all information about Book.
        :return: book id, book name, book description, book count, book authors
        """
        return f"'id': {self.pk}, 'name': '{self.name}', 'description': '{self.description}', 'count': {self.count}, 'authors': {list(self.authors.values_list('id', flat=True))}"


    def __repr__(self):
        """
        This magic method is redefined to show class and id of Book object.
        :return: class, id
        """
        return f'{self.__class__.__name__}(id={self.id})'

    @staticmethod
    def get_by_id(book_id):
        """
        :param book_id: SERIAL: the id of a Book to be found in the DB
        :return: book object or None if a book with such ID does not exist
        """
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(book_id):
        """
        :param book_id: an id of a book to be deleted
        :type book_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        try:
            book = Book.objects.get(id=book_id)
            if book:
                book.delete()
                return True
            return False
        except:
            print(f"Book with id {book_id} not found")
        

    @staticmethod
    def create(name, description, count=10, authors=None):
        """
        param name: Describes name of the book
        type name: str max_length=128
        param description: Describes description of the book
        type description: str
        param count: Describes count of the book
        type count: int default=10
        param authors: list of Authors
        type authors: list->Author
        :return: a new book object which is also written into the DB
        """
        if len(name) > 128 or len(name) <=0:
            return None       
        if type(description) != str or type(count) != int or type(name) !=str:
            return None
        book = Book.objects.create(name=name, description=description, count=count)
        book.save()
        if authors:
            book.authors.set(authors)
            book.save()
        return book



    def to_dict(self):
        """
        :return: book id, book name, book description, book count, book authors
        :Example:
        | {
        |   'id': 8,
        |   'name': 'django book',
        |   'description': 'bla bla bla',
        |   'count': 10',
        |   'authors': []
        | }
        """
        book_dict = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'count': self.count,
            'authors': self.authors,
        }
        return book_dict

    def update(self, name=None, description=None, count=None):
        """
        Updates book in the database with the specified parameters.\n
        param name: Describes name of the book
        type name: str max_length=128
        param description: Describes description of the book
        type description: str
        param count: Describes count of the book
        type count: int default=10
        :return: None
        """
        if name:
            self.name = name
        if description:
            self.description = description
        if count:
            self.count = count
        self.save()
        



    def add_authors(self, authors):
        """
        Add  authors to  book in the database with the specified parameters.\n
        param authors: list authors
        :return: None
        """
        try:
            book = Book.objects.get(name = self.name)
            for a in authors:
                book.authors.add(a)
            book.save()
        except Book.DoesNotExist:
            return None
        


    def remove_authors(self, authors):
        """
        Remove authors to  book in the database with the specified parameters.\n
        param authors: list authors
        :return: None
        """
        try:
            self.authors.remove(*authors)
        except Book.DoesNotExist:
            return None
        
    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all books
        """
        return list(Book.objects.all())