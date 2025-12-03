from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
import django.conf.urls
import home.views
from config import settings

urlpatterns = [
    path('ga-moazzen-manager/', admin.site.urls),
    path('', include('home.urls')),
]

django.conf.urls.handler404 = home.views.handler_404

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
