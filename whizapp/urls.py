from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
  
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('home/<str:qid>/',views.post_detail,name='post_detail'),
    path('home/<str:qid>/<str:cid>',views.reply,name='reply'),
    path('reset/<str:hash>', views.reset, name='reset'),
    path('forget/', views.forget, name='forget'),

]
urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)