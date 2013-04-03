# Create your views here.Q
from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User, Group
from django.forms import ModelForm
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.shortcuts import render_to_response, redirect

def index(request):
	return render_to_response('index.html')

def upload(request):
	#print request
	return render_to_response('upload.html')

def login(request):
	return render_to_response('login.html')
