import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now, localtime


def photo_upload_to(instance, filename):
    ext = filename.split('.')[-1]#获取png
    filename = f'{uuid.uuid4().hex[:10]}.{ext}'#取随机数的前十位加png形成图片名称
    return f'user/photos/{instance.user_id}_{filename}'

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    photo=models.ImageField(default='user/photos/default.png',upload_to='photos_upload_to')
    profile=models.TextField(default='谢谢你的关注',max_length=500)
    create_time=models.DateTimeField(default=now)
    update_time=models.DateTimeField(default=now)

    def __str__(self):
        return f'{self.user.username} -{localtime(self.create_time).strftime('%Y/%m/%d %H:%M:%S')}'

