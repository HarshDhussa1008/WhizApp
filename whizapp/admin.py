from django.contrib import admin
from .models import Question,Comment,CommentImages,QuestionImages,CommentReply
from django.contrib.auth.models import User
from .views import notify
# Register your models here.

def user_notify(modeladmin, request, queryset):
    u=User.objects.all()
    for i in u:
      for q in queryset:
        notify(i,q)
    
make_published.short_description = "Notify"

class QuestionAdmin(admin.ModelAdmin):
  actions=[user_notify]

admin.site.register(Question,QuestionAdmin)
admin.site.register(QuestionImages)
admin.site.register(Comment)
admin.site.register(CommentImages)
admin.site.register(CommentReply)
