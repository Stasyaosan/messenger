from django.db import models
from datetime import datetime


class User(models.Model):
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(default='')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/default.png')
    created_date = models.DateTimeField(auto_now=True)
    token = models.TextField(null=True, blank=True)
    suc = models.IntegerField(default=0)
    update_date = models.DateTimeField(auto_now=True)
    token_api = models.CharField(max_length=100, default=None)


class Group_chat(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    users = models.ManyToManyField(User, related_name='users')
    avatar = models.ImageField(upload_to='avatars_chat/', default='avatars_chat/default.png')
    created_date = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator', default=None)


class Message(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Group_chat, on_delete=models.CASCADE, default=None)
    file = models.FileField(upload_to='files/', blank=True, null=True)
    datetime = models.DateTimeField(auto_now=True)
