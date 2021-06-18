from django.contrib import admin
from .models import Question,Comment,CommentImages,QuestionImages,CommentReply
from django.contrib.auth.models import User
from .views import notify
# Register your models here.

def user_notify(modeladmin, request, queryset):
    u=User.objects.all()
    for i in u:
        if i.is_staff:
            notify(i,queryset)
    
user_notify.short_description = "Notify"

class QuestionAdmin(admin.ModelAdmin):
  actions=[user_notify]

admin.site.register(Question,QuestionAdmin)
admin.site.register(QuestionImages)
admin.site.register(Comment)
admin.site.register(CommentImages)
admin.site.register(CommentReply)
