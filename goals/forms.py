from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class GoalForm(forms.Form):
    use_required_attribute = False
    title = forms.CharField(label='Title')
    description = forms.CharField(label='Description', widget=forms.Textarea())


class LoginForm(forms.Form):
    use_required_attribute = False
    email = forms.EmailField(label='email')
    password = forms.CharField(label='password', widget=forms.PasswordInput())

    def clean_email(self):
        # will be populated with any data that has survived so far
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            # if the validation error is raised, the form will display an error message at the top of the form (normally) describing the problem.
            raise forms.ValidationError(
                "An account with this email address does not exist.")
        return self.cleaned_data['email']


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
























# class GoalForm(forms.ModelForm):
#     use_required_attribute = False
#     class Meta:
#         model = Goal
#         exclude = ()

#     def __init__(self, *args, **kwargs):
#         super(GoalForm, self).__init__(*args, **kwargs)
#         self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': "What's in your mind"})
#         self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Description'})
