from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from manage.models import UploadFileForm, NewDirForm
from subprocess import call
import os, time
from stat import *

# location where files of each user will be stored
data_root = 'user_data/'
shared_dir = 'shared/'

# the decorator prevents access and redirects users who have not logged in
@login_required(redirect_field_name='/login')
def new_dir(request):
    '''Creates new folder for user inside current dir'''
    # extract directory from URL
    curr_dir = request.path.split('/')[2:]
    curr_dir = '/'.join(curr_dir)

    user = request.user.username

    # if user submitted a new file for upload
    if request.method == 'POST':
        dir_name = request.POST.get('directory')
        dir_name = sanitize(dir_name)
        dir_path = curr_dir + '/' + dir_name

        # put user-entered information in form
        form = NewDirForm(request.POST)

        # if form is ok, create the dir and return user to this page
        if form.is_valid():
            handle_new_dir(user, dir_path)

    return HttpResponseRedirect('/manage/' + curr_dir)

# the decorator prevents access and redirects users who have not logged in
@login_required(redirect_field_name='/login')
def delete(request):
    '''Deletes the file/dir user wanted to delete'''
    # extract directory from URL
    curr_dir = request.path.split('/')[2:-1]
    curr_dir = '/'.join(curr_dir)

    file_path = request.path.split('/')[2:]
    file_name = file_path[-1]
    file_path = '/'.join(file_path)

    user = request.user.username

    # system call to remove the file
    call(['rm', '-rf', data_root + user + '/' + file_path])
    # system call to remove the file from shared files as well
    call(['rm', '-rf', shared_dir + file_name])

    return HttpResponseRedirect('/manage/' + curr_dir)

# the decorator prevents access and redirects users who have not logged in
@login_required(redirect_field_name='/login')
def download(request):
    '''Serves the file user clicked on'''
    # extract path from URL
    file_path = request.path.split('/')[2:]
    file_name = file_path[-1]
    file_path = '/'.join(file_path)

    user = request.user.username
    user_file = open(data_root + user + '/' + file_path)

    return serve_download(user_file, file_name)

@login_required(redirect_field_name='/login')
def download_shared(request):
    '''Serves the file user clicked on in the shared list'''
    # extract file name from URL
    file_name = request.path.split('/')[-1]

    shared_file = open(shared_dir + file_name)

    return serve_download(shared_file, file_name)

def serve_download(fl, file_name):
    '''Actually return the file fl to the user'''
    # create a response for downloading; make the file an attachment
    response = HttpResponse(fl, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="'+file_name+'"'
    return response

# the decorator prevents access and redirects users who have not logged in
@login_required(redirect_field_name='/login')
def show_shared(request):
    '''Displays the files users decided to share publicly'''
    dir_data = get_dir_data('..', shared_dir)

    # load the page with the shared files
    return render_to_response('shared.html', {'dir_data': dir_data}, RequestContext(request))


# the decorator prevents access and redirects users who have not logged in
@login_required(redirect_field_name='/login')
def upload(request):
    '''Displays uploaded files and lets users upload new files in current dir'''
    try:
        # extract directory from URL
        curr_dir = request.path.split('/')[2:]
        if curr_dir[0]:
            curr_dir = '/'.join(curr_dir) + '/'
        else:
            curr_dir = ''

        # set the prev_dir for the Go Up link to go 1 step up in path
        prev_dir = request.path.split('/')[2:-1]
        prev_dir = '/'.join(prev_dir)

    except IndexError: # user just logged in or registered
        curr_dir = ''
        prev_dir = ''

    user = request.user.username

    # if user submitted a new file for upload
    if request.method == 'POST':
        # put user-entered information in form
        form = UploadFileForm(request.POST, request.FILES)

        # if form is ok, save the file and return user to this page
        if form.is_valid():
            file_name = request.POST.get('title')
            if request.POST.get('to_share'):
                # save the file to shared files dir
                handle_shared_file(request.FILES['file'], file_name)

            # save uploaded file to user's dir
            handle_uploaded_file(request.FILES['file'], user, file_name, curr_dir)

    # just empty form now when loading page
    form = UploadFileForm()

    # get files and dirs in curr_dir
    dir_data = get_dir_data(user, curr_dir)

    # load the page with the form and the user's files
    return render_to_response('upload.html', 
                             {'form': form, 'dir_data': dir_data, 'curr_dir': curr_dir, 'prev_dir': prev_dir}, 
                             RequestContext(request))

def get_dir_data(user, curr_dir):
    '''Returns a dictionary of files/dirs and file info for specified user and dir'''
    curr_dir = data_root + user + '/' + curr_dir
    dir_data = {}

    try:
        # iterate through all files and dirs in current dir
        for fd in os.listdir(curr_dir):
            file_path = curr_dir + '/' + fd

            if os.path.isfile(file_path):
                # get size and last modification time for each file
                file_stats = os.stat(file_path)
                file_size = 'File size: ' + str(file_stats[ST_SIZE]) + ' bytes'
                last_mod_time = 'Last modified on ' + str(time.asctime(time.localtime(file_stats[ST_MTIME])))

                # store the information for this file
                dir_data[fd] = [file_size, last_mod_time]

            else:
                # this is a dir, only get last_mod_time
                dir_stats = os.stat(file_path)
                last_mod_time = 'Last modified on ' + str(time.asctime(time.localtime(dir_stats[ST_MTIME])))

                dir_data[fd] = [last_mod_time]

    except: # new user, doesn't have a directory yet, so just don't display files
        pass
    
    return dir_data

def sanitize(user_input):
    '''Remove dangerous characters from user_input'''
    user_input = user_input.replace(' ', '')
    user_input = user_input.replace('.', '')
    user_input = user_input.replace('/', '')
    user_input = user_input.replace(';', '')
    return user_input

def handle_new_dir(user, dir_path):
    '''Helper function to create directory for user'''
    # create a dir for the user (error is ignored if it already exists)
    res = call(['mkdir', data_root + user + '/' + dir_path]) 

def handle_shared_file(f, file_name):
    '''Helper function to write uploaded file to disk to shared'''
    write_uploaded_file(f, shared_dir + file_name)

def handle_uploaded_file(f, user, file_name, curr_dir):
    '''Helper function to write uploaded file to disk to user's curr dir'''
    # create a dir for the user (error is ignored if it already exists)
    res = call(['mkdir', data_root + user])

    # create the uploaded file with user-entered file_name (title)
    curr_dir = data_root + user + '/' + curr_dir
    file_path = curr_dir + '/' + file_name

    write_uploaded_file(f, file_path)

def write_uploaded_file(f, file_path):
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)



