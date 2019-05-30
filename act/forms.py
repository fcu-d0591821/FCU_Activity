from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.db.models import EmailField
from django.utils.translation import ugettext_lazy as _
from .models import ExtendUser, Activity

DATE_ATTR = {
    'type': 'datetime-local',
    'class': 'form-control'
}
TEXT_ATTR = {
    'class': 'form-control'
}
FILE_ATTR = {
    'class': 'form-control-file'
}

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
        labels = {
            'title': '標題',
            'start': '開始時間',
            'end': '結束時間',
            'description': '活動敘述',
            'poster': '海報'
        }
        widgets = {
            'title': forms.TextInput(TEXT_ATTR),
            'start': forms.DateTimeInput(DATE_ATTR),
            'end': forms.DateTimeInput(DATE_ATTR),
            'description': forms.Textarea(TEXT_ATTR),
            'poster': forms.FileInput(FILE_ATTR)
        }
