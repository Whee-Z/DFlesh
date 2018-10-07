from django.shortcuts import render
from .models import TypeInfo,GoodInfo
from django.core.paginator import Paginator

# Create your views here.
#查询每类商品最新的四个和点击率最高的四个
def index(request):
    """
    该视图主要是查询页面中呈现的商品
    每类商品要查询两次
    """
    count = request.session.get('count')
    fruit = GoodInfo.objects.filter(good_type__id=1).order_by("-id")[:4]
    fruit_click = GoodInfo.objects.filter(good_type__id=1).order_by("-good_click")[:4]
    seafood = GoodInfo.objects.filter(good_type__id=2).order_by("-id")[:4]
    seafood_click = GoodInfo.objects.filter(good_type__id=2).order_by("-good_click")[:4]
    meat = GoodInfo.objects.filter(good_type__id=3).order_by("-id")[:4]
    meat_click = GoodInfo.objects.filter(good_type__id=3).order_by("-good_click")[:4]
    egg = GoodInfo.objects.filter(good_type__id=4).order_by("-id")[:4]
    egg_click = GoodInfo.objects.filter(good_type__id=4).order_by("-good_click")[:4]
    vegetable = GoodInfo.objects.filter(good_type__id=5).order_by("-id")[:4]
    vegetable_click = GoodInfo.objects.filter(good_type__id=5).order_by("-good_click")[:4]
    freezefood = GoodInfo.objects.filter(good_type__id=6).order_by("-id")[:4]
    freezefood_click = GoodInfo.objects.filter(good_type__id=6).order_by("-good_click")[:4]

    # # 构造上下文
    context = {'title': '首页', 'fruit': fruit,
               'seafood': seafood, 'meat': meat, 'egg': egg,
               'vegetable': vegetable, 'freezefood': freezefood,
               'fruit_click': fruit_click, 'seafood_click': seafood_click, 'meat_click': meat_click,
               'egg_click': egg_click, 'vegetable_click': vegetable_click, 'freezefood_click': freezefood_click,
               'guest_cart': 1, 'page_name': 0, 'count': count}

    return render(request,'df_user/index.html',context)

#商品列表
def goodlist(request,typeid,pageid,sort):
    """
    goodlsit负责展示某件商品的详细信息
    :param typeid: 商品类型id
    :param pageid: 分页
    :param sort: 按照最新商品，商品价格，点击率进行排序
    """
    count = request.session.get('count')
    #获取最新的商品
    newgood = GoodInfo.objects.all().order_by('-id')[:2]
    #根据条件查询所有商品,1按照最新排序2按照价格排序3按照点击率排序
    if sort == '1':#1按照最新排序
        sum_goodlist = GoodInfo.objects.filter(good_type_id=typeid).order_by('-id')
    elif sort == '2':#2按照价格排序
        sum_goodlist = GoodInfo.objects.filter(good_type_id=typeid).order_by('-good_price')
    elif sort == '3':#3按照点击率排序
        sum_goodlist = GoodInfo.objects.filter(good_type_id=typeid).order_by('-good_click')

    #分页
    paginator = Paginator(sum_goodlist,10)
    goodList = paginator.page(int(pageid))
    #??????????
    pindexlist = paginator.page_range

    #确定商品类型
    goodtype = TypeInfo.objects.get(id=typeid)
    # count = CartInfo.objects.filter(
    #     user_id=request.session.get('userid')).count()
    # 构造上下文  'count': count,
    context = {'title': '商品详情',  'list': 1,
               'guest_cart': 1, 'goodtype': goodtype,
               'newgood': newgood, 'goodList': goodList,
               'typeid': typeid, 'sort': sort,
               'pindexlist': pindexlist, 'pageid': int(pageid),'count':count}

    # 渲染返回结果
    return render(request, 'df_goods/list.html', context)

#商品详情
def detail(request,id):
    good = GoodInfo.objects.get(pk=int(id))
    good.good_click=good.good_click+1
    good.save()
    # 查询当前商品的类型   goodinfo__id 值
    # goodtype = TypeInfo.objects.get(goodinfo__id=id)
    goodtype = good.good_type
    # type = TypeInfo()

    count = request.session.get('count')
    #goods.gtype = typeinfo    goods.gtype.goodsinfo_set -> typeinfo.goodsinfo_set
    news = good.good_type.goodinfo_set.order_by('-id')[0:2]
    # print '*' * 10
    # print news[0].gtitle
    # print goodtype    猪牛羊肉
    # print goods.gtype  猪牛羊肉

    context={'title':good.good_type.type_title,'guest_cart':1,
             'g':good,'newgood':news,'id':id,
             'isDetail': True,'list':1,'goodtype': goodtype,'count':count}
    response=render(request,'df_goods/detail.html',context)


    #使用cookies记录最近浏览的商品id

    #获取cookies
    good_ids = request.COOKIES.get('good_ids', '')
    #获取当前点击商品id
    good_id='%d'%good.id
    #判断cookies中商品id是否为空
    if good_ids!='':
        #分割出每个商品id
        good_id_list=good_ids.split(',')
        #判断商品是否已经存在于列表
        if good_id_list.count(good_id)>=1:
            #存在则移除
            good_id_list.remove(good_id)
        #在第一位添加
        good_id_list.insert(0,good_id)
        #判断列表数是否超过5个
        if len(good_id_list)>=6:
            #超过五个则删除第6个
            del good_id_list[5]
        #添加商品id到cookies
        good_ids=','.join(good_id_list)
    else:
        #第一次添加，直接追加
        good_ids=good_id
    response.set_cookie('good_ids',good_ids)

    return response
    

