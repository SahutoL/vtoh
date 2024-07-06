from django import forms
from .models import PDFDocument

class PDFUploadForm(forms.ModelForm):
    OUTPUT_CHOICES = [
        ('txt', 'TXT'),
    ]
    output_format = forms.ChoiceField(choices=OUTPUT_CHOICES, widget=forms.RadioSelect, label='TXT')

    class Meta:
        model = PDFDocument
        fields = ['file']
