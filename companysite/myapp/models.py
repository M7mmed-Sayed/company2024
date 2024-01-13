import os
from django.urls import reverse

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy import Column, String,Integer
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserCustom(db.Model):
    __tablename__ = 'userssql'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)  # Adjust the length as needed
    password_hash = Column(String)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True)
    is_staff = db.Column(db.Boolean, default=False)


    def set_password(self, password):
        # Hash the password using passlib's pbkdf2_sha256
        self.password_hash = pbkdf2_sha256.hash(password)

    def check_password(self, password):
        # Verify the password using passlib's pbkdf2_sha256
        return pbkdf2_sha256.verify(password, self.password_hash)

class PostType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    postType = models.ForeignKey(PostType, on_delete=models.CASCADE)
    postSubject = models.CharField(max_length=255)
    postContent = models.TextField()
    postDate = models.DateField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        return self.subject


def generate_image_filename(instance, filename):
    # Generate a unique filename for the image
    base_filename, file_extension = os.path.splitext(filename)
    return f'static/images/{instance.post.id}_{instance.id}{file_extension}'


class Image(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=generate_image_filename)


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name
