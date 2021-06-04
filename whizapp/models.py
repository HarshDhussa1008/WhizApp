import time
from django.db import models
from datetime import datetime

# Create your models here.
from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.post.user.id, filename+time.strftime("%Y%m%d-%H%M%S"))


class Question(models.Model):
    qid=models.AutoField(primary_key=True)
    title=models.TextField()
    description=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)
    status=models.CharField(default='Pending',max_length=50)

    def __str__(self):
        return self.title


class Comment(models.Model):
    cid=models.AutoField(primary_key=True)
    qid=models.ForeignKey(Question,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.qid.title


class QuestionImages(models.Model):
    post = models.ForeignKey(Question,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path)

    def __str__(self):
        return self.post.title


class CommentImages(models.Model):
    post = models.ForeignKey(Comment,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path)

    def __str__(self):
        return self.post.qid.title

class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment.qid.title

