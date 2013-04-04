from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from manage.models import UploadFileForm
from subprocess import call
import os, time
from stat import *

data_root = 'user_data/'

@login_required(redirect_field_name='/login')
def upload(request):
    user = request.user.username
    if request.method == 'POST':
        file_name = request.POST.get('title')
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], user, file_name)
            return HttpResponseRedirect('/manage')
    else:
        form = UploadFileForm()
    
    files = {}
    try:
        for f in os.listdir(data_root + user):
            file_stats = os.stat(data_root + user + '/' + f)
            file_size = 'File size: ' + str(file_stats[ST_SIZE]) + ' bytes'
            last_mod_time = 'Last modified on ' + str(time.asctime(time.localtime(file_stats[ST_MTIME])))
            files[f] = [file_size, last_mod_time]
    except: # new user, doesn't have a directory yet
        pass

    return render_to_response('upload.html', {'form': form, 'files':files}, RequestContext(request))

def handle_uploaded_file(f, user, file_name):
    res = call(['mkdir', data_root+user])
    file_path = data_root + user + '/' + file_name
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
