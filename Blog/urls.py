
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = i18n_patterns(
    path(_('admin/'), admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('', include('MyBlog.urls')),
    path(_('ckeditor/'),include('ckeditor_uploader.urls')),
    path(_('account/'), include('account.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    #path(r'^convert/', include('lazysignup.urls')),
    
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
