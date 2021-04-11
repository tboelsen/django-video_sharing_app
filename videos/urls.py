from django.urls import path
from .views import HomePageView, ThemeCreateView, DashboardView, ThemeDetailView, ThemeUpdateView, ThemeDeleteView, AddVideoView, VideoSearchView, VideoDeleteView

urlpatterns = [
    path('', HomePageView, name='home'),
    path('dashboard/', DashboardView, name='dashboard'),
    path('themes/create/', ThemeCreateView.as_view(), name='create_theme'),
    path('themes/<int:pk>', ThemeDetailView.as_view(), name='detail_theme'),
    path('themes/<int:pk>/update/', ThemeUpdateView.as_view(), name='update_theme'),
    path('themes/<int:pk>/delete/', ThemeDeleteView.as_view(), name='delete_theme'),
    path('themes/<int:pk>/addvideo/', AddVideoView, name='add_video'),
    path('video/search/', VideoSearchView, name='video_search'),
    path('video/<int:pk>/delete/', VideoDeleteView.as_view(), name='delete_video'),
]
