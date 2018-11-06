from django.conf import settings
#from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'^accounts/', include('accounts.urls')),
    # url(r'^mychart/', include('mychart.urls')),
    # url(r'', include('blog.urls', namespace='blog')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('mychart/', include('mychart.urls')),
    path('', include('blog.urls', namespace='blog')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

