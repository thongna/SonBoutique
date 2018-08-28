from django.contrib import admin
from .models import Contact, QuestionType, Question, Messages

# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone_number']
    search_fields = ['name']

@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'answer', 'created']
    search_fields = ['name', 'title']

@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'name', 'phone_number', 'created', 'readed']
    search_fields = ['name', 'title']
    list_editable = ['readed']