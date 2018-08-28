from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    skype = models.CharField(max_length=30, null=True, blank=True)
    businesshour = models.CharField(max_length=50, blank=True)

class QuestionType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Question(models.Model):
    name = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    answer = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created',]

class Messages(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(null=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, null=True)
    created = models.DateTimeField(auto_now_add=True)
    readed = models.BooleanField(default=False)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return 'Comment by {} with title "{}"'.format(self.name, self.title)