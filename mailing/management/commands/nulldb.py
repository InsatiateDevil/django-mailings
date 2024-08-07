import json
import os
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from blog.models import Blog
from config.settings import BASE_DIR
from mailing.models import Mailing, Message, Client
from users.models import User

file_path = os.path.join(BASE_DIR, 'db.json')


class Command(BaseCommand):

    @staticmethod
    def json_read(path_to_file):
        with open(path_to_file, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)

    # Здесь мы получаем данные из фикстурв с продуктами

    def handle(self, *args, **options):

        Mailing.objects.all().delete()
        Message.objects.all().delete()
        Client.objects.all().delete()
        Blog.objects.all().delete()
        User.objects.all().delete()

        # Создайте списки для хранения объектов
        user_for_create = []
        message_for_create = []
        client_for_create = []
        mailing_for_create = []
        blog_for_create = []
        permissions_for_create = []
        group_for_create = []
        dict_list = Command.json_read(file_path)

        # Обходим все значения категорий из фиктсуры для получения информации
        # об одном объекте
        for user in dict_list:
            if user['model'] == 'users.user':
                user_for_create.append(
                    User(pk=user['pk'],
                         email=user['fields']['email'],
                         password=user['fields']['password'],
                         first_name=user['fields']['first_name'],
                         last_name=user['fields']['last_name'],
                         is_active=user['fields']['is_active'],
                         is_staff=user['fields']['is_staff'],
                         is_superuser=user['fields']['is_superuser'],
                         avatar=user['fields']['avatar'],
                         token=user['fields']['token'],
                         groups=user['fields']['groups'],
                         user_permissions=user['fields']['user_permissions']
                         )
                )

        # Создаем объекты в базе с помощью метода bulk_create()
        User.objects.bulk_create(user_for_create)

        for message in dict_list:
            if message['model'] == 'mailing.message':
                message_for_create.append(
                    Message(pk=message['pk'],
                            subject=message['fields']['subject'],
                            message=message['fields']['message'],
                            owner=message['fields']['owner']
                            )
                )

        Message.objects.bulk_create(message_for_create)

        for client in dict_list:
            if client['model'] =='mailing.client':
                client_for_create.append(
                    Client(pk=client['pk'],
                           name=client['fields']['name'],
                           email=client['fields']['email'],
                           comment=client['fields']['comment'],
                           owner=client['fields']['owner']
                           )
                )

        Client.objects.bulk_create(client_for_create)

        for mailing in dict_list:
            if mailing['model'] == 'mailing.mailing':
                mailing_for_create.append(
                    Mailing(pk=mailing['pk'],
                            name=mailing['fields']['name'],
                            first_send_datetime=mailing['fields']['first_send_datetime'],
                            next_send_datetime=mailing['fields']['next_send_datetime'],
                            last_send_datetime=mailing['fields']['last_send_datetime'],
                            period=mailing['fields']['period'],
                            status=mailing['fields']['status'],
                            message=mailing['fields']['message'],
                            owner=mailing['fields']['owner'],
                            clients=mailing['fields']['clients'],
                            )
                )

        Mailing.objects.bulk_create(mailing_for_create)

        for blog in dict_list:
            if blog['model'] == 'blog.blog':
                blog_for_create.append(
                    Blog(pk=blog['pk'],
                         title=blog['fields']['title'],
                         text=blog['fields']['text'],
                         image=blog['fields']['image'],
                         view_count=blog['fields']['view_count'],
                         created_at=blog['fields']['created_at']
                         )
                )

        Blog.objects.bulk_create(blog_for_create)

        for permission in dict_list:
            if permission['model'] == 'auth.permission':
                permissions_for_create.append(
                    Permission(pk=permission['pk'],
                               name=permission['fields']['name'],
                               content_type=ContentType.objects.get(
                                   pk=permission['fields']['content_type']),
                               codename=permission['fields']['codename'])
                )

        Permission.objects.bulk_create(permissions_for_create)

        for group in dict_list:
            if group['model'] == 'auth.group':
                group_for_create.append(
                    Group(pk=group['pk'],
                          name=group['fields']['name'],
                          permissions=group['fields']['permissions'])
                )

        Group.objects.bulk_create(group_for_create)
