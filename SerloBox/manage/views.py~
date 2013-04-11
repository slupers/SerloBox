from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from manage.models import UploadFileForm
from subprocess import call
import os, time
from stat import *

# location where files of each user will be stored
data_root = 'user_data/'

# the decorator prevents access and redirects users who have not logged in
@login_required(redirect_field_name='/login')
def delete(request):
    '''Deletes the file user wanted to delete'''
    file_name = request.path.split('/')[-1]
    user = request.user.username
    # system call to remove the file
    call(['rm', data_root + user + '/' + file_name])

    form = UploadFileForm()
    files = display_files(user)
    # load the page with the form and the user's files
    return render_to_response('upload.html', {'form': form, 'files':files}, RequestContext(request))

def display_files(user):
    '''Returns a dictionary of files and file info for specified user'''
    # display user's files
    files = {}
    try:
        # iterate through all files in user's dir
        for f in os.listdir(data_root + user):
            # get size and last modification time for each file
            file_stats = os.stat(data_root + user + '/' + f)
            file_size = 'File size: ' + str(file_stats[ST_SIZE]) + ' bytes'
            last_mod_time = 'Last modified on ' + str(time.asctime(time.localtime(file_stats[ST_MTIME])))

            # store the information for this file
            files[f] = [file_size, last_mod_time]

    except: # new user, doesn't have a directory yet, so just don't display files
        pass

    return files

# the decorator prevents access and redirects users who have not logged in
@login_required(redirect_field_name='/login')
def download(request):
    '''Serves the file user clicked on'''
    file_name = request.path.split('/')[-1]
    user = request.user.username
    user_file = open(data_root + user + '/' + file_name)

    # create a response for downloading; make the file an attachment
    response = HttpResponse(user_file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="'+file_name+'"'
    return response


# the decorator prevents access and redirects users who have not logged in
@login_required(redirect_field_name='/login')
def upload(request):
    '''Displays uploaded files and lets users upload new files'''
    user = request.user.username

    # if user submitted a new file for upload
    if request.method == 'POST':
        file_name = request.POST.get('title')

        # put user-entered information in form
        form = UploadFileForm(request.POST, request.FILES)

        # if form is ok, save the file and return user to this page
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], user, file_name)
            return HttpResponseRedirect('/manage')

    # user didn't try to upload, just loading the page so keep form empty
    else:
        form = UploadFileForm()
    
    files = display_files(user)
    
    # load the page with the form and the user's files
    return render_to_response('upload.html', {'form': form, 'files':files}, RequestContext(request))

def handle_uploaded_file(f, user, file_name):
    '''Helper function to write uploaded file to disk to user's dir'''
    # create a dir for the user (error is ignored if it already exists)
    res = call(['mkdir', data_root+user])

    # create the uploaded file with user-entered file_name (title)
    file_path = data_root + user + '/' + file_name
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

