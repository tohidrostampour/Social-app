from django import forms


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
