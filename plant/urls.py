from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .tasks import notify_upcoming_works
from .views import callback

app_name = 'plant'
urlpatterns = [
    path('', views.index, name='index'),
    path('plants/new/', views.plants_new, name='plants_new'),
    path('plants/<int:pk>/delete/', views.plants_delete, name='plants_delete'),
    path('plants/<int:pk>/edit/', views.plants_edit, name='plants_edit'),
    path('plants/<int:pk>/', views.plants_detail, name='plants_detail'),
    path('users/<int:pk>/', views.users_detail, name='users_detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='plant\login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('callback/', views.callback),
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)