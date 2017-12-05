from django.conf.urls import url

from app03 import views as vw3
urlpatterns = [

    url(r'upup',vw3.upup),
    url(r'add',vw3.articleadd),
    url(r'del/(?P<article_id>\d+)',vw3.articledel),
    url(r'edit/(?P<article_id>\d+)',vw3.articleedit),
    url(r'commentTree/(?P<article_id>\d+)',vw3.commentTree),
    url(r'comment',vw3.comment),
    url(r'backstage',vw3.backstage),

    url(r'^(?P<username>.*)/articles/(?P<para>.*)',vw3.details),



    url(r'^(?P<username>.*)/(?P<condition>tag|cation|time)/(?P<para>.*)',vw3.personblog),

    url(r'^(?P<username>.*)',vw3.personblog,name='authorblog'),
]