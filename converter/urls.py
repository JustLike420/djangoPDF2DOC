from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import home, convert_pdf_docx

urlpatterns = [
    path('', home, name='home'),
    path('pdf_docx', convert_pdf_docx, name='pdf_docx'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
