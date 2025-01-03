#url:
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Users.urls')),
    path('', include('community.urls')),
    path('payments/', include('payments.urls')), 
    path('messages/', include('message.urls')),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
