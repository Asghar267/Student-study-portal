from dataclasses import field
import imp
from django import forms
from . models import *
from django.contrib.auth.forms import UserCreationForm
class Notesform(forms.ModelForm):

    class Meta:
        model = Notes
        fields = ['title', 'description']

class DateInput(forms.DateInput):
    input_type = 'date'


class Homeworkform(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due':DateInput()}
        fields = ['subject','title', 'description','due','is_finished']

class DashboardForm(forms.Form):
    text = forms.CharField(max_length=200,label="Enter Your Search")


class Todoform(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','is_finished']

class ConversionForm(forms.Form):
    CHOICES =[('length','Length'),('mass','Mass')]
    measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

class ConversionLengthForm(forms.Form):
    CHOICES =[('yard','Yard'),('foot','Foot')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs={'type':'number','placeholder':'Enter the number'}
    ))

    measure1 = forms.CharField(
        label='', widget=forms.Select(choices= CHOICES)
    )
    measure2 = forms.CharField(
        label='', widget=forms.Select(choices= CHOICES)
    )

class ConversionMassForm(forms.Form):
    CHOICES =[('pound','Pound'),('kilogram','Kilogram')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs={'type':'number','placeholder':'Enter the number'}
    ))

    measure1 = forms.CharField(
        label='', widget=forms.Select(choices= CHOICES)
    )
    measure2 = forms.CharField(
        label='', widget=forms.Select(choices= CHOICES)
    )
    
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']