"""demo_ajax URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin

from app01 import views
from app03 import views as vw3
from django.views.static import serve
from django.conf import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^test/', vw3.test),
    url(r'^moupsum/', views.moupsum),
    url(r'^upload/', views.upload),
    url(r'^login/', vw3.login2),
    url(r'^login/', vw3.login_test),
    url(r'^logout/', vw3.log_out),

    url(r'^pc-geetest/register', vw3.pcgetcaptcha, name='pcgetcaptcha'),
    url(r'^pc-geetest/ajax_validate',vw3.pcajax_validate, name='pcajax_validate'),

    url(r'^uploadFile/', vw3.uploadFile),
    url(r'^register/', vw3.register),
    # url(r'^code/', vw3.login_test),
    url(r'^get_validcode/', vw3.VerificationCode),
    url(r'^blog_home/', vw3.blog_home),
    url(r'^menu/(?P<menu>.+)', vw3.blog_home),
    url(r'^blog/', include('app03.urls')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^$',vw3.blog_home),

]
