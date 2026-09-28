from django.db import models


class Student(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30)
    home_country = models.CharField(max_length=100)
    campus_city = models.CharField(max_length=100)
    course = models.CharField(max_length=120)
    cardId = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    card_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.firstName} {self.lastName}'