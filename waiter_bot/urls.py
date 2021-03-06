"""waiter_bot URL Configuration

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
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from qr_generator.views import qr_generator

urlpatterns = [
    path('', qr_generator),
    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),
    path('admin/', admin.site.urls),
    path('cuenta/', include(('users.urls', 'users'), namespace='users')),
    path('cuenta/', include('django.contrib.auth.urls')),
    path('qr/', include(('qr_generator.urls', 'qr_generator'), namespace='qr_generator')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)