from django import forms
from django.contrib.auth import get_user_model
from shinobi_verse.models import Shinobi, Clan, Jutsu, Comment, Profile
import re

UserModel = get_user_model()


class ShinobiForm(forms.ModelForm):
    class Meta:
        model = Shinobi
        fields = ['shinobi_picture', 'name', 'age', 'village', 'rank', 'chakra_nature', 'clan', 'bio']


class ClanForm(forms.ModelForm):
    class Meta:
        model = Clan
        fields = ['symbol', 'name', 'village', 'description', 'founder']


class JutsuForm(forms.ModelForm):
    class Meta:
        model = Jutsu
        fields = ['name', 'chakra_type', 'jutsu_type', 'description']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirm', widget=forms.PasswordInput)
    email = forms.EmailField(max_length=50, required=True, widget=forms.EmailInput(attrs={'required': True}))

    class Meta:
        model = UserModel
        fields = ['email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class SearchForm(forms.Form):
    query = forms.CharField(label="Search", max_length=100, required=False)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'bio', 'avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'accept': 'image/*'})  # no 'multiple' here!
        }
    
    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if len(nickname) > 50:
            raise forms.ValidationError("Nickname cannot exceed 50 characters.")
        if not re.search(r'[A-Z]', nickname):
            raise forms.ValidationError("Nickname must contain at least one uppercase letter.")
        if not re.match(r'^[A-Za-z0-9]+$', nickname):
            raise forms.ValidationError("Nickname can only contain letters and numbers, no special characters or spaces.")
        return nickname

    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        if bio:
            if len(bio) > 500:
                raise forms.ValidationError("Bio cannot exceed 500 characters.")
        
        if not re.match(r'^[\w\s.,!?-]*$', bio):
            raise forms.ValidationError("Bio can only contains letters, numbers, spaces, basic punctuation.")
        return bio