from Shinobi_Network.shinobi_verse import views
from django.urls import path

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('profile/', views.profile_view, name='profile'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),

    path('shinobi/', views.ShinobiListView.as_view(), name='shinobi_list'),
    path('shinobi/<int:pk>/', views.ShinobiDetailView.as_view(), name='shinobi_detail'),
    path('shinobi/create/', views.ShinobiCreateView.as_view(), name='shinobi_create'),
    path('shinobi/<int:pk>/edit/', views.ShinobiUpdateView.as_view(), name='shinobi_update'),
    path('shinobi/<int:pk>/delete/', views.ShinobiDeleteView.as_view(), name='shinobi_delete'),

    path('clans/', views.ClanListView.as_view(), name='clan_list'),
    path('clans/<int:pk>/', views.ClanDetailView.as_view(), name='clan_detail'),
    path('clans/create/', views.ClanCreateView.as_view(), name='clan_create'),
    path('clans/<int:pk>/edit/', views.ClanUpdateView.as_view(), name='clan_update'),
    path('clans/<int:pk>/delete/', views.ClanDeleteView.as_view(), name='clan_delete'),

    path('jutsus/', views.JutsuListView.as_view(), name='jutsu-list'),
    path('jutsus/<int:pk>/', views.JutsuDetailView.as_view(), name='jutsu_detail'),
    path('jutsus/create/', views.JutsuCreateView.as_view(), name='jutsu_create'),
    path('jutsus/<int:pk>/edit/', views.JutsuUpdateView.as_view(), name='jutsu_update'),
    path('jutsus/<int:pk>/delete/', views.JutsuDeleteView.as_view(), name='jutsu_delete'),

    path('like/<str:model_name>/<int:object_id>/', views.like_view, name='like'),
    path('comment/<str:model_name>/<int:object_id>/', views.comment_view, name='comment'),
]