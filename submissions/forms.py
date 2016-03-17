from django.forms import ModelForm
from django import forms
from submissions.models import Submissions
from django.utils.translation import ugettext_lazy as _

class TeamDetailsForm(ModelForm):
    language = forms.ChoiceField(chioces=(('C','C'), ('C++', 'C++'), ('Python', 'Python')), required=True)
    class Meta:
        model = Submissions
        fields = ['problemId', 'language', 'solution']
        labels = {
            'problemId': _('Problem ID'),
            'language': _('Language'),
            'solution': _('Solution'),
        }
