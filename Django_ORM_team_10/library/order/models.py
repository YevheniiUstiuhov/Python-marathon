from django.db import models
from authentication.models import CustomUser
from book.models import Book
import datetime

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(null=True, blank=True)
    plated_end_at = models.DateTimeField()
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True,null=True, default=None)
    # book = models.ForeignKey(Book, on_delete=models.CASCADE,blank=True,null=True, default=None)
    # plated_end_at = models.DateTimeField(blank=True,null=True, default=None)
    # end_at = models.DateTimeField(blank=True,null=True, default=None)
    # created_at = models.DateTimeField(blank=True,null=True)
    

    def __str__(self):
        """
        Magic method is redefined to show all information about Order.
        :return: book id, book name, book description, book count, book authors
        """
        end_at = f"'{self.end_at}'" if self.end_at else "None"

        return f"'id': {self.id}, " \
               f"'user': {self.user.__class__.__name__}(id={self.user.id}), " \
               f"'book': {self.book.__class__.__name__}(id={self.book.id}), " \
               f"'created_at': '{self.created_at}', " \
               f"'end_at': {end_at}, " \
               f"'plated_end_at': " \
               f"'{self.plated_end_at}'"

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Order object.
        :return: class, id
        """
        return f'{self.__class__.__name__}(id={self.id})'

    def to_dict(self):
        """
        :return: dict contains order id, book id, user id, order created_at, order end_at, order plated_end_at
        :Example:
        | {
        |   'id': 8,
        |   'book': 8,
        |   'user': 8',
        |   'created_at': 1509393504,
        |   'end_at': 1509393504,
        |   'plated_end_at': 1509402866,
        | }
        """
        order_dict = {
            'id': self.id,
            'book': self.book.id,
            'user': self.user.id,
            'created_at': int(self.created_at.timestamp()),
            'end_at': int(self.end_at.timestamp()),
            'plated_end_at': int(self.plated_end_at.timestamp()),
        }
        return order_dict

    @staticmethod
    def create(user, book, plated_end_at):
        """
        :param user: the user who took the book
        :type user: CustomUser
        :param book: the book they took
        :type book: Book
        :param plated_end_at: planned return of data
        :type plated_end_at: int (timestamp)
        :return: a new order object which is also written into the DB
        """

        if not user.id:
            return None
        if book.count > 1:
            order = Order(user=user, book=book, plated_end_at=plated_end_at)
            order.save()
            return order
        else:
            return None


    @staticmethod
    def get_by_id(order_id):
        """
        :param order_id:
        :type order_id: int
        :return:  the object of the order, according to the specified id or null in case of its absence
        """
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None


    def update(self, plated_end_at=None, end_at=None):
        """
        Updates order in the database with the specified parameters.\n
        :param plated_end_at: new plated_end_at
        :type plated_end_at: int (timestamp)
        :param end_at: new end_at
        :type plated_end_at: int (timestamp)
        :return: None
        """
        if plated_end_at:
            self.plated_end_at = plated_end_at
        if end_at:
            self.end_at = end_at
        self.save()

    @staticmethod
    def get_all():
        """
        :return: all orders
        """
        queryset = list(Order.objects.all())
        return queryset

    @staticmethod
    def get_not_returned_books():
        """
        :return:  all orders that do not have a return date (end_at)
        """
        # not_returned = []
        # orders = Order.get_all()
        # for order in orders:
        #     if Order.objects.filter(end_at=None):
        #         not_returned.append(order)
        return list(Order.objects.filter(end_at = None))


    @staticmethod
    def delete_by_id(order_id):
        """
        :param order_id: an id of a user to be deleted
        :type order_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        get_by = Order.get_by_id(order_id)
        if get_by == None:
            return False
        Order.objects.filter(id = order_id).delete()
        return True
