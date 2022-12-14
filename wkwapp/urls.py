from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('me/', views.me, name='me'),
    path('visitedUser/<int:id>/', views.visitedUser, name='visitedUser'),
    path('visitedUser_knows/<int:id>/', views.visitedUser_knows, name='visitedUser_knows'),
    path('messagesPage/<int:id>/<int:action>/', views.messagesPage, name='messagesPage'),
    path('send_message/<int:id>', views.send_message, name='send_message'),
    path('read_message/<int:id>/<int:action>/', views.read_message, name='read_message'),
    path('everyone/', views.everyone, name='everyone'),
    path('askUser/', views.askUser, name='askUser'),
    path('acceptUser/', views.acceptUser, name='acceptUser'),
    path('know/', views.know, name='know'),
    path('know_requests/', views.know_requests, name='know_requests'),
    path('search_user/', views.search_user, name='search_user')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)