from django.db import models


# Create your models here.
class Client(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="имя клиента"
    )
    email = models.EmailField(
        max_length=100,
        verbose_name="email клиента"
    )
    comment = models.TextField(
        verbose_name="комментарий"
    )
    owner = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        verbose_name="пользователь"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"


class Message(models.Model):
    subject = models.CharField(
        max_length=150,
        verbose_name="тема сообщения"
    )
    message = models.TextField(
        verbose_name="сообщение"
    )
    owner = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        verbose_name="пользователь"
    )

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"


class Mailing(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="название рассылки"
    )
    first_send_datetime = models.DateTimeField(
        verbose_name="дата первого отправления"
    )
    next_send_datetime = models.DateTimeField(
        verbose_name="дата следующего отправления"
    )
    last_send_datetime = models.DateTimeField(
        verbose_name="дата последнего отправления"
    )
    period_choices = (
        (1, 'Каждую минуту'),
        (60, 'Каждый час'),
        (1440, 'Ежедневно'),
        (10080, 'Еженедельно'),
        (43200, 'Ежемесячно(каждые 30 дней)'),
    )
    period = models.IntegerField(
        choices=period_choices,
        verbose_name="периодичность рассылки"
    )
    status_choices = (
        (0, 'Создана'),
        (1, 'Запущена'),
        (2, 'Отменена пользователем'),
        (3, 'Отменена персоналом'),
        (4, 'Завершена')
    )
    status = models.IntegerField(
        choices=status_choices,
        verbose_name="статус рассылки"
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name="сообщение"
    )
    clients = models.ManyToManyField(
        Client,
        verbose_name="клиенты"
    )
    owner = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        verbose_name="пользователь"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        permissions = (
            ('mailing.can_change_mailing_status', 'Может изменять статус рассылки'),
            ('mailing.can_view_all_mailings', 'Может просматривать все рассылки'),
        )


class MailingTry(models.Model):
    try_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name="время и дата попытки",
        editable=False
    )
    status = models.BooleanField(
        verbose_name="статус попытки",
        editable=False
    )
    response = models.TextField(
        null=True,
        verbose_name="ответ почтового сервера",
        editable=False
    )
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        verbose_name="рассылка"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name="клиент"
    )

    def __str__(self):
        return (f'Попытка рассылки {self.pk} - {self.mailing} '
                f'- {self.try_datetime} - {self.status} - {self.client}')

    class Meta:
        verbose_name = "попытка отправки"
        verbose_name_plural = "попытки отправки"
