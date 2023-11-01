from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User, Profile
from .validator import validate_year
from django.contrib.auth.password_validation import validate_password


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, validators=[validate_password])
    password2 = forms.CharField(label='Password confirm', widget=forms.PasswordInput, validators=[validate_password])

    class Meta:
        model = User
        fields = ('phone_number',)
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="you can change your password  using <a href=\"../password/\">this form</a>")

    class Meta:
        model = User
        fields = ('phone_number', 'password', 'is_active', 'is_admin',)


class UserRegisterForm(forms.Form):
    phone_number = forms.CharField(max_length=11, label='شماره تلفن',
                                   widget=forms.NumberInput(attrs={'class': 'alert alert-dark col-md-3 text-center'}))
    password_1 = forms.CharField(label='رمز عبور', validators=[validate_password],
                                 widget=forms.PasswordInput(attrs={'class': 'alert alert-dark col-md-3 text-center'}))
    password_2 = forms.CharField(label='تائید رمز عبور', validators=[validate_password],
                                 max_length=128,
                                 widget=forms.PasswordInput(attrs={'class': 'alert alert-dark col-md-3 text-center'}))

    def clean_number_phone(self):
        phone_number = self.cleaned_data['phone_number']
        if User.objects.filter(phone_number=self.phone_number).exists():
            raise ValidationError('این شماره تلفن در حال حاضر موجود است')
        return phone_number

    def clean_password(self):
        """
        check password mach
        """
        password_1 = self.cleaned_data['password_1']
        password_2 = self.cleaned_data['password_2']
        if password_1 and password_2 and password_1 != password_2:
            raise ValidationError('رمز ها باید برابر باشند')
        return password_1


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(label='شماره تلفن',
                                   widget=forms.NumberInput(attrs={'class': 'alert alert-dark col-md-3 text-center'}))
    password = forms.CharField(label='رمز عبور',
                               widget=forms.PasswordInput(attrs={'class': 'alert alert-dark col-md-3 text-center'}))


class ChangePasswordForm(forms.Form):
    password_1 = forms.CharField(widget=forms.PasswordInput(), label='رمز عبور',
                                 validators=[validate_password])

    password_2 = forms.CharField(widget=forms.PasswordInput(), label='تائید رمز عبور',
                                 validators=[validate_password])

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password_1')
        p2 = cd.get('password_2')
        if p1 and p2 and p1 != p2:
            raise ValidationError("be most mach")


days_of_mounts = [
    (1, '1',), (2, '2',), (3, '3',), (4, '4',), (5, '5',), (6, '6',), (7, '7',), (8, '8',), (9, '9',), (10, '10',),
    (13, '13',), (14, '14',), (15, '15',), (16, '16',), (11, '11',), (12, '12',), (17, '17',), (18, '18',), (19, '19',),
    (20, '20',), (21, '21',), (22, '22',), (23, '23',), (24, '24',), (25, '25',), (26, '26',), (27, '27',), (28, '28',),
    (29, '29',), (30, '30',), (31, '31',)
]
mounts_of_year = [
    (1, 'فروردین',), (2, 'اردیبهشت',), (3, 'خرداد',), (4, 'تیر',), (5, 'مرداد',), (6, 'شهریور',),
    (7, 'مهر',), (8, 'آبان',), (9, 'آذر',), (10, 'دی',), (11, 'بهمن',), (12, 'اسفند',), ]


class DateBirthForm(forms.Form):
    day = forms.ChoiceField(choices=days_of_mounts)
    mount = forms.ChoiceField(choices=mounts_of_year)
    year = forms.IntegerField(validators=[validate_year])


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'address')


class NumberPhoneForgetPassword(forms.Form):
    number_phone = forms.CharField()

