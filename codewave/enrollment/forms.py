from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from enrollment.models import (Student, Teacher, classrooms, Enroll_Courses)

class Register_Form(forms.Form):
    username = forms.CharField(max_length=100,
    error_messages = {
        'required': "Please Enter your Username"
    }
    )
    email = forms.EmailField(error_messages = {
                 'required':"Please Enter your Email"
                 })
    password1 = forms.CharField(label="Password",
                                max_length=50,
                                widget=forms.PasswordInput(),
                                error_messages={
                                    'required': "Please Enter your password"
                                }
                                )
    password2 = forms.CharField(label="Confirm Password",
                                max_length=50,
                                widget=forms.PasswordInput(),
                                error_messages={
                                    'required': "Please Enter Confirm Password"
                                }
                                )

    # def clean(self):
    #     super(Register_Form, self).clean()
    #     # This method will set the `cleaned_data` attribute
    #
    #     username = self.cleaned_data.get('username')
    #     eamil = self.cleaned_data.get('email')
    #     password = self.cleaned_data.get('password')
    #     if len(username) | len(eamil) | len(password) == 0:
    #         raise ValidationError('field should not be blank')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) == 0:
            raise forms.ValidationError("User name should not be blank")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        u_email = User.objects.filter(email=email)
        if u_email:
            raise forms.ValidationError("Entered Eamil id already exists!!!")
        elif len(email) == 0:
            raise forms.ValidationError("Email field should not be blank")
        else:
            return email

    def clean_password2(self):

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password Do Not Matched!!!")
        elif len(password1) == 0 | len(password2) == 0:
            raise forms.ValidationError("Password should not be blank")
        else:
            return password2
