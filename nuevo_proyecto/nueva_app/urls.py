from django.urls import path
from . import views
from .views import PostListView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView
from .views import TagListView, TagCreateView, TagDeleteView, PostbyTagView
from . import views_debug
from django.conf import settings
from nueva_app.views import pais_info, peliculas

urlpatterns = [
    path('', views.home, name='home' ),
    path('login/', views.loginView, name='login'),
    path('registro/', views.registroView, name='registro'),
    path('logout/', views.logoutView, name='logout'),
    path('post/', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('new/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('tags/', TagListView.as_view(), name='tag_list'),
    path('tags/newtag/', TagCreateView.as_view(), name='tag_create'),
    path('tags/<int:pk>/delete/', TagDeleteView.as_view(), name='tag_delete'),
    path('post_by_tag/<int:pk>/', PostbyTagView.as_view(), name='post_list_by_tag'),
    path('politica-cookies/', views.politica_cookies, name='politica_cookies'),
    path('weather/', views.weather, name='weather'),
    path('pais/', pais_info, name='pais_info'),
    path('peliculas/', peliculas, name='peliculas'),

]


if settings.DEBUG:
    urlpatterns += [
        path("__debug/500/", views_debug.debug_500, name="debug_500"),
        path("__debug/403/", views_debug.debug_403, name="debug_403"),
        path("__debug/404/", views_debug.debug_404, name="debug_404"),
    ]