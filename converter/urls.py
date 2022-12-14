from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import home, convert_pdf_docx, convert_pdf_excel, convert_jpg_pdf, convert_pdf_jpg, convert_hmtl_pdf

urlpatterns = [
    path('', home, name='home'),
    path('pdf_docx', convert_pdf_docx, name='pdf_docx'),
    path('pdf_excel', convert_pdf_excel, name='pdf_excel'),
    path('jpg_pdf', convert_jpg_pdf, name='jpg_pdf'),
    path('pdf_jpg', convert_pdf_jpg, name='pdf_jpg'),
    path('html_pdf', convert_hmtl_pdf, name='html_pdf'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
