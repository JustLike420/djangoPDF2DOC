import mimetypes
import pdfkit
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from pdf2docx import Converter
from djangoPDF2DOC.settings import BASE_DIR
import tabula
from pdf2jpg import pdf2jpg
import jpg2pdf
from .models import UsersFiles
from django.core.files import File


def home(request):
    return render(request, 'home.html')


def save_file_user(request, path):
    with open(path, mode='rb') as f:
        if request.user.is_authenticated:
            item = UsersFiles.objects.create(
                user=request.user,
                file=File(f, name=path.split("\\")[-1]),
            )
        else:
            item = UsersFiles.objects.create(
                file=File(f, name=path.split("\\")[-1]),
            )
        item.save()


def convert_pdf_docx(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        if uploaded_file.content_type == 'application/pdf':
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            uploaded_file_url = fs.url(filename)
            output_file_url = str(BASE_DIR) + '/media/' + filename.replace('pdf', 'docx')

            cv = Converter(str(BASE_DIR) + uploaded_file_url)
            cv.convert(output_file_url)
            cv.close()

            path = open(output_file_url, 'rb')
            save_file_user(request, output_file_url)
            mime_type, _ = mimetypes.guess_type(output_file_url)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % filename.replace('pdf', 'docx')
            return response
    return render(request, 'pdf_docx.html')


def convert_pdf_excel(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        if uploaded_file.content_type == 'application/pdf':
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            uploaded_file_url = fs.url(filename)
            output_file_url = str(BASE_DIR) + '/media/' + filename.replace('pdf', 'xlsx')

            cv = tabula.read_pdf(str(BASE_DIR) + uploaded_file_url, pages='all')[0]
            cv.to_excel(output_file_url)
            save_file_user(request, output_file_url)
            path = open(output_file_url, 'rb')
            mime_type, _ = mimetypes.guess_type(output_file_url)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % filename.replace('pdf', 'xlsx')
            return response
    return render(request, 'pdf_excel.html')


def convert_pdf_jpg(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        if uploaded_file.content_type == 'application/pdf':
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            uploaded_file_url = fs.url(filename)

            result = pdf2jpg.convert_pdf2jpg(str(BASE_DIR) + uploaded_file_url, str(BASE_DIR) + '/media/', dpi=300,
                                             pages="ALL")
            output_file_url = result[0]['output_jpgfiles'][0]
            save_file_user(request, output_file_url)
            path = open(output_file_url, 'rb')
            mime_type, _ = mimetypes.guess_type(output_file_url)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % filename.replace('pdf', 'jpg')

            return response
    return render(request, 'pdf_excel.html')


def convert_jpg_pdf(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        if uploaded_file.content_type == 'image/jpeg':
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            uploaded_file_url = fs.url(filename)
            output_file_url = str(BASE_DIR) + '/media/' + filename.replace('jpg', 'pdf')

            with jpg2pdf.create(output_file_url) as pdf:
                pdf.add(str(BASE_DIR) + uploaded_file_url)
            save_file_user(request, output_file_url)
            path = open(output_file_url, 'rb')
            mime_type, _ = mimetypes.guess_type(output_file_url)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % filename.replace('jpg', 'pdf')
            return response
    return render(request, 'jpg_pdf.html')


def convert_hmtl_pdf(request):
    uploaded_file = request.FILES['document']
    if uploaded_file.content_type == 'text/html':
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        uploaded_file_url = fs.url(filename)
        output_file_url = str(BASE_DIR) + '/media/' + filename.replace('html', 'pdf')

        path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        try:
            # либа выдает какую-то ошибку.
            pdfkit.from_file(str(BASE_DIR) + uploaded_file_url, output_file_url, configuration=config)
        except:
            pass
        save_file_user(request, output_file_url)
        path = open(output_file_url, 'rb')
        mime_type, _ = mimetypes.guess_type(output_file_url)
        response = HttpResponse(path, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename.replace('html', 'pdf')
        return response
    return render(request, 'html_pdf.html')
