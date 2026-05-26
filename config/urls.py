from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ads import views as ads_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ads_views.index, name='index'),
    path('catalog/', ads_views.ad_list, name='ad_list'),
    path('ad/<int:pk>/', ads_views.ad_detail, name='ad_detail'),
    path('ad/create/', ads_views.ad_create, name='ad_create'),
    path('ad/<int:pk>/edit/', ads_views.ad_edit, name='ad_edit'),
    path('ad/<int:pk>/delete/', ads_views.ad_delete, name='ad_delete'),
    path('my-ads/', ads_views.my_ads, name='my_ads'),
    path('account/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)