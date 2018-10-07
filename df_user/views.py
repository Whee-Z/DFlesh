from django.shortcuts import render,redirect,HttpResponseRedirect
from hashlib import sha1
from .models import *
from django.http import JsonResponse
from .islogin import islogin
from df_goods.models import GoodInfo
from df_order.models import OrderInfo
from django.core.paginator import Paginator
from df_cart.models import *

# Create your views here.
def register(request):
    context = {'title':'用户注册'}
    return render(request,'df_user/register.html',context)

def register_handle(request):
    #接收输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    #判断两次密码
    if upwd!=upwd2:
        return redirect('/user/register/')
    #密码加密
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    upwd3 = s1.hexdigest()
    #创建对象，存储数据
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    #注册成功转到登录页
    return redirect('/user/login/')

def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()#只需要判断存不存在记个数就可以了
    return JsonResponse({'count':count})#思考什么时候是返回一个json数据呢

def login(request):
    uname = request.COOKIES.get('uname','')
    context = {'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'df_user/login.html',context)#context: 要传入文件中用于渲染呈现的数据, 默认是字典格式

def login_handle(request):
    #接收请求信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    remember = post.get('remember',0)
    #根据用户名查询对象
    user = UserInfo.objects.filter(uname=uname)
    #如果能查到正确的用户名，则判断密码是否正确，都正确则转向用户中心
    if len(user)==1:
        s1 = sha1()
        s1.update(upwd.encode('utf-8'))
        upwd = s1.hexdigest()

        if upwd==user[0].upwd:
            red = HttpResponseRedirect('/goods/index/')
            count = CartInfo.objects.filter(user_id=user[0].id).count()

            #记住用户名
            if remember != 0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1)
            request.session['user_id'] = user[0].id
            request.session['user_name'] = uname
            request.session['count'] = count
            return red
        else:
            context = {'title':'用户登录','error_name':0,'error_pwd':1,'uname':uname}
            return render(request,'df_user/login.html',context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname}
        return render(request, 'df_user/login.html', context)


#def index(request):
#    context = {'title':'首页'}
#    return render(request,'df_goods/index.html',context)

# 登录用户中心
@islogin
def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    user_phone = UserInfo.objects.get(id=request.session['user_id']).uphone
    user_address = UserInfo.objects.get(id=request.session['user_id']).uaddress
#此处应有最近浏览代码
    # 最近浏览
    good_ids = request.COOKIES.get('good_ids', '')
    good_id_list = good_ids.split(',')
    good_list = []
    if len(good_ids):
        for goods_id in good_id_list:
            good_list.append(GoodInfo.objects.get(id=int(goods_id)))

    context = {'title': '用户中心',
               'user_email': user_email,
               'user_name': request.session['user_name'],
               'page_name':1,'info':1,
               'user_phone':user_phone,
               'user_address':user_address,
               'good_list': good_list,
               }
    return render(request, 'df_user/user_center_info.html', context)

#我的订单
@islogin
def order(request):
    context = {'title':'用户中心','page_name':1,'order':1}
    return render(request,'df_user/user_center_order.html',context)

#收货地址
@islogin
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ureceiver = post.get('ureceiver')
        user.uaddress = post.get('uaddress')
        user.uphone = post.get('uphone')
        user.upostcode = post.get('upostcode')
        user.save()
    context = {'title':'用户中心','user':user,'page_name':1,'site':1}
    return render(request,'df_user/user_center_site.html',context)

def logout(request):
    request.session.flush()
    return redirect('/goods/index/')

@islogin
def user_center_order(request, pageid):
    """
    此页面用户展示用户提交的订单，由购物车页面下单后转调过来，也可以从个人信息页面查看
    根据用户订单是否支付、下单顺序进行排序
    """

    uid = request.session.get('user_id')
    # 订单信息，根据是否支付、下单顺序进行排序
    orderinfos = OrderInfo.objects.filter(
        user_id=uid).order_by('zhifu', '-oid')

    # 分页
    #获取orderinfos list  以两个为一页的 list
    paginator = Paginator(orderinfos, 2)
    # 获取 上面集合的第 pageid 个 值
    orderlist = paginator.page(int(pageid))
    #获取一共多少 页
    plist = paginator.page_range
    #3页分页显示
    qian1 = 0
    hou = 0
    hou2 = 0
    qian2 = 0
    # dd = dangqian ye
    dd = int(pageid)
    lenn = len(plist)
    if dd>1:
        qian1 = dd-1
    if dd>=3:
        qian2 = dd-2
    if dd<lenn:
        hou = dd+1
    if dd+2<=lenn:
        hou2 = dd+2



    # 构造上下文
    context = {'page_name': 1, 'title': '全部订单', 'pageid': int(pageid),
               'order': 1, 'orderlist': orderlist, 'plist': plist,
               'pre':qian1,'next':hou,'pree':qian2,'lenn':lenn,'nextt':hou2}

    return render(request, 'df_user/user_center_order.html', context)




