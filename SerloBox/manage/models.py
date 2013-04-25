from django import forms

class UploadFileForm(forms.Form):
    '''Forms for uploading a file'''
    title = forms.CharField(max_length=50)
    file  = forms.FileField()
    to_share = forms.BooleanField(required=False)

class NewDirForm(forms.Form):
    '''Forms for creating new directory'''
    directory = forms.CharField(max_length=50)
