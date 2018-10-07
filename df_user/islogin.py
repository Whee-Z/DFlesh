from django.http import HttpResponseRedirect

#如果没登录则转到登录页
def islogin(func):
    def login_fun(request,*args,**kwargs):
        if request.session.get('user_id'):
            return func(request,*args,**kwargs)
        else:
            red = HttpResponseRedirect('/user/login/')
            red.set_cookie('url',request.get_full_path)#记录要返回的那个路径
            return red
    return login_fun