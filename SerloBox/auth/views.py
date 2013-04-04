# Create your views here.
from django.shortcuts import render_to_response
from django.template import Context, RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import *

def login_user(request):
    state = "Please log in below..."
    username = ''
    password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        print username 
        print password 
        user = authenticate(username=username, password=password)
        print user
        
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
                return HttpResponseRedirect("/manage/")
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."
    return render_to_response('auth.html',{'state':state, 'username': username}, context_instance=RequestContext(request))

def register_user(request):
    state = "Please register below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if username and password and email:
            user = User.objects.create_user(username, email)
            # user was created
            if user:
                user.set_password(password)
                user.save()
                state = "Your account was created successfully!"
                login(request, user)
                return HttpResponseRedirect("/manage/")

            else:
                print "fail"
        # request was empty
        else:
            print "empty"
            

    return render_to_response('register.html',{'state':state, 'username': username}, RequestContext(request))

@login_required
def manage(request):
    # if not request.user.is_authenticated():
    #     return render_to_response('auth.html', {'state':"You must be logged in."})
    return render_to_response('manage.html')
    
def mylogout(request):    

    logout(request)
    return HttpResponseRedirect('/login/')