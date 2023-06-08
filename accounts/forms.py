from django import forms
from accounts.models import Account,UserProfile

def name_split(name):
    name = name.split("_")
    name_s = ""
    for i in name:
        name_s += i +" "
    return name_s.capitalize()

def add_css_class(form,css_class):
    for field_name in form.fields:
        widget = form.fields[field_name].widget # first_name.widget

        attrs = widget.attrs
        attrs['class'] = f"{attrs.get('class','')} {css_class}".strip()
        attrs['placeholder'] = f"Enter {name_split(field_name)}"
        widget.attrs = attrs

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Account
        fields = ['first_name','last_name','email','phone_number']

    # def __init__(self,*args,**kwargs):
    #     super(RegisterForm,self).__init__(*args,**kwargs)

    def clean(self):
        cleaned_data = super(RegisterForm,self).clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError("Password do not match!")
        

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False,error_messages={'invalid':("Image fiels only")},widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')

    def __init__(self,*args,**kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
