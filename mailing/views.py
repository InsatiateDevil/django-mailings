from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, \
    DeleteView, TemplateView

from mailing.models import Mailing, Client, Message
from mailing.services import get_uniq_clients_count, get_mailings_counts, \
    get_random_blogs


# Create your views here.

class HomeTemplateView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uniq_clients'] = get_uniq_clients_count()
        context['active_mailings'], context['mailings_count'] = get_mailings_counts()
        context['blog_list'] = get_random_blogs()
        return context


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    fields = '__all__'
    # form_class = MailingForm

    def get_success_url(self):
        return reverse('mailing:mailing_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    fields = '__all__'
    # form_class = MailingForm

    def get_success_url(self):
        return reverse('mailing:mailing_detail', kwargs={'pk': self.object.pk})


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = '__all__'
    # form_class = ClientForm

    def get_success_url(self):
        return reverse('mailing:client_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()
        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = '__all__'
    # form_class = ClientForm

    def get_success_url(self):
        return reverse('mailing:client_detail', kwargs={'pk': self.object.pk})


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = '__all__'
    # form_class = ClientForm

    def get_success_url(self):
        return reverse('mailing:message_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()
        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = '__all__'
    # form_class = ClientForm

    def get_success_url(self):
        return reverse('mailing:message_detail', kwargs={'pk': self.object.pk})


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')




