import json

from django.http import JsonResponse

from common.models import Medicine


def dispatcher(request):
    if 'usertype' not in request.session:
        return JsonResponse({
            'ret': '302',
            'msg': 'no login user',
            'redirect': '/mgr.signin.html',
        }, status=302)
    if request.session['usertype'] != 'mgr':
        return JsonResponse({
            'ret': '302',
            'msg': 'you are not manager',
            'redirect': '/mgr.signin.html',
        }, status=302)
    # 获取GET参数
    if request.method == 'GET':
        request.params = request.GET
    #    获取PUT，POST，DELETE请求体里面的参数，使用json格式
    elif request.method in ['PUT', 'POST', 'DELETE']:
        request.params = json.loads(request.body)
    # 然后从request.params里面取出action的值
    action = request.params['action']
    # 根据action的不同的值分派给不同的函数
    if action == 'list_medicine':
        return listmedicine(request)
    if action == 'add_medicine':
        return addmedicine(request)
    if action == 'modify_medicine':
        return modifymedicine(request)
    if action == 'del_medicine':
        return deletemedicine(request)
    else:
        return JsonResponse({'ret': 1, 'msg': 'no such a query'})


def listmedicine(request):
    qs = Medicine.objects.values()
    # 转换为list类型
    relist = list(qs)
    return JsonResponse({'ret': 0, 'relist': relist})


def addmedicine(request):
    info = request.params['data']
    medicine = Medicine.objects.create(
        name=info['name'],
        sn=info['sn'],
        desc=info['desc']
    )
    return JsonResponse({'ret': 0, 'id': medicine.id})


def modifymedicine(request):
    medicineid = request.params['id']
    newdata = request.params['newdata']
    try:
        # 找到这个药品通过id
        medicine = Medicine.objects.get(id=medicineid)
    except Medicine.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id `{medicineid}` not in the database'
        }
    if 'name' in newdata:
        medicine.name = newdata['name']
    if 'sn' in newdata:
        medicine.sn = newdata['sn']
    if 'desc' in newdata:
        medicine.desc = newdata['desc']
    # have to save
    medicine.save()
    return JsonResponse({'ret': 0})


def deletemedicine(request):
    medicineid = request.params['id']
    try:
        medicine = Medicine.objects.get(id=medicineid)
    except Medicine.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'no `{medicineid}` in database'
        }
    medicine.delete()
    return JsonResponse({'ret': 0})
