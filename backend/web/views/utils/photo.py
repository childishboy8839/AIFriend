import os

from django.conf import settings

#用户上传新头像时删除旧头像
def remove_old_photo(photo):
    if photo and photo.name != 'user/photos/default.png':#不是默认头像，进行删除
        old_path = settings.MEDIA_ROOT / photo.name #构造旧图片的路径
        if os.path.exists(old_path):#如果旧图片存在，则删除
            os.remove(old_path)
