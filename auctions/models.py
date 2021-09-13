from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE


class User(AbstractUser):
    pass


class Gender(models.Model):
    this_gender = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.this_gender}"


class category(models.Model):
    category_name = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.category_name}"


class listing(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    title = models.CharField(max_length=64)
    stock = models.IntegerField()
    description = models.TextField(max_length=240)
    latest_bid = models.DecimalField(max_digits=9, decimal_places=2)
    sex = models.ForeignKey(Gender, on_delete=CASCADE, related_name="Sex")
    category = models.ForeignKey(category, on_delete=CASCADE, related_name="category")
    end_date = models.DateTimeField(null=True, blank=True)
    closed = models.BooleanField(default=False)
    image = models.ImageField(upload_to="images", null=True, blank=True)

    def __str__(self) -> str:
        return f" Listing_ID: {self.id} Name: {self.user} is selling {self.title} with {self.stock} in stock. {self.latest_bid} is the bid"


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=240)
    listing = models.ForeignKey(
        listing, on_delete=CASCADE, related_name="comment_listing", default=""
    )

    def __str__(self) -> str:
        return f"{self.user} commented at {self.time}"


class watchList(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    watching = models.ForeignKey(
        listing, on_delete=CASCADE, related_name="watched_listing", default=""
    )

    def __str__(self) -> str:
        return f"{self.user} watching item {self.watching}"
