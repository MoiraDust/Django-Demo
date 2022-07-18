from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
# 首先导入model
from common.models import Client


# http://localhost/sales/orders
def listorders(request):
    return HttpResponse("下面是系统中所有的订单信息。。。")


# http://localhost/sales/orders2
def listorders2(request):
    return HttpResponse("下面是系统中所有的订单信息2。。。")


# http://localhost/sales/customers
def getCustomers(request):
    # 取得Client里面对象的所有值
    qs = Client.objects.values()
    # 定义返回字符串,初始化变量
    res = ''
    # 遍历结果集,把字符串给整合一下
    for customer in qs:
        for name, value in customer.items():
            res += f'{name} : {value} | '
            # <br> 表示换行
        res += '<br>'
    return HttpResponse(res)


# http://localhost/sales/getCustomerByName/?name=Alice
def getCustomerByName(request):
    # 先返回一个QS对象
    qs = Client.objects.values()
    # 检查URL中是否有关键字
    # GET代表GET请求
    # get代表获取请求中的参数
    # 如果没有name参数就返回一个None对象
    name = request.GET.get('name', None)
    # 如果有关键字
    if name:
        # 使用filter方法过滤
        qs = qs.filter(name=name)

    # 返回字符串
    res = ''
    for customer in qs:
        for name, value in customer.items():
            res += f'{name} : {value} | '
        res += '<br>'
    return HttpResponse(res)
