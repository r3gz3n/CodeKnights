from django.forms import ModelForm
from django import forms
from team.models import TeamDetails
from django.utils.translation import ugettext_lazy as _
import hashlib

class TeamDetailsForm(ModelForm):
    class Meta:
        model = TeamDetails
        fields = '__all__'
        labels = {
            'teamName': _('Team Name'),
            'password': _('Password'),
            'member1Name': _('First Member Name'),
            'member1Branch': _('First Member Branch'),
            'member2Name': _('Second Member Name'),
            'member2Branch': _('Second Member Branch'),
            'member3Name': _('Third Member Name'),
            'member3Branch': _('Third Member Branch'),

        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        md5sum = hashlib.md5()
        md5sum.update(password)
        hashed_password = md5sum.hexdigest()
        return hashed_password


class TeamPassForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = TeamDetails
        fields = ['teamName', 'password']
        labels = {
            'teamName': _('Team Name'),
            'password': _('Password'),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        md5sum = hashlib.md5()
        md5sum.update(password)
        hashed_password = md5sum.hexdigest()
        return hashed_password



