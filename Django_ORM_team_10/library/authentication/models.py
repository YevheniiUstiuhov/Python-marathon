from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


ROLE_CHOICES = (
    (0, 'visitor'),
    (1, 'admin'),
)


class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"'id': {self.pk}, " \
               f"'first_name': '{self.first_name}', " \
               f"'middle_name': '{self.middle_name}', " \
               f"'last_name': '{self.last_name}', " \
               f"'email': '{self.email}', " \
               f"'created_at': {int(self.created_at.timestamp())}, " \
               f"'updated_at': {int(self.updated_at.timestamp())}, " \
               f"'role': {self.role}, " \
               f"'is_active': {self.is_active}"

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.pk})'

    @staticmethod
    def get_by_id(user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def get_by_email(email):
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(user_id):
        try:
            user = CustomUser.objects.get(id=user_id)

            if user:
                user.delete()
                return True
            return False
        except:
            print(f"User with id {user_id} not found")

    @staticmethod
    def create(email, password, first_name=None, middle_name=None, last_name=None):
        if len(first_name) > 20 or len(middle_name) > 20 or len(last_name) > 20:
            return None
        if not email or '@' not in email:
            return None
        try:
            CustomUser.objects.get(email=email)
            return None
        except CustomUser.DoesNotExist:
            user = CustomUser(email=email, password=password, first_name=first_name, middle_name=middle_name,
                              last_name=last_name)
            user.save()
            return user

    def to_dict(self):

        return {
            'id': self.id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': int(self.created_at.timestamp()),
            'updated_at': int(self.updated_at.timestamp()),
            'role': self.role,
            'is_active': self.is_active,
        }

    def update(self,
               first_name=None,
               last_name=None,
               middle_name=None,
               password=None,
               role=None,
               is_active=None):

        if first_name is not None:
            self.first_name = first_name
        if middle_name is not None:
            self.middle_name = middle_name
        if last_name is not None:
            self.last_name = last_name
        if password is not None:
            self.password = password
        if role is not None:
            self.role = role
        if is_active is not None:
            self.is_active = is_active
        self.save()

    @staticmethod
    def get_all():
        return CustomUser.objects.all()

    def get_role_name(self):
        for choice in ROLE_CHOICES:
            if choice[0] == self.role:
                return choice[1]

        return 'Unknown Role'
