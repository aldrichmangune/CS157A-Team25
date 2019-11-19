from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account, Textbook, Category


class AccountCreationForm(UserCreationForm):
    """
    Form to validate user input when creating Accounts
    """

    class Meta:
        model = Account
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class' : 'form-control'}),
            'first_name': forms.TextInput(attrs={'class' : 'form-control'}),
            'last_name': forms.TextInput(attrs={'class' : 'form-control'}),
        }


class AccountChangeForm(forms.ModelForm):
    """
    Form to validate user input when changing an Account information
    """
    password_confirm = forms.CharField(required=True, label='Password Confirmation', widget=forms.PasswordInput(attrs={'class' : 'form-control'}));

    # Form validation checks if password field equals to password_confirm field, add an error if not
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

    """
    Form to validate user input when submitting a new Textbook Listing
    """

    Price = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}),label="Price", required=True);

    # Selection field for the Categories in the database
    Category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple(), required=True);

    class Meta:
        model = Textbook;
        fields = ('ISBN', 'Title', 'Image', 'Author', 'Date_Published', 'Publisher', 'Cond', 'Description')
        widgets = {
            'ISBN': forms.NumberInput(attrs={'class' : 'form-control'}),
            'Title': forms.TextInput(attrs={'class' : 'form-control'}),
            'Author': forms.TextInput(attrs={'class' : 'form-control'}),
            'Publisher': forms.TextInput(attrs={'class' : 'form-control'}),
            'Description': forms.Textarea(attrs={'class' : 'form-control'}),
            'Date_Published' : forms.SelectDateWidget(years=range(1900,2020)),
        }

class TextbookChangeForm(forms.ModelForm):

    """
    Form to validate the user input when editing listing information
    """

    Price = forms.FloatField(widget=forms.NumberInput(),label="Price", required=True);
    Category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple(), required=True);

    class Meta:
        model = Textbook;
        fields = ('ISBN', 'Title', 'Image', 'Author', 'Date_Published', 'Publisher', 'Cond', 'Description')
        widgets = {
            'ISBN': forms.NumberInput(attrs={'class' : 'form-control'}),
            'Title': forms.TextInput(attrs={'class' : 'form-control'}),
            'Author': forms.TextInput(attrs={'class' : 'form-control'}),
            'Publisher': forms.TextInput(attrs={'class' : 'form-control'}),
            'Description': forms.Textarea(attrs={'class' : 'form-control'}),
            'Date_Published' : forms.SelectDateWidget(years=range(1900,2020)),
        }
