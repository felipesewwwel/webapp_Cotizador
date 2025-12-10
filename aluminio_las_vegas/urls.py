from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core import views

router = DefaultRouter()
router.register(r'api/clients', views.ClientViewSet)
router.register(r'api/projects', views.ProjectViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.project_list, name='project_list'),
    path('dashboard/', views.earnings_dashboard, name='dashboard'),
    # URLS de la API
    path('', include(router.urls)),
]