from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from .models import Profile

# messages = {
#     'required' : 'این فیلد اجباری است',
#     'invalid':'لطفا یک ایمیل معتبر وارد کنید'
# }


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(max_length=40, widget=forms.PasswordInput(attrs={'class':'form-control',
        'aria-describedby':'passwordHelpBlock'}))

class UserRegisterationForm(forms.Form):
    username = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(min_length=8,max_length=40, widget=forms.PasswordInput(attrs={'class':'form-control',
        'aria-describedby':'passwordHelpBlock'}))


class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = Profile
        fields = ['bio','age','phone']
        widgets = {
            'bio' : forms.TextInput(attrs={'class':'form-control'}),
        }


class PhoneLoginForm(forms.Form):
    phone = forms.IntegerField()


    def clean_phone(self):
        phone = Profile.objects.filter(phone=self.cleaned_data['phone'])
        if not phone.exists():
            raise ValidationError('This Phone Does Not Exists')
        return self.cleaned_data['phone']


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()
    