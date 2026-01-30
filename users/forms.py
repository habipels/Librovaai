from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import get_user_model
#from captcha.fields import ReCaptchaField
#from captcha.widgets import ReCaptchaV2Checkbox


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='Geçerli bir email adresi girin.', required=True)
    user_role = forms.ChoiceField(
        choices=[('reader', 'Okuyucu'), ('author', 'Yazar')],
        initial='reader',
        widget=forms.RadioSelect,
        label='Hesap Türü',
        help_text='Yazar olarak kaydolursanız, admin onayı sonrası kitap yayınlayabilirsiniz.'
    )
    author_title = forms.ChoiceField(
        choices=[
            ('', '--- Seçiniz ---'),
            ('student', 'Öğrenci'),
            ('academic', 'Akademisyen'),
            ('researcher', 'Araştırmacı'),
            ('writer', 'Yazar'),
            ('professor', 'Profesör'),
            ('doctor', 'Doktor'),
            ('other', 'Diğer'),
        ],
        required=False,
        label='Ünvan (Yazar için)',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'user_role', 'author_title', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['username'].help_text = 'Kullanıcı adınızı belirleyin.'
        self.fields['password1'].help_text = 'En az 8 karakter, harf ve rakam içermeli.'

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.user_role = self.cleaned_data['user_role']
        
        # Eğer yazar seçildiyse ünvanı kaydet
        if user.user_role == 'author':
            user.author_title = self.cleaned_data.get('author_title', 'writer')
            user.is_author_approved = False  # Varsayılan olarak onaysız
        
        if commit:
            user.save()

        return user

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="Username or Email*")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))

    #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'image', 'description']

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())