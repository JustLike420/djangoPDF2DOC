import mimetypes
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from pdf2docx import Converter
from djangoPDF2DOC.settings import BASE_DIR


def home(request):
    return render(request, 'home.html')


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
            mime_type, _ = mimetypes.guess_type(output_file_url)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % filename.replace('pdf', 'docx')
            return response
    return render(request, 'pdf_docx.html')
