from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse


def signin(request):
    print('using signin function')
    userName = request.POST.get("username")
    passWord = request.POST.get("password")

    print(userName, passWord)
    # 使用Django auth库里面的方法进行用户名密码校验
    user = authenticate(username=userName, password=passWord)

    # 如果找到了用户并且密码正确
    if user is not None:
        # 用户已经激活
        if user.is_active:
            # 用户是超级管理员
            if user.is_superuser:
                login(request, user)
                # 把用户的类型存入session
                request.session['usertype'] = 'mgr'
                return JsonResponse({'ret': 0})
            # 如果不是管理员
            else:
                return JsonResponse({'ret': 1, 'msg': 'please use manager account to log in'})
        # 账号没被激活
        else:
            return JsonResponse({'ret': 0, 'msg': 'The account is banded'})
    else:
        return JsonResponse({'ret': 0, 'msg': 'wrong account information'})


def signout(request):
    # 直接调用logout方法
    logout(request)
    return JsonResponse({'ret': 0})
