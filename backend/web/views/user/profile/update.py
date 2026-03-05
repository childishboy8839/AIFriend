from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.user import UserProfile
from web.views.utils.photo import remove_old_photo


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]#验证登录
    def post(self, request):
        try:
            user = request.user  #获取user
            user_profile = UserProfile.objects.get(user=user)  #数据库查询
            username = request.data.get('username').strip() #获取用户输入的信息
            profile = request.data.get('profile').strip()[:500] #取前500个字
            photo = request.FILES.get('photo', None)

            if not username: #后端判断
                return Response({
                    'result': '用户名不能为空'
                })
            if not profile:
                return Response({
                    'result': '简介不能为空'
                })
            if username != user.username and User.objects.filter(username=username).exists():
                return Response({
                    'result': '用户名已存在'
                })

            if photo:#如果传入图片，删除旧头像
                remove_old_photo(user_profile.photo)
                user_profile.photo = photo
            user_profile.profile = profile #信息更新
            user_profile.update_time = now() #记录更新时间
            user_profile.save()
            user.username = username
            user.save()
            return Response({
                'result': 'success',
                'user_id': user.id,
                'username': user.username,
                'profile': user_profile.profile,
                'photo': user_profile.photo.url,#必须返回url
            })
        except:
            return Response({
                'result': '系统异常，请稍后重试'
            })
