from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from tools.otp_redis import set_otp_code_redis, validate_otp_code_redis
from tools.random_code import generator_code
from tools.sender import send_otp_code
from .services import services_create_user, get_user_by_id, get_user_by_phone_number
from .forms import *


class RegisterView(View):
    form_class = UserRegisterForm
    templates_class = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.templates_class, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            random_code = generator_code()
            send_otp_code(cd['phone_number'], random_code)
            set_otp_code_redis(phone_number=cd['phone_number'], code=random_code)
            request.session['user_registered_info'] = {'phone_number': cd['phone_number'], 'password': cd['password_1']}
            messages.success(request, 'we sent you a code', 'success')

            return redirect('accounts:verify_code')

        return render(request, self.templates_class, {'form': form})


class VerifyCodeRegisterView(View):
    form_class = VerifyCodeForm
    templates_class = 'accounts/verify.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.templates_class, {'form': form})

    def post(self, request):
        user_sessions = request.session['user_registered_info']
        form = self.form_class(request.POST)
        if form.is_valid():
            phone_number = user_sessions['phone_number']
            code = form.cleaned_data['code']
            if not validate_otp_code_redis(phone_number, code):
                messages.danger(request, 'OK Welcome ', 'danger')
                return redirect('accounts:verify_code')
            services_create_user(phone_number=user_sessions['phone_number'], password=user_sessions['password'])
            messages.success(request, 'OK Welcome ', 'success')
            return redirect('pages:home')
        return render(request, self.templates_class, {'form': form})


class LoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Welcome', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('pages:home')
            messages.error(request, 'Invalid credentials', 'danger')
        return render(request, self.template_name, {'form': form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "OK Good ", 'success')
        return redirect('pages:home')


class ProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'
    form_class = ProfileForm
    form_date_class = DateBirthForm

    def get(self, request):
        form = self.form_class()
        form_date = self.form_date_class()
        return render(request, self.template_name, {'form': form, 'form_date': form_date})

    def post(self, request):
        form = self.form_class(request.POST)
        form_date = self.form_date_class(request.POST)
        if form.is_valid() and form_date.is_valid():
            date = form_date.cleaned_data
            cd = form.cleaned_data
            date_birth = f"{date['year']}/{date['month']}/{date['day']}"
            profile = request.user.profile
            profile.date_of_birth = date_birth
            profile.email = cd['email']
            profile.last_name = cd['last_name']
            profile.first_name = cd['first_name']
            profile.save()
            messages.success(request, 'پروفایل شما بروز رسانی شد', 'info')
            return redirect('accounts:profile')
        messages.error(request, 'پروفایل شما بروز رسانی نشد', 'danger')
        return redirect('accounts:profile')


class ChangePasswordView(LoginRequiredMixin, View):
    form_class = ChangePasswordForm
    template_class = 'accounts/change_password.html'

    def get(self, request):
        return render(request, self.template_class, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = get_user_by_id(request.user.id)
            user.set_password(form.cleaned_data['password_1'])
            user.save()
            messages.success(request, 'رمز شما با موفقیت تغییر یافت', 'success')
            return redirect('pages:home')
        messages.error(request, 'مشکلی پیش آمد لطفا دوباره تلاش کنید', 'danger')
        return redirect('accounts:change_password')


class ChangeProfile(LoginRequiredMixin, View):
    template_name = 'accounts/change_profile.html'
    form_class = ProfileForm

    def get(self, request):
        form = self.form_class(instance=request.user.profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'پروفایل با موفقیت تغییر یافت', 'success')
            return redirect('accounts:profile')
        messages.warning(request, 'مشکلی در تغییر پروفایل رخ داد', 'warning')
        return redirect('accounts:change_profile')


class ChangeDateBirth(LoginRequiredMixin, View):
    template_name = 'accounts/change_date_birth.html'
    form_class = DateBirthForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            day = cd['day']
            month = cd['month']
            year = cd['year']
            date = f'{year}/{month}/{day}'
            request.user.profile.date_of_birth = date
            request.user.profile.save()
            messages.success(request, 'تاریخ تولد با موفقیت تغییر یافت', 'success')
            return redirect('accounts:profile')
        messages.error(request, 'مشکلی در تغییر تاریخ تولد رخ داد', 'danger')
        return redirect('accounts:change_birth')


class ForgetPasswordView(View):
    form_class = NumberPhoneForgetPassword
    template_name = 'accounts/forget_password.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = get_user_by_phone_number(cd['number_phone'])
            if user:
                random_code = generator_code()
                send_otp_code(cd['number_phone'], random_code)
                set_otp_code_redis(phone_number=cd['number_phone'], code=random_code)
                request.session['user_forget_password'] = {'number_phone': cd['number_phone']}
                messages.success(request, 'کدی برای شما ارسال شد', 'success')
                return redirect('accounts:verify_password')
            messages.error(request, 'کاربری پیدا نشد', 'danger')
            return redirect('accounts:forget_password')
        messages.error(request, 'فرم نامعتبر است', 'danger')
        return redirect('accounts:forget_password')


class VerifyCodePasswordView(View):
    form_class = VerifyCodeForm
    template_class = 'accounts/verify_password.html'

    def get(self, request):
        return render(request, self.template_class, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            phone_number = request.session['user_forget_password']['number_phone']
            if not validate_otp_code_redis(phone_number, code):
                messages.error(request, 'کد شما منقضی شده است!')
                return redirect('accounts:forget_password')
        messages.error(request, "مشگلی پیش آمد دوباره تلاش کنید")
        return redirect('accounts:forget_password')


class CreateNewPasswordView(View):
    form_class = ChangePasswordForm
    template_class = 'accounts/create_password.html'

    def get(self, request):
        return render(request, self.template_class, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = request.session['user_forget_password']['number_phone']
            user = get_user_by_phone_number(phone)
            user.set_password(form.cleaned_data['password_1'])
            user.save()
            messages.success(request, 'رمز شما با موفقیت تغییر یافت', 'success')
            return redirect('accounts:login')
        messages.error(request, 'مشکلی پیش آمد دوباره تلاش کنید', 'danger')
        return redirect('accounts:create_password')
