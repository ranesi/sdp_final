from django import forms
from .models import Document, Profile

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import ValidationError

BLANK_FIELD = "Field cannot be blank."
DUPLICATE = "%s taken."


class AddDocumentForm(forms.ModelForm):

    class Meta:

        model = Document
        fields = ('title', 'text',)

    # ########################################
    # # The following MAY be used eventually
    # # ... figured that they should be included
    # #
    # def clean_title(self):
    #
    #     title = self.cleaned_data['title']
    #
    #     if not title:
    #         ValidationError(BLANK_FIELD)
    #
    #     return title
    #
    # def clean_text(self):
    #
    #     text = self.cleaned_data['text']
    #
    #     if not text:
    #         ValidationError(BLANK_FIELD)
    #
    #     return text
    #
    # def save(self, commit=True):
    #
    #     document = super(AddDocumentForm, self).save(commit=False)
    #     document.title = self.cleaned_data['title']
    #     document.text = self.cleaned_data['text']
    #
    #     if commit:
    #         # document.submit()
    #         document.save()
    #
    #     return document()
    # #
    # ########################################


class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')

    def clean_username(self):

        field = 'Username'

        username = self.cleaned_data['username']

        if not username:
            raise ValidationError(DUPLICATE % field)

        if User.objects.filter(username__icontains=username).exists():
            raise ValidationError('Username taken!')

        return username

    def clean_first_name(self):

        first_name = self.cleaned_data['first_name']

        if not first_name:
            raise ValidationError(BLANK_FIELD)

        return first_name

    def clean_last_name(self):

        last_name = self.cleaned_data['last_name']

        if not last_name:
            raise ValidationError(BLANK_FIELD)

        return last_name

    def clean_email(self):

        field = 'Email'

        email = self.cleaned_data['email']

        if not email:
            raise ValidationError(BLANK_FIELD)

        if User.objects.filter(email__iexact=email).exists():
            ValidationError(DUPLICATE % field)

        return email

    def save(self, commit=True):

        user = super(CreateUserForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user


class UserProfileForm(forms.ModelForm):

    """...included in case social functionality will be included (eventually)"""

    class Meta:
        model = Profile
        fields = ['description', 'website_url']

