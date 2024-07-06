import os
from django.shortcuts import render
from django.http import FileResponse
from django.conf import settings
from .forms import PDFUploadForm
from pdfminer.high_level import extract_text
import unicodedata

def shift_jis_to_utf8(shift_jis_str):
    """
    Shift_JISエンコードされた文字列をUTF-8に変換

    Args:
        shift_jis_str (str): Shift_JISエンコードされた文字列

    Returns:
        str: UTF-8エンコードされた文字列
    """
    normalized_str = unicodedata.normalize('NFKC', shift_jis_str)
    
    utf8_str = ""
    for char in normalized_str:
        try:
            shift_jis_bytes = char.encode('shift_jis')
            utf8_char = shift_jis_bytes.decode('shift_jis').encode('utf-8').decode('utf-8')
            utf8_str += utf8_char
        except UnicodeEncodeError:
            utf8_str += char

    return utf8_str

def process_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_document = form.save()
            pdf_path = pdf_document.file.path
            result_text = shift_jis_to_utf8(extract_text(pdf_path)).split('\n\n')[:-7]
            os.remove(pdf_path)
            ind = 0
            for i in result_text:
                if '1  ' in i:
                    ind = result_text.index(i)
                    break
            result_text = result_text[ind+1:][::-1]
            story = ''
            for i in result_text:
                try:
                    if type(int(i.split(' ')[0])) == int:
                        pass
                except:
                    story += i.replace('\n', '')
            #story = story.replace('。', '。\n')

            output_path = os.path.join(settings.MEDIA_ROOT, 'output.txt')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(story)

            response = FileResponse(open(output_path, 'rb'))
            response['Content-Disposition'] = 'attachment; filename="output.txt"'
            os.remove(output_path)
            return response

    else:
        form = PDFUploadForm()
    return render(request, 'pdftotxt/upload.html', {'form': form})