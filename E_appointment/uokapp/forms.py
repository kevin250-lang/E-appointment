from django import forms
from django.contrib.auth.models import User
from uokapp.models import student, staffs, appointment, othersuggestion

"""===================================================== SUGGESTION ======================================================"""

class appointmentform(forms.ModelForm):
    suggestion_date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control'}))
    suggestion_hour = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control'}))
    end_time        = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control'}))
    student_reason  = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    class Meta():
        model   = appointment
        fields  = ('suggestion_date','suggestion_hour','end_time','student_reason')
        widgets = {
            'suggestion_date':forms.DateInput(attrs={'class':'datepicker'}),
        }
        labels = {
            'suggestion_date':('Desire date Yyyy-mm-dd'),
            'suggestion_hour':('Hour Hh:mm'),
            'end_time':('End time Hh:mm'),
        }

class othersuggestionform(forms.ModelForm):
    suggestion_date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control'}))
    suggestion_hour = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control'}))
    end_time        = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control'}))
    reason          = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    class Meta():
        model   = othersuggestion
        fields  = ('suggestion_date','suggestion_hour','end_time','reason')
        labels  = {
            'suggestion_date':('Desire date Yyyy-mm-dd'),
            'suggestion_hour':('Hour Hh:mm'),
            'end_time':('End time Hh:mm'),
        }

"""======================================================= USERS ========================================================="""
class userform(forms.ModelForm):
    first_name  = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name   = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    username    = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email       = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password    = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta():
        model   = User
        fields  = ('first_name','last_name','username','email','password')

class staffform(forms.ModelForm):
    phone   = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    # faculty = forms.ChoiceField(widget=forms.CheckboxInput(attrs={'class':'form-control'}))
    # campus  = forms.ChoiceField(widget=forms.SelectMultiple(attrs={'class':'form-control'}))
    
    # profile = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}))
    class Meta():
        model   = staffs
        fields  = ('phone','CFO','registror','lecturer','HOD','dean','faculty','campus','profile')

class studentform(forms.ModelForm):
    phone   = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    # campus  = forms.ChoiceField(widget=forms.CheckboxInput(attrs={'class':'form-control'}))
    # depart  = forms.ChoiceField(widget=forms.CheckboxInput(attrs={'class':'form-control'}))
    # session  = forms.ChoiceField(widget=forms.CheckboxInput(attrs={'class':'form-control'}))
    class Meta():
        model   = student
        fields  = ('phone','student','interns','campus','depart','session','profile')
