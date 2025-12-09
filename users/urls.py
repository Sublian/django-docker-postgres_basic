from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from .api import ProtectedTestView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('protected/', ProtectedTestView.as_view()),
]