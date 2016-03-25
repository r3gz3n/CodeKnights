from django.forms import ModelForm
from django import forms
from submissions.models import Submissions
from django.utils.translation import ugettext_lazy as _

class SubmissionsForm(ModelForm):
    language = forms.ChoiceField(choices=(('C','C'), ('C++', 'C++'), ('Python', 'Python')), required=True)
    class Meta:
        model = Submissions
        fields = ['problemId', 'language']
        labels = {
            'problemId': _('Problem ID'),
            'language': _('Language'),
        }
