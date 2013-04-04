from django import forms

class UploadFileForm(forms.Form):
    '''Forms for uploading a file'''
    title = forms.CharField(max_length=50)
    file  = forms.FileField()
