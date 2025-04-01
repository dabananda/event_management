from django import forms
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from events.mixins import TailwindFormMixin
from .models import Profile


class RegisterForm(TailwindFormMixin, UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']


class LoginForm(TailwindFormMixin, AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ['username', 'password']


class AssignRoleForm(TailwindFormMixin, forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a role"
    )


class CreateGroupForm(TailwindFormMixin, forms.ModelForm):
    permission = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assign permissions",
    )

    class Meta:
        model = Group
        fields = ['name']


class ProfileUpdateForm(TailwindFormMixin, forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = Profile
        fields = ['phone_number', 'profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].required = False
        self.fields['profile_picture'].required = False
