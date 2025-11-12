from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('backend/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('backend/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', RedirectView.as_view(url='/backend/swagger/')),
    path('backend/', include('core.urls')),
]
