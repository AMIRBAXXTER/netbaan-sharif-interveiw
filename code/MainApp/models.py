from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    username = models.CharField(max_length=11, unique=True, verbose_name='نام کاربری')

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
        db_table = 'users'


class Books(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    author = models.CharField(max_length=100, verbose_name='نویسنده')
    genre = models.CharField(max_length=100, verbose_name='ژانر')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب ها'
        db_table = 'books'


class Reviews(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='کاربر')
    book = models.ForeignKey(Books, on_delete=models.CASCADE, verbose_name='کتاب')
    rating = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='امتیاز')

    def __str__(self):
        return f'{self.user.username} - {self.book.title} => {self.rating}'

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
        db_table = 'reviews'
