import secrets

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, FormView, \
    ListView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserUpdateForm, PasswordRecoveryForm, \
    LoginForm
from users.models import User


class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('blog:index')


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Confirm your email',
            message=f'Please click on the link to confirm your email: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    form_class = UserUpdateForm


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm

    def get_success_url(self):
        return reverse('users:profile',
                       kwargs={'pk': self.request.user.pk})


def email_confirm_view(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.token = None
    user.save()
    return redirect(reverse('users:login'))


class PasswordRecoveryView(FormView):
    model = User
    form_class = PasswordRecoveryForm
    template_name = 'users/password_recovery.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except ObjectDoesNotExist:
                form.add_error('email', 'Пользователь не найден')
                return self.form_invalid(form)
            password = User.objects.make_random_password(length=12)
            user.set_password(password)
            user.save()
            send_mail(
                subject='Your new password',
                message=f'Your new password is: {password}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            return super().form_valid(form)


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.can_view_users'

    def post(self, request, *args, **kwargs):
        user = User.objects.filter(pk=request.POST.get('id')).first()
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return redirect('users:user_list')


def manage_user_status(request, pk):
    user = User.objects.filter(pk=pk).first()
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect('users:user_list')
