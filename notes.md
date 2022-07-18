### create django project

```shell
django-admin startproject projectName
```

- 和项目同名的文件夹下面放置的是配置文件
- _manage.py_ 是工具脚本， 包含常用命令
- _wsgi.py_ ： server 调用 application 的入口

  - python 组织制定了 web 服务网关接口（Web Server Gateway Interface） 规范 ，简称 wsgi
  - 分为两块
    - wsgi web server
      - 接受 http 请求，调用 application 的接口或者方法，函数
      - 接受 application 的返回结果，再通过 http 返回给前端
    - wsgi web application
      - 处理具体请求，把数据返回给 server
  - 为什么分成两个部分：
    - server 提供高效 http 请求处理环境可以使用多线程、多进程或者协程的机制。http 请求发送到 wsgi web server,wsgi web server 分配 线程或者进程或者 轻量级线程(协程)，然后在 这些 线程、进程、或者协程里面，去调用执行 wsgi web application 的入口代码
    - application 处理具体业务

- django 属于 application 的框架,但也提供了一个调试代码用的简单的 server, 上线的时候需要选择一个高效的 wsgi web server。
- request 用来取出请求信息，而 response 则用来添加要返回给浏览器的信息。

### Run server

```shell
python manage.py runserver 0.0.0.0:80
```

注意：要使用 127.0.0.1 访问。可以在 _settings.py_ 里面增加一些 ip 地址作为访问地址

### 创建项目 app

- 一个 Django 的 app 可以理解为一个模块，类似于一个包

```shell
python manage.py startapp appName
```

- http 发送的请求通常在 _view.py_ 里面处理

```python
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

# http://localhost/sales/orders
def listorders(request):
    return HttpResponse("下面是系统中所有的订单信息。。。")
```

- 告诉 Django：url 和相应函数（理解为 Handel）URL 路由设置

  - 配置目录，_urls.py_，在 urlpatterns 里面配置

  ```python
  from sales.views import listorders
  urlpatterns = [
  path('admin/', admin.site.urls),
  path('sales/orders', listorders),
  ]
  ```

  - 如果路由项目特别多的时候，可以归类（sales 归 sales，mgr 归类为 mgr），可以把主路由表(_urls.py_)拆分为不同的路由子表 - 在 app 里面新增一个路由文件（以 sales 为例）

    - 文件路径：_sales/urls.py_

    ```python
    from django.urls import path
    # 导入sales下面的views里面的处理请求的函数
    from sales.views import listorders, listorders2
    urlpatterns = [
    path('sales/orders', listorders),
    path('sales/orders2', listorders2)
    ]
    ```

    - 文件路径：_demo/urls.py_

    ```python
    from django.contrib import admin
    # 导入include
    from django.urls import path, include

    urlpatterns = [
    path('admin/', admin.site.urls),
    # include里面写上app.urls
    path('sales/', include('sales.urls')),
    ]
    ```

  - path 可以写为正则表达式

### 数据库

#### 先使用 sqlite

- 数据库配置在 _settings.py_ ->

  ```python
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
  }
  ```

  - 如果没有自动创建 `db.sqlite3` 的话，执行命令：`python manage.py migrate`

- 使用 sqliteStudio 链接了数据库后，里面有一些默认的表，都是在 _settings.py_ 里面 `INSTALLED_APPS` 配置的

#### 使用 ORM

- ORM（object relational mapping） 指的是通过对象来操作数据库

- 数据库表的操作，包括 表的定义、表中数据的增删改查，都可以通过 Model 类型的对象进行的。(和 Spring 很像)

- 通常，在 Django 中

  - 定义一张数据库的表 就是定义一个继承自 django.db.models.Model 的类

  - 定义该表中的字段（列）， 就是定义该类里面的一些属性

  - 类的方法就是对该表中数据的处理方法，包括 数据的增删改查

##### 定义数据库表

- 创建继承一个 model 的类就可以了

- 可以新建一个应用（APP）叫 common 专门用来存放一些公用工具,然后在*models.py*里面创建表

  ```python
  名称 = models.类型(约束)
  ```

  ```python
  from django.db import models
  # 继承model
  class Customer(models.Model):
    # 客户名称
    name = models.CharField(max_length=200)

    # 联系电话
    phonenumber = models.CharField(max_length=200)

    # 地址
    address = models.CharField(max_length=200)
  ```

  [关系对应表]: (https://blog.csdn.net/qq_40942329/article/details/79030129)
  [官方文档]: (https://docs.djangoproject.com/en/4.0/ref/models/fields/#model-field-types)

- 再在数据库里面创建表

  - 告诉 Django 新建了一个模块（APP）
    _settings.py_ -> INSTALLED_APP

  ```python
  INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 加入下面这行
    'common.apps.CommonConfig',
  ]
  ```

  - 执行命令创建表：
    `python manage.py makemigrations 修改的应用(model)的名称`
    比如：
    `python manage.py makemigrations common`
    这个时候只是在 _common_ 下的 _migration_ 里面新增了一个 00001_initial.py 文件，还需要将这个文件提交到数据库

  - 把变动提交到数据库里面
    `python manage.py migrate`

- 数据库增加一个字段 qq 的时候,重复执行上面的命令.这个时候会报错:
  ```terminal
  It is impossible to add a non-nullable field 'qq' to client without specifying a default. This is because the database needs something to populate existing rows.
  ```
  原因：可能原数据库已经有一些记录了，原来字段没有 qq，qq 没有指定为空，所以需要配置缺省值，或者配置可以为空；
  如果设置 _null=True_，则仅表示在数据库中该字段可以为空，但使用后台管理添加数据时仍然要需要输入值，因为 Django 自动做了数据验证不允许字段为空
  如果想要在 Django 中也可以将字段保存为空值，则需要添加另一个参数：_blank=True_
  ```python
  qq = models.CharField(max_length=30, null=True, blank=True)
  ```

### 使用 Django admin 管理数据

- 因为 Django 会自己生成 auth_user 表，一般不去修改，直接使用
- 由于 Django 的密码是收到保护的，一般不在数据库管理工具直接新建管理员账户，而是使用控制台`python manage.py createsuperuser`
  ```shell
  python manage.py createsuperuser
  Username (leave blank to use 'byhy'): byhy
  Email address: byhy@163.com
  Password:
  Password (again):
  Superuser created successfully.
  ```
- 现在就可以访问 `http://127.0.0.1/admin/` ，输入刚才注册的用户密码登录
- 但是此时没有办法在这个网站管理新建的 client 表，要使用的话需要进行登记。需要进入*common/admin.py*

  ```python
  from django.contrib import admin

  from .models import Customer

  dmin.site.register(Customer)
  ```

### 读取表中数据

- 在 sales 的 views.py 里面新增一个处理请求的方法

```python
# 首先导入model
from common.models import Client
# http://localhost/sales/customers
def getCustomers(request):
    # objects是Django里面的类用来操作数据库的接口，objects是model.Model里面的，称为manager接口
    # objects.values()返回QuerySet对象，包含所有的表记录，每一条记录都是一个dict对象（字典对象），也就是一个键值对
    qs = Client.objects.values()
    # 定义返回字符串,初始化变量
    res = ''
    # 遍历结果集,把字符串给整合一下，这里的customer就是一个dict对象
    for customer in qs:
      # 再遍历dict对象，使用items()取出键值对
        for name, value in customer.items():
            res += f'{name} : {value} | '
            # <br> 表示换行
        res += '<br>'
    return HttpResponse(res)
```

#### 使用 filter 方法过滤结果集

```python
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
```

以上效果类似于

```sql
select * from customer where customer.name = 'Alice'
```

Django 不用原生查询语句，只需要使用对象里面的方法
然后注册路由。不要忘记在路由最后面加上/.其实一般最后都要加一个/，但是前面写错了懒得改了

```python
path('getCustomerByName/', getCustomerByName)
```

- request.GET.get
  会把所有的参数都放进类似字典的东西里面。
  如果说一个 url 是`/sales/customers/?phonenumber=13000000001&qq=123`
  ```python
  request.GET={
    'phonenumber':'13000000001',
    'qq':'123'
  }
  ```
  （有点像一个 json）

### 资源的增删改查

- 关于 path()方法：
  函数 `path()` 具有四个参数，两个必须参数：`route` 和 `view`，两个可选参数：`kwargs` 和 `name`.

  - `route`:route 是一个匹配 URL 的准则（类似正则表达式）。当 Django 响应一个请求时，它会从 urlpatterns 的第一项开始，按顺序依次匹配列表中的项，直到找到匹配的项。

  这些准则不会匹配 `GET` 和 `POST` 参数或域名。例如，URLconf 在处理请求 https://www.example.com/myapp/ 时，它会尝试匹配 myapp/ 。处理请求 https://www.example.com/myapp/?page=3 时，也只会尝试匹配 myapp/

  - `view`:当 Django 找到了一个匹配的准则，就会调用这个特定的视图函数，并传入一个 HttpRequest 对象作为第一个参数，被“捕获”的参数以关键字参数的形式传入

  - `kwargs`:任意个关键字参数可以作为一个字典传递给目标视图函数

  - `name`:为你的 URL 取名能使你在 Django 的任意地方唯一地引用它

- url 是一样的，要怎么定位到 function？_url 是一样的，但是请求方法不一样_,django 的 url 路由功能*不*支持*直接*根据 http 请求的方法和请求体里面的参数进行路由,因为`path()`没有这个参数

  - GET 查看
  - POST 增加
  - DELETE 删除
  - PUT 修改
  - 解决方案：

    1. 自己编写一个函数，根据 http 请求的类型和请求体里面的参数分发

    - 思路:所有的增删改查都在同一个函数里面进行处理，再在 dispatch 里面进行细分

    ```python
    url('/api/mgr/customers','dispatch')
    ```

    - 在 customer.py 下面定义一个 dispatcher 函数。`json.loads(request.body)`把 request 请求转化为 python 字典对象

    ```python
    def dispatcher(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    # GET请求 参数在url中，同过request 对象的 GET属性获取
    if request.method == 'GET':
        request.params = request.GET

    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    elif request.method in ['POST','PUT','DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式,使用json.load()变成字典类型
        request.params = json.loads(request.body)

    # 根据不同的 action 分派给不同的函数进行处理

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
      return JsonResponse({'ret': 1, 'msg': '不支持该类型 http 请求'})
    ```

- 在总路由表和子路由表里面注册路由

```python
path('mgr/', include('mgr.urls'))
```

```python
from django.urls import path

from mgr import customer

urlpatterns = [
    path('customers', customer.dispatcher),
]
```

#### 查

- GET 请求参数的格式

```
GET  /api/mgr/customers?action=list_customer  HTTP/1.1
```

- GET 返回参数的格式

```json
{
  "ret": 0,
  "retlist": [
    {
      "address": "company address",
      "id": 1,
      "name": "name",
      "phonenumber": "11111111"
    },

    {
      "address": "company address 2",
      "id": 4,
      "name": "name 2",
      "phonenumber": "111111111"
    }
  ]
}
```

- 写出数据处理的逻辑，使用 `list()`将 QuerySet 对象转化为一个字典.不用写在 view 里面，因为这个不是 view

```python
# 查询客户
def listcustomers(request):
  # 返回一个 QuerySet 对象 ，包含所有的表记录
  qs = Client.objects.values()

  # 将 QuerySet 对象 转化为 list 类型
  # 否则不能 被 转化为 JSON 字符串
  retlist = list(qs)

  return JsonResponse({'ret': 0, 'retlist': retlist})
```

#### 增

- POST 请求参数

```json
{
  "action": "add_customer",
  "data": {
    "name": "company name",
    "phonenumber": "123456789",
    "address": "company address"
  }
}
```

- 实现代码。`request.params`是一个字典对象

```python
def addcustomer(request):
  info = request.params['data']
  # create成功后会返回这个新建的对象
  newClient = Client.objects.create(name=info['name'],
                                    phoneNumber=info['phoneNumber'],
                                    address=info['address'])
  return JsonResponse({'ret': 0, 'id': newClient.id})
```

- 暂时先取消 CSRF:django 需要对 POST 和 PUT 先进行校验，先暂时取消

#### 改

- PUT 请求参数

```json
{
  "action": "modify_customer",
  "id": 6,
  "newdata": {
    "name": "company name",
    "phonenumber": "11111111",
    "address": "address"
  }
}
```

- 实现代码

```python
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
```

#### 删

- DELETE 请求参数

```json
{
  "action": "del_customer",
  "id": 6
}
```

- 代码实现

```python
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
```

### 登陆功能的实现

- 响应 response 和请求 request
  - 响应的`content-type`一般都是 json
  - 请求的`content-type`大部分都是 x-www-form-urlencode,json 或者 xml（不常见）
    - urlencode 格式：
      `参数名=值&参数名=值...`

#### Steps

- 取出参数里面的值
  - django 一开始就会生成一张 user 表，密码是加密的，所以调用 Django 的库进行密码校验`user = authenticate(数据库字段名=url对应的参数值)`
- 校验值
- 使用`login(request, user)`方法登陆用户
- signin

  ```python
  def signin(request):
    userName = request.POST.get("username")
    passWord = request.POST.get("password")

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
  ```

- sign-out
  ```python
  def signout(request):
    # 直接调用logout方法
    logout(request)
    return JsonResponse({'ret': 0})
  ```

### 使用 python 构建 http 请求

#### 使用 requests 库

- [requests 库的教程](https://docs.python-requests.org/zh_CN/latest/user/quickstart.html)
- 代码：post 用 data,get 用 params

  ```python
  response = requests.post('url', data = {'key':'value'})

  pprint.pprint(response.json())
  ```

  ```python
  response = requests.ger('url', params = {'key':'value'})

  pprint.pprint(response.json())
  ```

### session 和 token

#### 检验用户是否登陆了

##### session

- Django 的`django_session`的 session data 存储了该用户的 ID 、姓名 、登录名 之类的
- 成功调用`login()`方法之后，Django 会在`django_session`表里新增一条记录
- 使用`request.session['key']='value'`可以给 session 增添一些值
- 然后在该登录请求的 HTTP 响应消息中， 的头字段 Set-Cookie 里填入 `sessionid` 数据.
  `Set-Cookie: sessionid=6qu1cuk8cxvtf4w9rjxeppexh2izy0hh`.
  意思是把`sessionid`存在`cookie`里面。以后每次访问 同一个网站服务， 必须在 HTTP 请求中再带上 这些 cookie 里面的数据。
- 服务端接受到该请求后，只需要到 session 表中查看是否有该 sessionid 对应的记录，这样就可以判断这个请求是否是前面已经登录的用户发出的。

###### 在 mgr 相关的 api 下面加上验证登陆信息

- Django 的 setting 里面有 session 的支持
- 检查有没有登陆&是不是管理员。这个例子在`customer.py`里面增加代码
  `302`代表重定向

```python
# 校验登陆的用户是否是mgr用户
# 用户是否登陆:如果session中没有usertype这个值
if 'usertype' not in request.session:
    return JsonResponse({'ret': 302, 'msg': 'not login', 'redirect': '/mgr/sign.html'}, status=302)
if request.session['usertype'] != 'mgr':
    return JsonResponse({'ret': 302, 'msg': 'not super account', 'redirect': '/mgr/sign.html'}, status=302)
```

##### token

- [详见这个 issue](https://github.com/MoiraDust/myblog/issues/19)

### 关系型数据库

#### 一对多

- 就是外键的关系
- 比如说一个`Client`可以有多个`Order`.Order 表里面的客户 ID 必须是 Client 表中的客户 ID（外键）.
  Order 里面 ClientID 的值只能是 Client 表里面 ID 的主键

```python
class Order(models.Model):
    name = models.CharField(max_length=200)
    create_date = models.DateTimeField(default=datetime.datetime.now)
    # 客户为外键
    customer = models.ForeignKey(Client, on_delete=models.PROTECT)
```

- 语法

```python
字段名=models.ForeignKey(关联的表名,on_delete=...)
```

- on_delete 的值
  - CASCADE：删除主键记录和 相应的外键表记录。
    比如，我们要删除客户 A，在删除了 Client 中 A 同时，也删除 Order 表中**所有**A 的订单记录
  - PROTECT：禁止删除记录。
    除非我们将 Order 表中所有 A 的订单记录都先删除掉，才能删除该 Client 中 A 的记录。
  - SET_NULL：删除主键记录，并且将外键记录中外键字段的值置为 null。 当然前提是外键字段要设置为值允许是 null。
    比如，我们要删除客户张三时，在删除了客户张三记录同时，会将 Order 表里面所有的 张三记录里面的 customer 字段值置为 null。 但是上面我们并没有设置 customer 字段有 null=True 的参数设置，所以，是不能取值为 SET_NULL 的。

#### 一对一

- 唯一对应关系，比如说`Student`和`Address`
- 数据库中实现方式依旧是外键，但需要有一个`unique=true`
- Django 中用 `OneToOneField` 对象实现一对一的关系
- Django 中有个例子：把默认的 user 表给 extend 了
- 代码例子:

```python
class Student(models.Model):
    # 姓名
    name = models.CharField(max_length=200)
    # 班级
    classname = models.CharField(max_length=200)
    # 描述
    desc = models.CharField(max_length=200)


class ContactAddress(models.Model):
    # 一对一 对应学生
    student = models.OneToOneField(Student, on_delete=models.PROTECT)
    # 家庭
    homeaddress = models.CharField(max_length=200)
    # 电话号码
    phone = models.CharField(max_length=200)
```

#### 多对多

- 比如说`medicine`和`order`的关系,一个订单有多种药品，一个药品可以加入多个订单
- Django 通过`ManyToManyField`表示

```python
# order
class Order(models.Model):
    name = models.CharField(max_length=200)
    create_date = models.DateTimeField(default=datetime.datetime.now)
    # 客户为外键
    customer = models.ForeignKey(Client, on_delete=models.PROTECT)
    # 订单中的药品
    medicine = models.ManyToManyField(Medicine, through='OrderMedicine')


class OrderMedicine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()
```

- `through`可以不写。但由于这个例子还需要药品采购数量，所以需要加
- Order 表和 Medicine 表 的多对多关系 是 通过另外一张表， 也就是 through 参数 指定的 OrderMedicine 表 来确定的。
- migrate 的时候，Django 会自动产生一张新表 （这里就是 common_ordermedicine）来 实现 order 表 和 medicine 表之间的多对多的关系。

### 药品管理

- 和 customer 差不多...

### ORM 处理关联表

[ORM 方法](https://www.byhy.net/tut/webdev/django/11/)

#### 使用 shell 命令直接插入数据

- 在 command 里面输入`python manage.py shell`
- 创建数据

```python
from common.models import *
对象名 = 类名.objects.create(字段名=数据)
```

```python
from common.models import *
c1 = Country.objects.create(name='中国')
c2 = Country.objects.create(name='美国')
c3 = Country.objects.create(name='法国')
Student.objects.create(name='白月', grade=1, country=c1)
Student.objects.create(name='黑羽', grade=2, country=c1)
Student.objects.create(name='大罗', grade=1, country=c1)
Student.objects.create(name='真佛', grade=2, country=c1)
Student.objects.create(name='Mike', grade=1, country=c2)
Student.objects.create(name='Gus',  grade=1, country=c2)
Student.objects.create(name='White', grade=2, country=c2)
Student.objects.create(name='Napolen', grade=2, country=c3)
```

- 通过外键访问数据
  - 获取实例
  ```python
  实例名=类名.objects.get(字段名=值)
  s1 = Student.objects.get(name='白月')
  ```
  - 通过外键连接到另一个数据库，读取另一个数据库中的字段
  ```python
  实例名.外链表.字段名
  s1.country.name
  ```
- 外键表字段过滤

  - 查找一年级学生,使用`className.objects.filter(condition).value`

  ```python
  Student.objects.filter(grade=1).values()
  ```

  - 查找一年级的中国学生

    - 方法 1：先从`Country`表找到中国的 ID，再从`Student`表找到学生

    ```python
    cn = Country.objects.get(name='China')
    Student.objects.filter(grade=1,country_id=cn.id).values()
    ```

    或者也可以直接把外链表写上.创建学生实例的时候直接就是写的`country=国家实例`

    ```python
    Student.objects.filter(grade=1,country=cn).values()
    ```

    - 方法 2:使用外键关联

    ```python
    表名.objects.filter(本表的condition,外链表的字段='值').values()
    Student.objects.filter(grade=1,country__name='中国').values()
    ```

    **tip:**

    - `country__name`有两个下划线。两个下划线在 Django 底层会被解析为外链表
    - `values()`里面的参数是返回的字段，如`values('name','country__name')`
    - 两个下划线很奇怪，可以给字段名重命名可以使用`annotate`方法

    ```python
    表名.objects.annotate(
      新列名=F('旧列名')
    )\
    .filter(condition).values()
    ```

    ```python
    from django.db.models import F

    # annotate 可以将表字段进行别名处理
    Student.objects.annotate(
    countryname=F('country__name'),
    studentname=F('name')
    )\
    .filter(grade=1,countryname='中国').values('studentname','countryname')
    ```
