from django.contrib import admin

from mailing.models import Mailing, Message, Client, MailingTry


# Register your models here.
@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'period', 'status', 'owner')
    list_filter = ('status', 'owner', 'period')
    search_fields = ('name',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject')
    list_filter = ('owner',)
    search_fields = ('subject', 'message')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    search_fields = ('name', 'email', 'comment')


@admin.register(MailingTry)
class MailingTryAdmin(admin.ModelAdmin):
    list_display = ('id', 'try_datetime', 'status', 'mailing', 'client')
    list_filter = ('status', 'mailing', 'client')
    search_fields = ('mailing', 'client', 'response')
