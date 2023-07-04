import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library.settings")
django.setup()

from book.models import Book
from author.models import Author

###
b1 = Book.create(name="Easy Cook", description="vmfjv sdfv ssdf sfsd", count=6)
b1.save()

b2 = Book.create(name="Good Luck", description="norm", count=67)
b2.save()

b3 = Book.create(name="Some Book", description="fdfv lnjk jhkkjkuijiy hgj gg bb",)
b3.save()

a1 = Author.create(name="E", surname="M", patronymic="S")
a1.save()
a1.books.add(b1, b2)

a2 = Author.create(name="unnamed", surname="Smith", patronymic="J")
a2.save()
a2.books.add(b3)
