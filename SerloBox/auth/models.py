from django.db import models
from django.forms import ModelForm

# Create your models here.
#class UserField(models.CharField)

class acctForm(ModelForm):
	class Meta:
		model = acct
		fields = ('username', 'password')

class acct(models.Model):
	username = models.CharField(max_length=10)
	password = models.CharField(max_length=16)

