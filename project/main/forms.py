from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import Account, Textbook

class AccountCreationForm(UserCreationForm):

    class Meta:
        model = Account
        fields = ('username', 'email', 'first_name', 'last_name')


class AccountChangeForm(forms.ModelForm):

    password_confirm = forms.CharField(required=True, label='Password Confirmation', widget=forms.PasswordInput(attrs={'class' : 'form-control'}));

    def clean_password_confirm(self):
        if self.cleaned_data['password'] != self.data['password_confirm']:
            self.add_error('password_confirm', "Password confirmation field doesn't match password field!")
        return self.cleaned_data['password']
    class Meta:
        model = Account
        fields = ('Profile_Picture','email', 'first_name', 'last_name', 'password',)
        widgets = {
            'email': forms.EmailInput(attrs={'class' : 'form-control'}),
            'first_name': forms.TextInput(attrs={'class' : 'form-control'}),
            'last_name': forms.TextInput(attrs={'class' : 'form-control'}),
            'password': forms.PasswordInput(attrs={'class' : 'form-control'}),
        }

class TextbookCreationForm(forms.ModelForm):
    Date = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2020)), label='Date Published', required=True, initial=timezone.now())
    class Meta:
        model = Textbook;
        fields = ('ISBN', 'Title', 'Image', 'Author', 'Publisher', 'Condition', 'Description')
        widgets = {
            'ISBN': forms.NumberInput(attrs={'class' : 'form-control'}),
            'Title': forms.TextInput(attrs={'class' : 'form-control'}),
            'Author': forms.TextInput(attrs={'class' : 'form-control'}),
            'Publisher': forms.TextInput(attrs={'class' : 'form-control'}),
            'Description': forms.Textarea(attrs={'class' : 'form-control'}),
        }
