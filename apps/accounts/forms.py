from typing import Any
from django import forms
from django.forms.widgets import TextInput, PasswordInput, EmailInput
from .models import User, UserResetPassword
from apps.accounts.utilits import CODE_LENGTH, GenerateNewPassword, send_mail_code


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(widget=TextInput(attrs={'placeholder':'username:'}), required=False)
    email = forms.EmailField(widget=TextInput(attrs={'placeholder':'email manzilingizni kiriting:'}), required=True)
    first_name = forms.CharField(widget=TextInput(attrs={'placeholder':'ismingizni kiriting:'}), required=True)
    last_name = forms.CharField(widget=TextInput(attrs={'placeholder':'familiyangizni kiriting:'}), required=True)
    phone = forms.CharField(widget=TextInput(attrs={'placeholder':'telefon nomeringizni kiriting:'}), required=False)
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'password:'}), required=True)
    confirm_password = forms.CharField(widget=TextInput(attrs={'placeholder':'confirm password...'}), required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu email avval ro\'yxatdan o\'tgan, iltimos boshqa email kiriting:')
        return email
    
    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        if password1 != password2:
            raise forms.ValidationError('Parollar bir-biriga mos emas!!!')
        return password2
    
    def save(self, commit=True):
        password = self.cleaned_data.get('password')
        user = super().save(commit)
        user.username = self.cleaned_data.get('email')
        user.set_password(password)
        user.save()

        return user

class LoginForm(forms.Form):
    email = forms.EmailField(widget=EmailInput(attrs={'placeholder':'Emailingizni kiriting:'}), required=True)
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password kiriting:'}), required=True)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if not email or not password:
            raise forms.ValidationError('Bo\'sh bo\'lmasligi kerak!!!')
        return self.cleaned_data
    
    
    
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'birth')
        
        
class ResetPasswordForm(forms.ModelForm):
    email = forms.EmailField(widget=TextInput(attrs={'placeholder':'emailingizni kiriting:'}), required=True)
    
    class Meta:
        model = UserResetPassword
        fields  =('email',)
    
    def clean(self):
        email = self.cleaned_data.get('email')
        is_email = User.objects.filter(email=email).exists()
        if not is_email:
            raise forms.ValidationError("Bunday emailga ega foydalanuvchi topilmadi...")
        return self.cleaned_data

    def save(self, commit=True):
        email = self.cleaned_data.get('email')
        change_pass = super().save()
        
        new_pass = GenerateNewPassword().new_password()
        # send_mail_code(email, new_pass)
        
        print("user new password: ", new_pass)
        user = User.objects.get(email=email)
        user.set_password(new_pass)
        user.save()

        return change_pass

class UpdatePasswordForm(forms.Form):
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'eski parolni kiriting:'}), required=True)
    new_password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'yangi parol kiriting:'}), required=True)
    password_confirm = forms.CharField(widget=PasswordInput(attrs={'placeholder':'yangi parolni tasdiqlang:'}), required=True)

    def __init__(self, user, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)
        self.user = user
        
    def clean_password(self):
        valid = self.user.check_password(self.cleaned_data['password'])
        if not valid:
            raise forms.ValidationError('Eski parolni no\'to\'g\'ri kiritdingiz. Iltimos qaytadan kiriting')
    
        if self.cleaned_data.get('new_password') != self.cleaned_data.get('password_confirm'):
            raise forms.ValidationError('Parollar bir-biriga mos kelmadi. Parollar bir xil kiritilsin.')
        return self.cleaned_data





    



    
