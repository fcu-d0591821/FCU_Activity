from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.db.models import EmailField
from django.utils.translation import ugettext_lazy as _
from .models import ExtendUser, Activity

class ExtendUserAdminForm(forms.ModelForm):
    class Meta:
        model = ExtendUser
        fields = '__all__'

class ExtendUserCreationForm(UserCreationForm):
    email = EmailField(_('email address'))

    class Meta:
        fields = ('username', 'email', 'studentId', 'nickName')
        model = ExtendUser
        field_classes = {'username': UsernameField}

class ActivityAdminForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'

class ActivityCreateForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ('title', 'start', 'end', 'description', 'poster')
