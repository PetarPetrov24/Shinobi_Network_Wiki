from django import forms
from django.contrib.auth import get_user_model
from shinobi_verse.models import Shinobi, Clan, Jutsu, Comment

UserModel = get_user_model()


class ShinobiForm(forms.ModelForm):
    class Meta:
        model = Shinobi
        fields = ['name', 'age', 'village', 'rank', 'chakra_nature', 'clan', 'bio', 'shinobi_picture']


class ClanForm(forms.ModelForm):
    class Meta:
        model = Clan
        fields = ['name', 'village', 'symbol', 'description', 'founder']


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




