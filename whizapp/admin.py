from django.contrib import admin
from .models import Question,Comment,CommentImages,QuestionImages,CommentReply
# Register your models here.

admin.site.register(Question)
admin.site.register(QuestionImages)
admin.site.register(Comment)
admin.site.register(CommentImages)
admin.site.register(CommentReply)