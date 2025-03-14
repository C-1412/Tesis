from django import forms
from django.forms import ModelForm

from core.user.models import User
from django.contrib.auth.models import Group


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autofocus'] = True

    groups = forms.ModelChoiceField(queryset=Group.objects.all(), 
                                    widget=forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%'}))

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'groups', 'area']
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese su email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Ingrese su username'}),
            'password': forms.PasswordInput(render_value=True, attrs={'placeholder': 'Ingrese su password'}),
            'area': forms.Select(attrs={'class': 'form-control', 'style': 'width: 100%'}),
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff', 'first_name', 'last_name', 'image']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
                u.groups.clear()
                if self.cleaned_data['groups']:
                    u.groups.add(self.cleaned_data['groups'])
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'username', 'password', 'image'
        widgets = {
            'email': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su email',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su username',
                }
            ),

        }
        exclude = ['password','user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff', 'groups', 'first_name', 'last_name', 'image']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
