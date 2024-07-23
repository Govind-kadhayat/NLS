from django.contrib import admin


# Register your models here.
from .models import *

admin.site.register(Contact)
admin.site.register(Signup)
admin.site.register(Category)
class AnserAdmin(admin.StackedInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnserAdmin]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)