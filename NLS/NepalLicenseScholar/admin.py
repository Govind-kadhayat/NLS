from django.contrib import admin
from .models import *

admin.site.register(Contact)
admin.site.register(Category)
class AnserAdmin(admin.StackedInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnserAdmin]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)