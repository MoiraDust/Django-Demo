import json

# JsonResponse会把自己把response转换为JSON格式
from django.http import JsonResponse

from common.models import Client


def dispatcher(request):
    # 校验登陆的用户是否是mgr用户
    # 用户是否登陆:如果session中没有usertype这个值
    if 'usertype' not in request.session:
        return JsonResponse({'ret': 302, 'msg': 'not login', 'redirect': '/mgr/sign.html'}, status=302)
    if request.session['usertype'] != 'mgr':
        return JsonResponse({'ret': 302, 'msg': 'not super account', 'redirect': '/mgr/sign.html'}, status=302)
    # 增删改查的dispatcher
    if request.method == 'GET':
        request.params = request.GET
    elif request.method in ['POST', 'PUT', 'DELETE']:
        request.params = json.loads(request.body)
    action = request.params['action']
    if action == 'list_customer':
        return listcustomers(request)
    elif action == 'add_customer':
        return addcustomer(request)
    elif action == 'modify_customer':
        return modifycustomer(request)
    elif action == 'del_customer':
        return deletecustomer(request)
    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


def listcustomers(request):
    print('list customer')
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = Client.objects.values()

    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    retlist = list(qs)

    return JsonResponse({'ret': 0, 'retlist': retlist})


def addcustomer(request):
    info = request.params['data']
    # create成功后会返回这个新建的对象
    newClient = Client.objects.create(name=info['name'],
                                      phoneNumber=info['phoneNumber'],
                                      address=info['address'])
    return JsonResponse({'ret': 0, 'id': newClient.id})


def modifycustomer(request):
    uid = request.params['id']
    info = request.params['newdata']
    try:
        # 根据id找到对应的客户
        client = Client.objects.get(id=uid)
    except Client.DoesNotExist:
        return {
            'ret': 1,
            'msg': 'no client'
        }
    if 'name' in info:
        client.name = info['name']
    if 'phoneNumber' in info:
        client.phoneNumber = info['phoneNumber']
    if 'address' in info:
        client.address = info['address']
    # 执行save()才能保存到数据库
    client.save()
    return JsonResponse({"ret": 0})


def deletecustomer(request):
    uid = request.params['id']
    try:
        client = Client.objects.get(id=uid)
    except Client.DoesNotExist:
        return {
            'ret': 1,
            'msg': 'no client'
        }
    client.delete()
    return JsonResponse({'ret': 0})
