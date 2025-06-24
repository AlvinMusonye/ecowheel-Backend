from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse  # 👈 Add this import

# 👇 Add this simple root view
def home(request):
    return JsonResponse({"message": "EcoWheel API is live"})

urlpatterns = [
    path('', home),  # 👈 This makes your root URL return a working response
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('bookings/', include('bookings.urls')),
    path('community/', include('community.urls')),
    path('tours/', include('tours.urls')),
    path('impact/', include('impact.urls')),
    path('mpesa/', include('mpesa.urls')),
    path('gallery/', include('gallery.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
