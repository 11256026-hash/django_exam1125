from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from grades import views as grades_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', grades_views.home_view, name='home'),
    path('grades/', include('grades.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
