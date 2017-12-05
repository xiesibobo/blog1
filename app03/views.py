import json,os
import datetime
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
from django.conf import settings
from app03 import models
from app03 import forms
from django.db import transaction
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger



# Create your views here.


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        response = {'flag': False}
        userobj = models.UserInfo.objects.filter(username=username, password=password)

        if userobj:
            response["flag"] = True
        import json
        return HttpResponse(json.dumps(response))
        # return HttpResponse('OK')

def log_out(request):
    auth.logout(request)

    return redirect("/login/")



def register(request):
    regResponse = {"user": None, "errorsList": None}
    if request.method == 'GET':
        formobj = forms.UserInfoForm(request)
        return render(request, 'registers.html', {'forms': formobj})
    elif request.is_ajax():
        formobj = forms.UserInfoForm(data=request.POST, request=request)
        if formobj.is_valid():
            username = formobj.cleaned_data.get('username')
            password = formobj.cleaned_data.get('password')
            email = formobj.cleaned_data.get('email')
            avatar_img = formobj.cleaned_data.get('avatar')
            nickname = formobj.cleaned_data.get('nickname')
            user_obj = models.UserInfo.objects.create_user(username=username, password=password, email=email,
                                                           avatar=avatar_img, nickname=nickname)
            regResponse['user'] = user_obj
        else:

            regResponse['errorsList'] = formobj.errors
        return HttpResponse(json.dumps(regResponse))


def ajax_register(request):
    return HttpResponse('OK!')


def login_test(request):
    if request.method == 'GET':
        return render(request, 'logintest.html')
    if request.is_ajax():
        login_response = {'is_login': False, 'error_msg': None}
        if request.session['keepValidCode'].upper() != request.POST.get('validCode').upper():
            login_response['error_msg'] = '验证码输入错误'
        else:
            print(request.POST.get('username'),request.POST.get('password'))
            user = auth.authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            if user:
                login_response['is_login'] = True
                auth.login(request, user)
            else:
                login_response['error_msg'] = '用户名或者密码错误'
    return HttpResponse(json.dumps(login_response))


def VerificationCode(request):
    # from  PIL import Image
    # img=Image.new(mode='RGB',size=(120,60),color='yellow')
    # from io import BytesIO
    # f=BytesIO()
    # img.save(f,'png')
    # data=f.getvalue()

    import random
    import os
    from io import BytesIO
    from  PIL import Image, ImageDraw, ImageFont

    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    img = Image.new(mode='RGB', size=(120, 40), color=color)
    draw = ImageDraw.Draw(img, "RGB")

    # print(settings.BASE_DIR)
    font_dir = os.path.join(settings.BASE_DIR, 'static', 'font', 'W5.ttf')
    # print(font_dir)
    font = ImageFont.truetype(font_dir, 25)
    # draw.line()

    # font = ImageFont.load_default().font

    valid_list = []
    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_lower_zimu = chr(random.randint(65, 90))
        random_upper_zimu = chr(random.randint(97, 122))
        random_char = random.choice([random_num, random_lower_zimu, random_upper_zimu])
        draw.text([5 + i * 20, 10], random_char,
                  (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), font=font)
        valid_list.append(random_char)
    f = BytesIO()
    img.save(f, 'png')
    data = f.getvalue()
    valid_str = "".join(valid_list)
    print(valid_str)

    request.session["keepValidCode"] = valid_str

    return HttpResponse(data)


def blog_home(request, *args, **kwargs):

    if kwargs:
        print(kwargs.get('menu'))
        article_list_all = models.Article.objects.filter(site_article_category__title=kwargs.get('menu'))
        print(article_list_all)
    else:
        article_list_all = models.Article.objects.all()

    page_list = Paginator(article_list_all, 1)
    numcount = page_list.page_range
    num_pages = page_list.num_pages
    num = request.GET.get('page', 1)
    if num_pages > 10 and int(num) > 5:
        numcount = list(numcount)[int(num) - 5:int(num) + 5]
        print(numcount, type(numcount))
    else:
        numcount = list(numcount)[:10]
        print(numcount)

    article_list=page_list.page(num)
    sitecategory = models.SiteCategory.objects.all()

    return render(request, 'bloghome.html', {'article_list': article_list,
                                             'sitecategory': sitecategory,
                                             'numcount': numcount,
                                             'num': int(num),
                                             'num_pages': num_pages,
                                             'range10': range(11)
                                             })


def personblog(request, *args, **kwargs):
    from django.db.models import Count
    nickname = kwargs.get('username')

    userobj = models.UserInfo.objects.filter(nickname=nickname).first()
    if userobj:

        if kwargs.get('condition')=='tag':
            article_list_all=models.Article.objects.filter(user=userobj,article2tag__tag__title=kwargs.get('para'))
        elif kwargs.get('condition')=='time':
            thedate=kwargs.get('para').split('/')
            article_list_all = models.Article.objects.filter(user=userobj, create_time__year=thedate[0],create_time__month=thedate[1])
        elif kwargs.get('condition')=='cation':
            article_list_all = models.Article.objects.filter(user=userobj, category__title=kwargs.get('para'))
        else:
            article_list_all = models.Article.objects.filter(user__nickname=nickname)

        cations = models.Category.objects.filter(blog__user__nickname=nickname)

        tags = models.Tag.objects.filter(blog__user__nickname=nickname).annotate(c=Count('article__nid')).values_list(
            'title', 'c')

        dates = models.Article.objects.filter(user=userobj).extra(
            select={'filter_create_date': 'strftime("%%Y/%%m",create_time)'}).values_list(
            'filter_create_date').annotate(Count('nid'))

        page_list = Paginator(article_list_all, 1)
        numcount = page_list.page_range
        num_pages = page_list.num_pages
        num = request.GET.get('page', 1)
        if num_pages > 10 and int(num) > 5:
            numcount = list(numcount)[int(num) - 5:int(num) + 5]
            print(numcount, type(numcount))
        else:
            numcount = list(numcount)[:10]
            print(numcount)

        article_list = page_list.page(num)

        return render(request, 'personindex.html',
                      {'article_list': article_list,
                       'userobj': userobj,
                       'cations': cations,
                       'tags': tags,
                       'dates':dates,
                       'numcount': numcount,
                       'num': int(num),
                       'num_pages': num_pages,
                       'range10': range(11)
                       })
    else:
        return HttpResponse('<h1>404 NOT FOUND</h1>')


def details(request,*args,**kwargs):
    from django.db.models import Count

    deatil=models.ArticleDetail.objects.filter(article__nid=kwargs.get('para')).first()
    userobj = models.UserInfo.objects.filter(nickname=kwargs.get('username')).first()
    if deatil and userobj:
        cations = models.Category.objects.filter(blog__user__nickname=kwargs.get('username'))

        tags = models.Tag.objects.filter(blog__user__nickname=kwargs.get('username')).annotate(c=Count('article__nid')).values_list(
            'title', 'c')

        dates = models.Article.objects.filter(user=userobj).extra(
            select={'filter_create_date': 'strftime("%%Y/%%m",create_time)'}).values_list(
            'filter_create_date').annotate(Count('nid'))
        comments=models.Comment.objects.filter(article__nid=kwargs.get('para'))
        return render(request,'article_detil.html',{'comments':comments,'deatil':deatil,'userobj': userobj, 'cations': cations, 'tags': tags,'dates':dates})
    else:
        return HttpResponse('<h1>404 NOT FOUND</h1>')



def upup(request):
    import json
    from django.db.models import F
    data = {'flag': False, 'msg': None,'is_login':False}
    if request.is_ajax():
        artical_id=request.POST.get('articel')
        if not request.user.is_authenticated():
            data['msg']='您未登录，请登录'
        else:
            data['flag'] = True
            user_id = request.user.nid
            art = models.ArticleUp.objects.filter(article_id=artical_id, user_id=user_id)
            if art:
                data['msg'] = '您已经赞过'
            else:
                with transaction.atomic():
                    models.ArticleUp.objects.create(article_id=artical_id,user_id=user_id)
                    models.Article.objects.filter(nid=artical_id).update(up_count=F('up_count')+1)
                data['flag']=True
                data['msg']='您赞了一下'
    else:return HttpResponse('滚')

    return HttpResponse(json.dumps(data))



def comment(request):
    from django.db.models import F

    if request.is_ajax():
        article_id = request.POST.get('article_id')
        user_id = request.user.nid
        comment_context = request.POST.get('comment_context')
        comment_Respones = {}
        with transaction.atomic():
            if request.POST.get('parent_comment_id'):
                comment_obj = models.Comment.objects.create(user_id=user_id, article_id=article_id,
                                                            content=comment_context,parent_comment_id=request.POST.get('parent_comment_id'))
            else:
                comment_obj=models.Comment.objects.create(user_id=user_id,article_id=article_id,content=comment_context)
            models.Article.objects.update(comment_count=F('comment_count')+1)
            comment_Respones['create_time']=str(comment_obj.create_time)
            comment_Respones['comment_id']=comment_obj.nid
        from django.http import JsonResponse
        return JsonResponse(comment_Respones)
    else:HttpResponse('滚')



def commentTree(request,article_id):
    comment_list=models.Comment.objects.filter(article_id=article_id).values('nid','content','parent_comment_id','user__avatar','create_time','user__nickname')
    comment_dict={}
    comment_tree=[]
    for comment in comment_list:
        comment_dict[comment['nid']]=comment
        comment['create_time']=str(comment['create_time'])[:19]
        comment['children_comments']=[]
        if comment['parent_comment_id']:
            comment_dict.get(comment['parent_comment_id'])['children_comments'].append(comment)
        else:
            comment_tree.append(comment)
    return HttpResponse(json.dumps(comment_tree))



def backstage(request):

    article_list=models.Article.objects.filter(user=request.user)
    category_list=models.Category.objects.filter(blog__user=request.user)
    tag_list=models.Tag.objects.filter(blog__user=request.user)
    return render(request,'backstage.html',{'article_list':article_list,'category_list':category_list,'tag_list':tag_list})


def articleadd(request):
    if request.method=='GET':
        article_list = models.Article.objects.filter(user=request.user)
        category_list = models.Category.objects.filter(blog__user=request.user)
        tag_list = models.Tag.objects.filter(blog__user=request.user)
        article_form = forms.ArticleForm(request=request)
        return render(request,'article_add.html',{'article_list':article_list,'category_list':category_list,'tag_list':tag_list,'article_form':article_form})
    elif request.method=='POST':
        article_form = forms.ArticleForm(data=request.POST,request=request)
        if article_form.is_valid():
            with transaction.atomic():
                title = article_form.cleaned_data.get("title")
                content = article_form.cleaned_data.get("content")
                article_obj = models.Article.objects.create(title=title, desc=content[0:30],
                                                            create_time=datetime.datetime.now(),
                                                            user=request.user,
                                                            category_nid=request.POST.get('categorys'),
                                                            site_article_category_tid=request.POST.get(
                                                                'sitearticlecategorys'),
                                                            )
                tags = request.POST.get('tags')
                for tags_id in tags:
                    models.Article2Tag.objects.create(article=article_obj, tag_id=tags_id)
                models.ArticleDetail.objects.create(content=content, article=article_obj)
            print('*'*40)
        return HttpResponse("添加成功")





def uploadFile(request):
    file_obj=request.FILES.get('imgFile')
    from demo_ajax import settings
    file_path=os.path.join(settings.BASE_DIR,'app03','media','article_upload',file_obj.name)
    with open(file_path,'wb') as f:
        for i in file_obj:
            f.write(i)
    response={
        'error':0,
        'url':'/media/article_upload/'+file_obj.name+'/'
    }
    return HttpResponse(json.dumps(response))

from app03.geetest import GeetestLib
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"
mobile_geetest_id = "7c25da6fe21944cfe507d2f9876775a9"
mobile_geetest_key = "f5883f4ee3bd4fa8caec67941de1b903"

def pcgetcaptcha(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)

def pcajax_validate(request):

    if request.method == "POST":
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        print("status",status)
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {"status":"success"} if result else {"status":"fail"}
        return HttpResponse(json.dumps(result))
    return HttpResponse("error")




def login2(request):
    '''


    添加完滑动验证码的登陆页面
    :param request:
    :return:
    '''
    if request.method == 'GET':
        return render(request, 'logintest.html')
    if request.is_ajax():
        result = {'is_login': False, 'error_msg': None}
        if request.session['keepValidCode'].upper() != request.POST.get('validCode').upper():
            result['error_msg'] = '验证码输入错误'
        else:
            gt = GeetestLib(pc_geetest_id, pc_geetest_key)
            challenge = request.POST.get(gt.FN_CHALLENGE, '')
            validate = request.POST.get(gt.FN_VALIDATE, '')
            seccode = request.POST.get(gt.FN_SECCODE, '')
            status = request.session[gt.GT_STATUS_SESSION_KEY]
            user_id = request.session["user_id"]
            print(request.POST.get('username'),request.POST.get('password'))
            user = auth.authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            if user:
                result['is_login'] = True
                auth.login(request, user)
            else:
                result['error_msg'] = '用户名或者密码错误'
            if status:
                login_response = gt.success_validate(challenge, validate, seccode, user_id)
            else:
                login_response = gt.failback_validate(challenge, validate, seccode)
            if login_response :
             result["status"] = "success"
            else: result["status"]="fail"
        return HttpResponse(json.dumps(result))


def articledel(request,article_id):
    msg={'flag':True,'error':None}
    del_obj=models.Article.objects.filter(nid=article_id,user=request.user)
    if del_obj:

        del_obj.delete()
        msg['flag']=True
    else:
        msg['error']='无法删除'
    return HttpResponse(json.dumps(msg))


def articleedit(request,article_id):

    article_obj=models.Article.objects.filter(nid=article_id,user=request.user)
    print(request.method)
    if request.method=='POST':
        article_form = forms.ArticleForm(data=request.POST,request=request)
        if article_form.is_valid():
            title = article_form.cleaned_data.get("title")
            content = article_form.cleaned_data.get("content")
            with transaction.atomic():
                article_obj.update(title=title)
                models.ArticleDetail.objects.filter(article__nid=article_id).update(content=content)

            return HttpResponse('OK')
        else:return HttpResponse('error')
    # article_form=forms.ArticleForm(article)
    article=article_obj.values('nid','title','articledetail__content')[0]
    category_list = models.Category.objects.filter(blog__user=request.user)
    tag_list = models.Tag.objects.filter(blog__user=request.user)
    article_form=forms.ArticleForm(request=request,data={'title':article['title'],'content':article['articledetail__content']})
    return render(request,'edit.html',{'nid':article['nid'],'category_list':category_list,'tag_list':tag_list,'article_form':article_form})
    # return HttpResponse(article['articledetail__content'])


def test(request):
    testform=forms.ArticleForm(request=request)
    if request.method=='POST':
        testform = forms.ArticleForm(data=request.POST,request=request)
        testform.is_valid()
        print(testform.cleaned_data)
        return HttpResponse('OK!')
    return render(request, 'test.html',{'testform':testform})