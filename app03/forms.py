from django.forms import Form, fields, widgets
from django.core.validators import ValidationError,RegexValidator
from app03 import models

class UserInfoForm(Form):
    username = fields.CharField(
        label='用户名',
        required=True,
        error_messages={'required': '用户名不能为空'},
        widget=widgets.TextInput(attrs={'placeholder': '用户名', 'class': 'form-control data'})

    )
    nickname = fields.CharField(
        label='昵称',
        required=True,
        error_messages={'required':'昵称不能为空'},
        widget=widgets.TextInput(attrs={'placeholder':'昵称','class':'form-control data'})
    )
    password = fields.CharField(
        label='密码',
        required=True,
        error_messages={'required': '密码不能为空'},
        widget=widgets.PasswordInput(attrs={'placeholder': '密码', 'class': 'form-control data'}))
    repaet_password = fields.CharField(
        label='再一次输入密码',
        required=True,
        error_messages={'required': '请再次输入密码'},
        widget=widgets.PasswordInput(attrs={'placeholder': '密码', 'class': 'form-control data'}))
    email = fields.EmailField(
        label='邮箱',
        required=True,
        error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'},
        widget=widgets.EmailInput(attrs={'placeholder': '邮箱', 'class': 'form-control data'}))
    tel = fields.CharField(
        label='手机号',
        required=True,
        error_messages={'required':'手机号码不能为空'},
        widget=widgets.NumberInput(attrs={'placeholder':'手机号码', 'class': 'form-control data'})
    )
    avatar = fields.ImageField(
        label='头像',
        widget=widgets.FileInput(attrs={'class':'avatar_file'})
    )
    valid_code=fields.CharField(
        label='验证码',
        required=True,
        error_messages={'required':'请输入验证码'},
        widget=widgets.TextInput(attrs={'placeholder':'验证码','class':"form-control item"})
    )

    def clean(self):
        if self.cleaned_data.get('password')==self.cleaned_data.get('repeat_password'):
            return self.cleaned_data
        else:
            raise ValidationError('密码不一致，请重新输入')
    def clean_tel(self):
        length=len(self.cleaned_data.get('tel'))
        if length==11 :
            return self.cleaned_data.get('tel')

        raise ValidationError('不是正确的手机号码')
    def clean_username(self):
        username=self.cleaned_data.get('username')
        if models.UserInfo.objects.filter(username=username):
            raise ValidationError('用户名已存在')
        else:
            return self.cleaned_data.get('username')
    def clean_password(self):
        if len(self.cleaned_data.get('password'))>8:
            return self.cleaned_data.get('password')
        else:raise ValidationError('密码八位以上')
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if models.UserInfo.objects.filter(email=email):
            raise ValidationError('邮箱已使用')
        else:
            return self.cleaned_data.get('email')

    def clean_valid_code(self):
        if self.cleaned_data.get('valid_code').upper()==self.request.session.get('valid_code').upper():
            return self.cleaned_data.get('valid_code')
        else:
            raise ValidationError('验证码错误')
    def __init__(self,request,*args,**kwargs):
        super(UserInfoForm,self).__init__(*args,**kwargs)
        self.request=request

# class Comm


from app03.plugins import xss_plugin


class ArticleForm(Form):
    def __init__(self,request,*args,**kwargs):
        super(ArticleForm,self).__init__(*args,**kwargs)
        self.fields['tags'].choices=models.Tag.objects.filter(blog__user=request.user).values_list('nid', 'title')
        self.fields['categorys'].choices=models.Category.objects.filter(blog__user=request.user).values_list('nid', 'title')

        self.fields['categorys'].choices.insert(0,(None, "请选择"))
        self.fields['sitearticlecategorys'].choices=models.SiteArticleCategory.objects.values_list('tid', 'title')
        self.fields['sitearticlecategorys'].choices.insert(0,(None, "请选择"))




    title=fields.CharField(max_length=20,
                           error_messages={'required':'标题不能为空'},
                           widget=widgets.TextInput({'class':'form-control'})
                           )
    content=fields.CharField(error_messages={'required':'内容不能为空'},
                             widget=widgets.Textarea({'class':'form-control','id':'editor_id'}))
    categorys=fields.ChoiceField(label='个人站点：',initial=[],
                            choices=[],
                            widget=widgets.Select({'class':'list-inline'})
    )
    tags=fields.MultipleChoiceField(label='个人标签：',initial=[],
                                    choices=[],
                            widget=widgets.CheckboxSelectMultiple(attrs={'class':'list-inline'})

    )
    sitearticlecategorys=fields.ChoiceField(label='站点分类：',initial=[],
                                            choices=[],
                            widget=widgets.Select(attrs={'class':'list-inline'})
    )


    def clean_content(self):
        html_str=self.cleaned_data.get('content')
        clean_content=xss_plugin.filter_xss(html_str)

        self.cleaned_data['content']=clean_content

        return self.cleaned_data.get('content')