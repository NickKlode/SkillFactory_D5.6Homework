from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.fields import TextField
from django.contrib.auth.forms import UserCreationForm
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.authorRating = pRat * 3 + cRat
        self.save()

        def __str__(self):
            return f'{self.authorUser.first_name}'

class Category(models.Model):
    name = models.CharField('Категории', max_length=64, unique=True)
    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, "Новость"),
        (ARTICLE, "Статья"),
    )
    categoryType = models.CharField('Тип', max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField('Поиск по дате в формате "год-месяц-день"', auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField('Заголовок', max_length=128)
    text = models.TextField('Поле для текста')
    rating = models.SmallIntegerField('Рейтинг', default=0)
    
    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return f'/news/{self.pk}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + '...'

class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

