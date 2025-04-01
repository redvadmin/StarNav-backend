from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'navigations', views.NavigationViewSet)
router.register(r'notes', views.UserNoteViewSet)
router.register(r'settings', views.UserSettingsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
] 