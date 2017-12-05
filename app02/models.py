from django.db import models
#
# # Create your models here.
#
# class user_info(models.Model):
#     id=models.AutoField(primary_key=True)
#     username = models.CharField(verbose_name='用户名',max_length=32)
#     password = models.CharField(verbose_name='密码',max_length=64)
#
#
# class Author(models.Model):
#     SEX_CHOICES=(
#         ('M','Male'),
#         ('N','NO'),
#         ('F','FeMale')
#     )
#     aid=models.AutoField(primary_key=True)
#     uid=models.OneToOneField('user_info')
#     name=models.CharField(verbose_name='博客名',max_length=32)
#     nickname=models.CharField(verbose_name='真实姓名',max_length=32)
#     tel=models.IntegerField()
#     email=models.EmailField()
#     gender = models.CharField(max_length=2, choices=SEX_CHOICES)
#     avatar=models.ImageField()
#
#
# class Tag(models.Model):
#     '''
#     标签
#     '''
#     tid=models.AutoField(primary_key=True)
#     tname=models.CharField(verbose_name='标签名',max_length=32)
#
#
# class classfy(models.Model):
#     '''
#     分类
#     '''
#     cid=models.AutoField(primary_key=True)
#     cname=models.CharField(verbose_name='分类名',max_length=32)
#
# class Article(models.Model):
#     '''
#     文章概要
#     '''
#     aid=models.AutoField(primary_key=True)
#     title=models.CharField(verbose_name='标题',max_length=64)
#     tag=models.ManyToManyField(verbose_name='标签',to='Tag')
#     classify=models.ForeignKey(verbose_name='分类',to='classfy')
#     suummary=models.OneToOneField(verbose_name='详细',to='Suummary')
#
#
# class Suummary(models.Model):
#     '''
#     文章
#     '''
#     sid=models.ForeignKey(to='Article')
#     context=models.TextField()
#
#
# class Poll(models.Model):
#     '''
#     点赞
#     '''
#     lid=models.AutoField(primary_key=True)
#
#     author=models.ForeignKey(verbose_name='谁点赞',to='Author')
#     article=models.ForeignKey(verbose_name='那篇点的赞',to='Article')
#     comment=models.ForeignKey(verbose_name='点赞对象',to='Comment',null=True)
#     flag=models.BooleanField()
#
#     class Meta:
#         unique_poll = ('author', 'article','comment','flag')
#
#
# class Comment(models.Model):
#     '''
#     评论
#     '''
#     author=models.ForeignKey('Author')
#     article=models.ForeignKey(to='Article')
#     tocomment=models.ForeignKey(to='Comment',null=True)
#     time=models.DateField(verbose_name='点赞时间')
#     class Meta:
#         unique_poll = ('author', 'article','tocomment','time')
#
#
# class Fans(models.Model):
#     fid=models.AutoField(primary_key=True)
#     aid = models.OneToOneField('Author')
#     bid = models.OneToOneField('Author')
#
#     class Meta:
#         unique_poll = ('aid', 'bid')
#
#
#
#
#
# '''
# class Fans(models.Model):
#
#     粉丝
#
#     jid=models.OneToOneField('Author')
#     bid=models.OneToOneField('Author')
#     just=models.BooleanField(default=False)#TRUE为互粉
#
#
# '''
#



class ClassList(models.Model):
    '''
    班级列表
    '''
    nid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=24)

class Student(models.Model):
    '''
    学生表
    '''
    nid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=16)
    cls=models.ForeignKey(to='ClassList')


class Questionnaire(models.Model):
    '''
    问卷表
    '''
    nid=models.AutoField(primary_key=True)
    title=models.CharField(max_length=64)
    cls=models.ForeignKey(to='ClassList')
    creator=models.ForeignKey(to='UserInfo')

class Questions(models.Model):

    title=models.CharField(max_length=64)
    question_types=(
        (1,'打分'),
        (2,'单选'),
        (3,'评价')
    )
    tp=models.IntegerField(choices=question_types)

class Option(models.Model):
    title=models.CharField(verbose_name='选项名称',max_length=32)
    score=models.IntegerField(verbose_name='选项对应的分值')
    qs=models.ForeignKey(to=Questions)

class Answer(models.Model):
    stu=models.ForeignKey(to='Student')
    question=models.ForeignKey(to='Questions')
    option=models.ForeignKey(to='Option',null=True,blank=True)
    val=models.IntegerField(null=True,blank=True)
    content=models.CharField(max_length=255,null=True,blank=True)
