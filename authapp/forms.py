from django.contrib.auth.models import User
from django import forms
# from .models import Profile
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import UserModel
from django.contrib.auth.forms import PasswordResetForm
from django.forms.widgets import ClearableFileInput

class ImageWidget(ClearableFileInput):
    template_name = 'authapp/image_widget.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['image_url'] = value.url if value else ''
        return context

    def value_from_datadict(self, data, files, name):
        upload = super().value_from_datadict(data, files, name)
        if data.get(name + '-clear') == 'on':
            return False
        return upload

class UserRegistration(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat Password', widget=forms.PasswordInput)
    class Meta:
        model = UserModel
        fields = ('username', 'first_name', 'last_name', 'email', 'user_image', 'user_position', 'user_about')

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Passwords don\'t match.')
            return cd['password2']


class UserEditForm(forms.ModelForm):
    user_about = forms.CharField(widget=forms.Textarea(attrs={'spellcheck': 'true'}), max_length=200)
    user_image = forms.ImageField(widget=ImageWidget, required=False)
    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'email', 'user_image', 'user_position', 'user_about')

    def clean_user_about(self):
        user_about = self.cleaned_data['user_about']
        if len(user_about) > 200:
            raise forms.ValidationError("User about cannot be more than 200 characters")
        return user_about


