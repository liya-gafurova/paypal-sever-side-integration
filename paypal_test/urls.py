"""paypal_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from finance.urls import finance_url_patterns
from paypal_test.swagger import swagger_urls, decorated_login_view

urlpatterns = [
        url(r'^admin/', admin.site.urls),

        url(r'^', include('django.contrib.auth.urls')),
        url(r'^api/v1/auth/login/$', decorated_login_view, name='rest_login'),
        url(r'^api/v1/auth/', include('rest_auth.urls')),
        url(r'^api/v1/auth/registration/', include('rest_auth.registration.urls')),
        *swagger_urls,

        *finance_url_patterns,

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
print(urlpatterns)
