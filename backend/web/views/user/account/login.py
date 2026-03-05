from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from web.models.user import UserProfile


class LoginView(APIView):  #REST接口：处理用户登录请求，返回 JWT 认证信息
    def post(self, request,*args,**kwargs):
        try:
            username = request.data.get('username').strip()
            password = request.data.get('password').strip()#获取用户名和密码
            if not username or not password:  #后端校验
                return Response({
                    'result': '用户名和密码不能为空',
                })
            user=authenticate(username=username,password=password)#这是 Django 的认证函数,用来判断用户名和密码是否匹配,内部做了：查询用户，校验用户名和密码，返回用户或者None
            if user :#用户名密码正确
                user_profile=UserProfile.objects.get(user=user)
                refresh = RefreshToken.for_user(user)#生成jwt，生成refresh,用来刷新token;access,用来访问接口
                response=Response({    #返回响应
                    'result': 'success',
                    'access': str(refresh.access_token),
                    'user_id': user.id,
                    'username': user.username,
                    'photo': user_profile.photo.url,
                    'profile': user_profile.profile,
                })
                response.set_cookie(  #设置 Refresh Token Cookie  把 Refresh Token 存到浏览器的 Cookie 中。
                    key='refresh_token',
                    value=str(refresh),
                    httponly=True,
                    samesite='Lax',
                    secure=True,
                    max_age=86400*7,

                )
                return response
            else:
                return Response({
                    'result':'用户名或密码错误'
                })

        except:
            import traceback
            print(traceback.print_exc())
            return Response(
                {
                    'result':'系统异常，请稍后重试',
                }
            )