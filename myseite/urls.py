from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views

def has_permission(request):
    return request.user.is_active

admin.site.site_header = 'システム管理者サイト'
admin.site.site_title = 'マイプロジェクト'
admin.site.index_title = 'ホーム'
admin.site.site_url = None
admin.site.has_pemission = has_permission

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('plants.urls')),
    path('account/', include('account.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
