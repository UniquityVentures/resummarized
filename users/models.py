from django.db import models
from pgvector.django import CosineDistance
from django.db.models import Avg
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone = models.CharField("Phone number", max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone"]

    objects = UserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name

    def for_you(self):
        from articles.models import Article
        user_preference = (
            self.article_history.all()
            .values("article__vector")
            .aggregate(Avg("article__vector__vector"))
        )
        print(user_preference)

        user_preference_vector = (
            user_preference["article__vector__vector__avg"]
            if user_preference["article__vector__vector__avg"]
            else [0] * 768
        )

        return Article.objects.all().order_by(
            CosineDistance("vector__vector", user_preference_vector)
        )

