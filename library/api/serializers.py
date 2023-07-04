from rest_framework import serializers
from book.models import Book
from author.models import Author
from order.models import Order

class BookNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['name']

class AuthorSerializer(serializers.ModelSerializer):
    books = BookNameSerializer(many=True)

    class Meta:
        model = Author
        fields = '__all__'

        
class BookSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()  
    def get_authors(self, obj):
        return [f"{author.name} {author.surname}" for author in obj.authors.all()]
    class Meta:
        model = Book
        fields = ['id', 'name','description','count', 'authors']


class OrderSerializer(serializers.ModelSerializer):
    # book = BookNameSerializer(many=True)
    class Meta:
        model = Order
        fields = '__all__'

    
