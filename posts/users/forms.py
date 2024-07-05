from django import forms


class LoginUserForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'type': 'email',
            'class': 'form-control rounded-3',
            'id': 'floatingInput',
            'placeholder': 'name@example.com'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'type': 'password',
            'class': 'form-control rounded-3',
            'id': 'floatingPassword',
            'placeholder': 'Password'

        })
    )


class RegistrationUserForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'type': 'email',
            'class': 'form-control rounded-3',
            'id': 'floatingInput',
            'placeholder': 'name@example.com'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'type': 'password',
            'class': 'form-control rounded-3',
            'id': 'floatingPassword1',
            'placeholder': 'Password'

        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'type': 'password',
            'class': 'form-control rounded-3',
            'id': 'floatingPassword2',
            'placeholder': 'Password'

        })
    )

