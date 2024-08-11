from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, \
    DeleteView, TemplateView

from mailing.forms import MailingForm
from mailing.models import Mailing, Client, Message, MailingTry
from mailing.services import get_uniq_clients_count, get_mailings_counts, \
    get_random_blogs
from mailing.tasks import activate_mailings


# Create your views here.

class HomeTemplateView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uniq_clients'] = get_uniq_clients_count()
        context['mailings_count'], context[
            'active_mailings'] = get_mailings_counts()
        context['blog_list'] = get_random_blogs()
        return context


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if self.request.user.is_superuser or self.request.user.has_perm(
                'mailing.can_view_all_mailings'):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = Mailing(owner=self.request.user)
        return kwargs

    def get_success_url(self):
        return reverse('mailing:mailing_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.next_send_datetime = mailing.first_send_datetime
        mailing.owner = self.request.user
        mailing.save()
        activate_time = mailing.next_send_datetime - timedelta(minutes=5)
        activate_mailings.apply_async((mailing.id,), eta=activate_time)
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm

    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.next_send_datetime = mailing.first_send_datetime
        mailing.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailing:mailing_detail', kwargs={'pk': self.object.pk})


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if self.request.user.is_superuser or self.request.user.has_perm(
                'mailing.can_see'):
            return Client.objects.all()
        return Client.objects.filter(owner=user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ['name', 'email', 'comment']

    def get_success_url(self):
        return reverse('mailing:client_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()
        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_object(self, queryset=None):
        obj = super().get_object()
        if self.request.user.is_superuser:
            return obj
        elif obj.owner != self.request.user:
            raise PermissionDenied('Вы не можете просматривать чужих клиентов')
        return obj


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ['name', 'email', 'comment']

    def get_success_url(self):
        return reverse('mailing:client_detail', kwargs={'pk': self.object.pk})


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    permission_required = 'mailing.can_see_messages'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if self.request.user.is_superuser or self.request.user.has_perm(
                'mailing.can_see'):
            return Message.objects.all()
        return Message.objects.filter(owner=user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['subject', 'message']

    def get_success_url(self):
        return reverse('mailing:message_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()
        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message

    def get_object(self, queryset=None):
        obj = super().get_object()
        if self.request.user.is_superuser:
            return obj
        elif obj.owner != self.request.user:
            raise PermissionDenied('Вы не можете просматривать чужие сообщения')
        return obj


def mailing_cancel(request, pk):
    mailing = Mailing.objects.filter(pk=pk).first()
    if request.user == mailing.owner:
        mailing.status = 2
        mailing.save()
        return redirect('mailing:mailing_detail', pk=pk)
    elif request.user.is_superuser or request.user.has_perm(
            'mailing.can_change_mailing_status'):
        mailing.status = 3
        mailing.save()
        return redirect('mailing:mailing_detail', pk=pk)
    else:
        raise PermissionDenied(
            'Шуруй отседова, ПЁС(плюс пасхалка получается)))))))')


def mailing_activate(request, pk):
    mailing = Mailing.objects.filter(pk=pk).first()
    if mailing.status == 3 and request.user == mailing.owner:
        raise PermissionDenied('Обратитесь в поддержку сервиса')
    elif mailing.status == 2 and request.user == mailing.owner:
        mailing.status = 1
        mailing.save()
        return redirect('mailing:mailing_detail', pk=pk)
    elif request.user.is_superuser or request.user.has_perm(
            'mailing.can_change_mailing_status') and mailing.status == 3:
        mailing.status = 1
        mailing.save()
        return redirect('mailing:mailing_detail', pk=pk)
    else:
        raise PermissionDenied('Что-то пошло не так =(')


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ['subject', 'message']

    def get_success_url(self):
        return reverse('mailing:message_detail', kwargs={'pk': self.object.pk})


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')


class MailingTryListView(LoginRequiredMixin, ListView):
    model = MailingTry

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_obj'] = Mailing.objects.filter(
            pk=self.kwargs['pk']).first()
        return context

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if self.request.user.is_superuser:
            return MailingTry.objects.filter(mailing=self.kwargs['pk'])
        return MailingTry.objects.filter(mailing=self.kwargs['pk'])
