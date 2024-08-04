from datetime import datetime
from random import shuffle

import pytz
from django.core.cache import cache

from config import settings
from config.settings import CACHE_ENABLED
from mailing.models import Client, Mailing
from blog.models import Blog


def get_datetime():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    return current_datetime


def get_uniq_clients_count():
    if CACHE_ENABLED:
        key = 'uniq_clients_count'
        uniq_clients_count = cache.get(key)
        if uniq_clients_count is None:
            clients = Client.objects.all()
            email_list = []
            for client in clients:
                email_list.append(client.email)
            uniq_clients_count = len(set(email_list))
            cache.set(key, uniq_clients_count, timeout=60)
    else:
        clients = Client.objects.all()
        email_list = []
        for client in clients:
            email_list.append(client.email)
        uniq_clients_count = len(set(email_list))
    return uniq_clients_count


def get_mailings_counts():
    if CACHE_ENABLED:
        key_1 = 'mailings_count'
        key_2 = 'active_mailings_count'
        mailings_count = cache.get(key_1)
        active_mailings_count = cache.get(key_2)
        if mailings_count is None:
            mailings_count = Mailing.objects.all().count()
            cache.set(key_1, mailings_count, timeout=60)
        if active_mailings_count is None:
            active_mailings_count = Mailing.objects.filter(status=1).count()
            cache.set(key_2, active_mailings_count, timeout=60)
    else:
        mailings_count = Mailing.objects.all().count()
        active_mailings_count = Mailing.objects.filter(status=1).count()
    return mailings_count, active_mailings_count


def get_random_blogs():
    if CACHE_ENABLED:
        key = 'random_blogs'
        random_blogs = cache.get(key)
        if random_blogs is None:
            random_blogs = list(Blog.objects.all().order_by('?')[:12])
            cache.set(key, random_blogs, timeout=60)
    else:
        random_blogs = list(Blog.objects.all().order_by('?')[:12])
    shuffle(random_blogs)
    return random_blogs[:3]
