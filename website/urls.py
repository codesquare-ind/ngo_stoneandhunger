from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('public.urls')),
    path('', include('projects.urls')),
    path('', include('account.urls')),
    path('', include('blog.urls')),
    path('', include('events.urls')),
    path('', include('spotlight.urls')),
    path('a/', include('administration.urls')),
    path('api/account/', include('account.api.urls')),
    path('api/projects/', include('projects.api.urls')),
    path('api/blog/', include('blog.api.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

handler404 = 'public.views.pg_not_found_error'

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
