from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.
class ExpenseType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Expenses(models.Model):
    name = models.ForeignKey(ExpenseType, on_delete=models.CASCADE)
    month = models.DateField(default=datetime.date.today)
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    note = models.TextField(blank=True, null=True)
    create_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('-month',)

    def __str__(self):
        return self.name.name