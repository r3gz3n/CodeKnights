from django.forms import ModelForm
from django import forms
from submissions.models import Submissions
from django.utils.translation import ugettext_lazy as _

problemIds = (
    ('Hello_World', 'Hello_World'),
    ('Sum_Of_Two_Numbers', 'Sum_Of_Two_Numbers'),
    ('Small_Factorial', 'Small_Factorial')
)

class SubmissionsForm(ModelForm):
    language = forms.ChoiceField(choices=(('C','C'), ('C++', 'C++'), ('Python', 'Python')), required = True)
    problemId = forms.ChoiceField(choices = problemIds, required = True)
    class Meta:
        model = Submissions
        fields = ['problemId', 'language']
        labels = {
            'problemId': _('Problem ID'),
            'language': _('Language'),
        }
