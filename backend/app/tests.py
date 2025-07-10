from uuid import uuid4
from datetime import timedelta

from django.test import (
    override_settings,
    TransactionTestCase,
)
from django.core import mail
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from channels.exceptions import DenyConnection

from project.asgi import application
from app.models import (
    Message,
    Document,
)


AUTH_COOKIE_ACCESS = settings.SIMPLE_JWT['AUTH_COOKIE_ACCESS']
AUTH_COOKIE_REFRESH = settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH']
ACCESS_TOKEN_LIFETIME = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
REFRESH_TOKEN_LIFETIME = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

User = get_user_model()


def get_at(user, expired=False):
    at = AccessToken.for_user(user)
    if expired:
        expired_time = timezone.now() - ACCESS_TOKEN_LIFETIME - timedelta(seconds=1)
        at.set_exp(from_time=expired_time)
    return at


def get_rt(user, expired=False):
    rt = RefreshToken.for_user(user)
    if expired:
        expired_time = timezone.now() - REFRESH_TOKEN_LIFETIME - timedelta(seconds=1)
        rt.set_exp(from_time=expired_time)
    return rt


def get_admin_user_data():
    return {
        'username': 'admin',
        'password': 'admin_password',
    }


def get_normal_user_data():
    return {
        'username': 'normal@test.com',
        'password': 'normal_password',
    }


def generate_user_data():
    return {
        'username': f'user_{str(uuid4())[:4]}@test.com',
        'password': str(uuid4()),
    }


@override_settings(
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_TASK_EAGER_PROPAGATES=True
)
class AppEndpointsTestCase(TransactionTestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user_data = get_admin_user_data()
        self.admin_user = User.objects.create_user(
            username=self.admin_user_data['username'],
            password=self.admin_user_data['password'],
            is_staff=True,
        )
        self.normal_user_data = get_normal_user_data()
        self.normal_user = User.objects.create_user(
            username=self.normal_user_data['username'],
            password=self.normal_user_data['password'],
            is_staff=False,
        )
        self.message1 = Message.objects.create(
            user=self.admin_user,
            content='message admin',
        )
        self.message2 = Message.objects.create(
            user=self.normal_user,
            content='message normal',
        )
        self.document1 = Document.objects.create(
            title='document1',
            content='content1',
        )
        self.document2 = Document.objects.create(
            title='document2',
            content='content2',
        )
        self.document3 = Document.objects.create(
            title='document3',
            content='content3',
        )

    def test_api_token_login_success_admin(self):
        url = reverse('app:api_token_login')
        response = self.client.post(url, {
            'username': self.admin_user_data['username'],
            'password': self.admin_user_data['password'],
        })
        self.assertEqual(response.status_code, 200)

    def test_api_token_login_success_normal(self):
        url = reverse('app:api_token_login')
        response = self.client.post(url, {
            'username': self.normal_user_data['username'],
            'password': self.normal_user_data['password'],
        })
        self.assertEqual(response.status_code, 200)

    def test_api_token_login_fail_empty_data(self):
        url = reverse('app:api_token_login')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 400)

    def test_api_token_login_fail_empty_username(self):
        url = reverse('app:api_token_login')
        response = self.client.post(url, {
            'password': self.admin_user_data['password'],
        })
        self.assertEqual(response.status_code, 400)

    def test_api_token_login_fail_wrong_username(self):
        url = reverse('app:api_token_login')
        response = self.client.post(url, {
            'username': 'wrong_username',
            'password': 'password',
        })
        self.assertEqual(response.status_code, 401)

    def test_api_token_login_fail_admin_empty_password(self):
        url = reverse('app:api_token_login')
        response = self.client.post(url, {
            'username': self.admin_user_data['username'],
        })
        self.assertEqual(response.status_code, 400)

    def test_api_token_login_fail_admin_wrong_password(self):
        url = reverse('app:api_token_login')
        response = self.client.post(url, {
            'username': self.admin_user_data['username'],
            'password': 'wrong_password',
        })
        self.assertEqual(response.status_code, 401)

    def test_api_token_login_fail_normal_empty_password(self):
        url = reverse('app:api_token_login')
        response = self.client.post(url, {
            'username': self.normal_user_data['username'],
        })
        self.assertEqual(response.status_code, 400)

    def test_api_token_login_fail_normal_wrong_password(self):
        url = reverse('app:api_token_login')
        response = self.client.post(url, {
            'username': self.normal_user_data['username'],
            'password': 'wrong_password',
        })
        self.assertEqual(response.status_code, 401)

    def test_api_token_refresh_success_admin(self):
        url = reverse('app:api_token_refresh')
        rt = get_rt(self.admin_user)
        self.client.cookies[AUTH_COOKIE_REFRESH] = str(rt)
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)

    def test_api_token_refresh_success_normal(self):
        url = reverse('app:api_token_refresh')
        rt = get_rt(self.normal_user)
        self.client.cookies[AUTH_COOKIE_REFRESH] = str(rt)
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)

    def test_api_token_refresh_fail_empty_token(self):
        url = reverse('app:api_token_refresh')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 400)

    def test_api_token_refresh_fail_invalid_token(self):
        url = reverse('app:api_token_refresh')
        self.client.cookies[AUTH_COOKIE_REFRESH] = 'invalid_token'
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 401)

    def test_api_token_refresh_fail_admin_expired_token(self):
        url = reverse('app:api_token_refresh')
        rt = get_rt(self.admin_user, expired=True)
        self.client.cookies[AUTH_COOKIE_REFRESH] = str(rt)
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 401)

    def test_api_token_refresh_fail_normal_expired_token(self):
        url = reverse('app:api_token_refresh')
        rt = get_rt(self.normal_user, expired=True)
        self.client.cookies[AUTH_COOKIE_REFRESH] = str(rt)
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 401)

    def test_api_token_logout_success_admin(self):
        url = reverse('app:api_token_logout')
        rt = get_rt(self.admin_user)
        self.client.cookies[AUTH_COOKIE_REFRESH] = str(rt)
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)

    def test_api_token_logout_success_normal(self):
        url = reverse('app:api_token_logout')
        rt = get_rt(self.normal_user)
        self.client.cookies[AUTH_COOKIE_REFRESH] = str(rt)
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)

    def test_api_token_logout_fail_empty_token(self):
        url = reverse('app:api_token_logout')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 400)

    def test_api_token_logout_fail_invalid_token(self):
        url = reverse('app:api_token_logout')
        self.client.cookies[AUTH_COOKIE_REFRESH] = 'invalid_token'
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 401)

    def test_api_token_logout_fail_admin_expired_token(self):
        url = reverse('app:api_token_logout')
        rt = get_rt(self.admin_user, expired=True)
        self.client.cookies[AUTH_COOKIE_REFRESH] = str(rt)
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 401)

    def test_api_token_logout_fail_normal_expired_token(self):
        url = reverse('app:api_token_logout')
        rt = get_rt(self.normal_user, expired=True)
        self.client.cookies[AUTH_COOKIE_REFRESH] = str(rt)
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 401)

    def test_api_health_get_success(self):
        url = reverse('app:api_health')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_api_websocket_ticket_post_success_admin(self):
        url = reverse('app:api_websocket_ticket')
        at = get_at(self.admin_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 201)
        ticket = response.data['ticket']
        self.assertEqual(cache.get(f'websocket:ticket:{ticket}'), self.admin_user.id)

    def test_api_websocket_ticket_post_success_normal(self):
        url = reverse('app:api_websocket_ticket')
        at = get_at(self.normal_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 201)
        ticket = response.data['ticket']
        self.assertEqual(cache.get(f'websocket:ticket:{ticket}'), self.normal_user.id)

    def test_api_websocket_ticket_post_fail_empty_token(self):
        url = reverse('app:api_websocket_ticket')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 401)

    def test_api_websocket_ticket_post_fail_invalid_token(self):
        url = reverse('app:api_websocket_ticket')
        self.client.cookies[AUTH_COOKIE_ACCESS] = 'invalid_token'
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 401)

    def test_api_websocket_ticket_post_fail_admin_expired_token(self):
        url = reverse('app:api_websocket_ticket')
        at = get_at(self.admin_user, expired=True)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 401)

    def test_api_websocket_ticket_post_fail_normal_expired_token(self):
        url = reverse('app:api_websocket_ticket')
        at = get_at(self.normal_user, expired=True)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 401)

    async def test_ws_chat_connect_success_admin(self):
        url = reverse('app:api_websocket_ticket')
        at = get_at(self.admin_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = await sync_to_async(self.client.post)(url, {})
        ticket = response.data['ticket']
        communicator = WebsocketCommunicator(application, f'/ws/chat/?ticket={ticket}')
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        self.assertEqual(communicator.scope['user'].id, self.admin_user.id)
        await communicator.disconnect()

    async def test_ws_chat_connect_success_normal(self):
        url = reverse('app:api_websocket_ticket')
        at = get_at(self.normal_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = await sync_to_async(self.client.post)(url, {})
        ticket = response.data['ticket']
        communicator = WebsocketCommunicator(application, f'/ws/chat/?ticket={ticket}')
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        self.assertEqual(communicator.scope['user'].id, self.normal_user.id)
        await communicator.disconnect()

    async def test_ws_chat_connect_fail_empty_ticket(self):
        communicator = WebsocketCommunicator(application, '/ws/chat/')
        with self.assertRaises(DenyConnection):
            await communicator.connect()

    async def test_ws_chat_connect_fail_invalid_ticket(self):
        communicator = WebsocketCommunicator(application, '/ws/chat/?ticket=invalid_ticket')
        with self.assertRaises(DenyConnection):
            await communicator.connect()

    async def test_ws_chat_connect_fail_admin_expired_ticket(self):
        url = reverse('app:api_websocket_ticket')
        at = get_at(self.admin_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = await sync_to_async(self.client.post)(url, {})
        ticket = response.data['ticket']
        communicator = WebsocketCommunicator(application, f'/ws/chat/?ticket={ticket}')
        await communicator.connect()
        await communicator.disconnect()
        communicator = WebsocketCommunicator(application, f'/ws/chat/?ticket={ticket}')
        with self.assertRaises(DenyConnection):
            await communicator.connect()

    async def test_ws_chat_connect_fail_normal_expired_ticket(self):
        url = reverse('app:api_websocket_ticket')
        at = get_at(self.normal_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = await sync_to_async(self.client.post)(url, {})
        ticket = response.data['ticket']
        communicator = WebsocketCommunicator(application, f'/ws/chat/?ticket={ticket}')
        await communicator.connect()
        await communicator.disconnect()
        communicator = WebsocketCommunicator(application, f'/ws/chat/?ticket={ticket}')
        with self.assertRaises(DenyConnection):
            await communicator.connect()

    def test_api_message_detail_get_success_admin(self):
        at = get_at(self.admin_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        url = reverse('app:api_message-detail', args=[self.message1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.message1.id)
        self.assertEqual(response.data['user'], self.message1.user.id)
        self.assertEqual(response.data['username'], self.message1.user.username)
        self.assertEqual(response.data['content'], self.message1.content)
        url = reverse('app:api_message-detail', args=[self.message2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.message2.id)
        self.assertEqual(response.data['user'], self.message2.user.id)
        self.assertEqual(response.data['username'], self.message2.user.username)
        self.assertEqual(response.data['content'], self.message2.content)

    def test_api_message_detail_get_success_normal(self):
        at = get_at(self.normal_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        url = reverse('app:api_message-detail', args=[self.message1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.message1.id)
        self.assertEqual(response.data['user'], self.message1.user.id)
        self.assertEqual(response.data['username'], self.message1.user.username)
        self.assertEqual(response.data['content'], self.message1.content)
        url = reverse('app:api_message-detail', args=[self.message2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.message2.id)
        self.assertEqual(response.data['user'], self.message2.user.id)
        self.assertEqual(response.data['username'], self.message2.user.username)
        self.assertEqual(response.data['content'], self.message2.content)

    def test_api_message_detail_get_fail_empty_token(self):
        url = reverse('app:api_message-detail', args=[self.message1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_message_detail_get_fail_invalid_token(self):
        url = reverse('app:api_message-detail', args=[self.message1.id])
        self.client.cookies[AUTH_COOKIE_ACCESS] = 'invalid_token'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_message_detail_get_fail_admin_expired_token(self):
        url = reverse('app:api_message-detail', args=[self.message1.id])
        at = get_at(self.admin_user, expired=True)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_message_detail_get_fail_normal_expired_token(self):
        url = reverse('app:api_message-detail', args=[self.message1.id])
        at = get_at(self.normal_user, expired=True)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_message_list_get_success_admin(self):
        at = get_at(self.admin_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        url = reverse('app:api_message-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.data['results']
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['id'], self.message2.id)
        self.assertEqual(data[0]['user'], self.message2.user.id)
        self.assertEqual(data[0]['username'], self.message2.user.username)
        self.assertEqual(data[0]['content'], self.message2.content)
        self.assertEqual(data[1]['id'], self.message1.id)
        self.assertEqual(data[1]['user'], self.message1.user.id)
        self.assertEqual(data[1]['username'], self.message1.user.username)
        self.assertEqual(data[1]['content'], self.message1.content)

    def test_api_message_list_get_success_normal(self):
        at = get_at(self.normal_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        url = reverse('app:api_message-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.data['results']
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['id'], self.message2.id)
        self.assertEqual(data[0]['user'], self.message2.user.id)
        self.assertEqual(data[0]['username'], self.message2.user.username)
        self.assertEqual(data[0]['content'], self.message2.content)
        self.assertEqual(data[1]['id'], self.message1.id)
        self.assertEqual(data[1]['user'], self.message1.user.id)
        self.assertEqual(data[1]['username'], self.message1.user.username)
        self.assertEqual(data[1]['content'], self.message1.content)

    def test_api_message_list_get_fail_empty_token(self):
        url = reverse('app:api_message-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_message_list_get_fail_invalid_token(self):
        url = reverse('app:api_message-list')
        self.client.cookies[AUTH_COOKIE_ACCESS] = 'invalid_token'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_message_list_get_fail_admin_expired_token(self):
        url = reverse('app:api_message-list')
        at = get_at(self.admin_user, expired=True)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_message_list_get_fail_normal_expired_token(self):
        url = reverse('app:api_message-list')
        at = get_at(self.normal_user, expired=True)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_message_post_success_admin(self):
        url = reverse('app:api_message-list')
        at = get_at(self.admin_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.post(url, {
            'content': "new message admin",
        })
        self.assertEqual(response.status_code, 201)
        message = Message.objects.last()
        self.assertEqual(message.content, "new message admin")
        self.assertEqual(message.user, self.admin_user)

    def test_api_message_post_success_normal(self):
        url = reverse('app:api_message-list')
        at = get_at(self.normal_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.post(url, {
            'content': "new message normal",
        })
        self.assertEqual(response.status_code, 201)
        message = Message.objects.last()
        self.assertEqual(message.content, "new message normal")
        self.assertEqual(message.user, self.normal_user)

    def test_api_message_post_fail_empty_token(self):
        url = reverse('app:api_message-list')
        response = self.client.post(url, {
            'content': "new message admin",
        })
        self.assertEqual(response.status_code, 401)

    def test_api_message_post_fail_invalid_token(self):
        url = reverse('app:api_message-list')
        self.client.cookies[AUTH_COOKIE_ACCESS] = 'invalid_token'
        response = self.client.post(url, {
            'content': "new message admin",
        })
        self.assertEqual(response.status_code, 401)

    def test_api_message_post_fail_admin_expired_token(self):
        url = reverse('app:api_message-list')
        at = get_at(self.admin_user, expired=True)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.post(url, {
            'content': "new message admin",
        })
        self.assertEqual(response.status_code, 401)

    def test_api_message_post_fail_normal_expired_token(self):
        url = reverse('app:api_message-list')
        at = get_at(self.normal_user, expired=True)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.post(url, {
            'content': "new message normal",
        })
        self.assertEqual(response.status_code, 401)

    def test_api_message_post_fail_admin_empty_content(self):
        url = reverse('app:api_message-list')
        at = get_at(self.admin_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 400)

    def test_api_message_post_fail_normal_empty_content(self):
        url = reverse('app:api_message-list')
        at = get_at(self.normal_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 400)

    async def test_ws_chat_message_success_admin(self):
        url = reverse('app:api_websocket_ticket')
        at = get_at(self.admin_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = await sync_to_async(self.client.post)(url, {})
        ticket = response.data['ticket']
        communicator_admin = WebsocketCommunicator(application, f'/ws/chat/?ticket={ticket}')
        await communicator_admin.connect()
        at = get_at(self.normal_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = await sync_to_async(self.client.post)(url, {})
        ticket = response.data['ticket']
        communicator_normal = WebsocketCommunicator(application, f'/ws/chat/?ticket={ticket}')
        await communicator_normal.connect()
        url = reverse('app:api_message-list')
        at = get_at(self.admin_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = await sync_to_async(self.client.post)(url, {
            'content': "test message admin",
        })
        response = await communicator_admin.receive_json_from()
        self.assertEqual(response['type'], 'chat_message')
        self.assertEqual(response['message']['user'], self.admin_user.id)
        self.assertEqual(response['message']['username'], self.admin_user.username)
        self.assertEqual(response['message']['content'], "test message admin")
        response = await communicator_normal.receive_json_from()
        self.assertEqual(response['type'], 'chat_message')
        self.assertEqual(response['message']['user'], self.admin_user.id)
        self.assertEqual(response['message']['username'], self.admin_user.username)
        self.assertEqual(response['message']['content'], "test message admin")
        await communicator_admin.disconnect()
        await communicator_normal.disconnect()

    async def test_ws_chat_message_success_normal(self):
        url = reverse('app:api_websocket_ticket')
        at = get_at(self.admin_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = await sync_to_async(self.client.post)(url, {})
        ticket = response.data['ticket']
        communicator_admin = WebsocketCommunicator(application, f'/ws/chat/?ticket={ticket}')
        await communicator_admin.connect()
        at = get_at(self.normal_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = await sync_to_async(self.client.post)(url, {})
        ticket = response.data['ticket']
        communicator_normal = WebsocketCommunicator(application, f'/ws/chat/?ticket={ticket}')
        await communicator_normal.connect()
        url = reverse('app:api_message-list')
        at = get_at(self.normal_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = await sync_to_async(self.client.post)(url, {
            'content': "test message normal",
        })
        response = await communicator_admin.receive_json_from()
        self.assertEqual(response['type'], 'chat_message')
        self.assertEqual(response['message']['user'], self.normal_user.id)
        self.assertEqual(response['message']['username'], self.normal_user.username)
        self.assertEqual(response['message']['content'], "test message normal")
        response = await communicator_normal.receive_json_from()
        self.assertEqual(response['type'], 'chat_message')
        self.assertEqual(response['message']['user'], self.normal_user.id)
        self.assertEqual(response['message']['username'], self.normal_user.username)
        self.assertEqual(response['message']['content'], "test message normal")
        await communicator_admin.disconnect()
        await communicator_normal.disconnect()

    def test_api_user_register_post_success(self):
        url = reverse('app:api_user_register')
        data = generate_user_data()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username=data['username']).exists())
        user = User.objects.get(username=data['username'])
        self.assertFalse(user.is_staff)

    def test_api_user_register_post_fail_existing_username(self):
        url = reverse('app:api_user_register')
        data = generate_user_data()
        data['username'] = self.normal_user_data['username']
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_api_user_register_post_fail_empty_username(self):
        url = reverse('app:api_user_register')
        data = generate_user_data()
        del data['username']
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_api_user_register_post_fail_empty_password(self):
        url = reverse('app:api_user_register')
        data = generate_user_data()
        del data['password']
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_api_user_register_post_fail_short_password(self):
        url = reverse('app:api_user_register')
        data = generate_user_data()
        data['password'] = 'short'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_api_user_register_post_fail_common_password(self):
        url = reverse('app:api_user_register')
        data = generate_user_data()
        data['password'] = '12345678'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_api_user_register_post_fail_similar_password(self):
        url = reverse('app:api_user_register')
        data = generate_user_data()
        data['password'] = data['username'].split('@')[0]
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_api_user_profile_get_success_admin(self):
        url = reverse('app:api_user_profile')
        at = get_at(self.admin_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], self.admin_user_data['username'])
        self.assertTrue(response.data['is_staff'])

    def test_api_user_profile_get_success_normal(self):
        url = reverse('app:api_user_profile')
        at = get_at(self.normal_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], self.normal_user_data['username'])
        self.assertFalse(response.data['is_staff'])

    def test_api_user_profile_get_fail_empty_token(self):
        url = reverse('app:api_user_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_user_profile_get_fail_invalid_token(self):
        url = reverse('app:api_user_profile')
        self.client.cookies[AUTH_COOKIE_ACCESS] = 'invalid_token'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_user_profile_get_fail_admin_expired_token(self):
        url = reverse('app:api_user_profile')
        at = get_at(self.admin_user, expired=True)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_user_profile_get_fail_normal_expired_token(self):
        url = reverse('app:api_user_profile')
        at = get_at(self.normal_user, expired=True)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_user_profile_patch_success_admin_username(self):
        url = reverse('app:api_user_profile')
        at = get_at(self.admin_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        new_username = generate_user_data()['username']
        response = self.client.patch(url, {
            'username': new_username
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(id=self.admin_user.id).username, new_username)

    def test_api_user_profile_patch_success_admin_password(self):
        url = reverse('app:api_user_profile')
        at = get_at(self.admin_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        new_password = generate_user_data()['password']
        response = self.client.patch(url, {
            'password': new_password
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.get(id=self.admin_user.id).check_password(new_password))

    def test_api_user_profile_patch_success_normal_username(self):
        url = reverse('app:api_user_profile')
        at = get_at(self.normal_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        new_username = generate_user_data()['username']
        response = self.client.patch(url, {
            'username': new_username
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(id=self.normal_user.id).username, new_username)

    def test_api_user_profile_patch_success_normal_password(self):
        url = reverse('app:api_user_profile')
        at = get_at(self.normal_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        new_password = generate_user_data()['password']
        response = self.client.patch(url, {
            'password': new_password
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.get(id=self.normal_user.id).check_password(new_password))

    def test_api_user_profile_patch_fail_admin_empty_data(self):
        url = reverse('app:api_user_profile')
        at = get_at(self.admin_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.patch(url, {})
        self.assertEqual(response.status_code, 400)

    def test_api_user_profile_patch_fail_normal_empty_data(self):
        url = reverse('app:api_user_profile')
        at = get_at(self.normal_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.patch(url, {})
        self.assertEqual(response.status_code, 400)

    def test_api_user_profile_patch_fail_admin_short_password(self):
        url = reverse('app:api_user_profile')
        at = get_at(self.admin_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.patch(url, {
            'password': 'short'
        })
        self.assertEqual(response.status_code, 400)

    def test_api_user_profile_patch_fail_admin_common_password(self):
        url = reverse('app:api_user_profile')
        at = get_at(self.admin_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.patch(url, {
            'password': '12345678'
        })
        self.assertEqual(response.status_code, 400)

    def test_api_user_profile_patch_fail_admin_similar_password(self):
        url = reverse('app:api_user_profile')
        at = get_at(self.admin_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.patch(url, {
            'password': self.admin_user_data['username'].split('@')[0]
        })
        self.assertEqual(response.status_code, 400)

    def test_api_user_profile_patch_fail_normal_short_password(self):
        url = reverse('app:api_user_profile')
        at = get_at(self.normal_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.patch(url, {
            'password': 'short'
        })
        self.assertEqual(response.status_code, 400)

    def test_api_user_profile_patch_fail_normal_common_password(self):
        url = reverse('app:api_user_profile')
        at = get_at(self.normal_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.patch(url, {
            'password': '12345678'
        })
        self.assertEqual(response.status_code, 400)

    def test_api_user_profile_patch_fail_normal_similar_password(self):
        url = reverse('app:api_user_profile')
        at = get_at(self.normal_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.patch(url, {
            'password': self.normal_user_data['username'].split('@')[0]
        })
        self.assertEqual(response.status_code, 400)

    def test_api_user_profile_patch_fail_empty_token(self):
        url = reverse('app:api_user_profile')
        response = self.client.patch(url, {})
        self.assertEqual(response.status_code, 401)

    def test_api_user_profile_patch_fail_invalid_token(self):
        url = reverse('app:api_user_profile')
        self.client.cookies[AUTH_COOKIE_ACCESS] = 'invalid_token'
        response = self.client.patch(url, {})
        self.assertEqual(response.status_code, 401)

    def test_api_user_profile_patch_fail_admin_expired_token(self):
        url = reverse('app:api_user_profile')
        at = get_at(self.admin_user, expired=True)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.patch(url, {})
        self.assertEqual(response.status_code, 401)

    def test_api_user_profile_patch_fail_normal_expired_token(self):
        url = reverse('app:api_user_profile')
        at = get_at(self.normal_user, expired=True)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.patch(url, {})
        self.assertEqual(response.status_code, 401)

    def test_api_user_password_request_post_success(self):
        url = reverse('app:api_user_password_request')
        normal_email = self.normal_user_data['username']
        cache.delete(f'password_reset:email:{normal_email}')
        response = self.client.post(url, {
            'email': normal_email,
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [normal_email])
        self.assertEqual(mail.outbox[0].from_email, settings.EMAIL_HOST_USER)
        token = cache.get(f'password_reset:email:{normal_email}')
        self.assertIsNotNone(token)
        ttl = cache.ttl(f'password_reset:email:{normal_email}')
        self.assertIsNotNone(ttl)
        self.assertGreater(ttl, 0)
        email = cache.get(f'password_reset:token:{token}')
        self.assertEqual(email, normal_email)
        ttl = cache.ttl(f'password_reset:token:{token}')
        self.assertIsNotNone(ttl)
        self.assertGreater(ttl, 0)

    def test_api_user_password_request_post_success_wrong_email(self):
        url = reverse('app:api_user_password_request')
        wrong_email = 'wrong_email@test.com'
        cache.delete(f'password_reset:email:{wrong_email}')
        response = self.client.post(url, {
            'email': wrong_email,
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(mail.outbox), 0)
        token = cache.get(f'password_reset:email:{wrong_email}')
        self.assertIsNotNone(token)
        ttl = cache.ttl(f'password_reset:email:{wrong_email}')
        self.assertIsNotNone(ttl)
        self.assertGreater(ttl, 0)
        email = cache.get(f'password_reset:token:{token}')
        self.assertIsNone(email)
        ttl = cache.ttl(f'password_reset:token:{token}')
        self.assertTrue(ttl is None or ttl <= 0)

    def test_api_user_password_request_post_fail_recent_email(self):
        url = reverse('app:api_user_password_request')
        normal_email = self.normal_user_data['username']
        cache.delete(f'password_reset:email:{normal_email}')
        _ = self.client.post(url, {
            'email': normal_email,
        })
        response = self.client.post(url, {
            'email': normal_email,
        })
        self.assertEqual(response.status_code, 400)

    def test_api_user_password_request_post_fail_empty_email(self):
        url = reverse('app:api_user_password_request')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(mail.outbox), 0)

    def test_api_user_password_request_post_fail_invalid_email(self):
        url = reverse('app:api_user_password_request')
        cache.delete('password_reset:email:invalid_email')
        response = self.client.post(url, {
            'email': 'invalid_email',
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(mail.outbox), 0)

    def test_api_user_password_reset_patch_success(self):
        token = str(uuid4())
        normal_email = self.normal_user_data['username']
        cache.set(f'password_reset:token:{token}', normal_email, 600)
        url = reverse('app:api_user_password_reset')
        new_password = generate_user_data()['password']
        response = self.client.patch(url, {
            'token': token,
            'password': new_password,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.get(username=normal_email).check_password(new_password))
        self.assertIsNone(cache.get(f'password_reset:email:{normal_email}'))
        self.assertIsNone(cache.get(f'password_reset:token:{token}'))

    def test_api_user_password_reset_patch_fail_invalid_token(self):
        url = reverse('app:api_user_password_reset')
        new_password = generate_user_data()['password']
        response = self.client.patch(url, {
            'token': 'invalid_token',
            'password': new_password,
        })
        self.assertEqual(response.status_code, 400)

    def test_api_user_password_reset_patch_fail_empty_token(self):
        url = reverse('app:api_user_password_reset')
        new_password = generate_user_data()['password']
        response = self.client.patch(url, {
            'password': new_password,
        })
        self.assertEqual(response.status_code, 400)

    def test_api_user_password_reset_patch_fail_empty_password(self):
        token = str(uuid4())
        normal_email = self.normal_user_data['username']
        cache.set(f'password_reset:token:{token}', normal_email, settings.EMAIL_RETRY_DELAY)
        url = reverse('app:api_user_password_reset')
        response = self.client.patch(url, {
            'token': token,
        })
        self.assertEqual(response.status_code, 400)

    def test_api_user_password_reset_patch_fail_short_password(self):
        token = str(uuid4())
        normal_email = self.normal_user_data['username']
        cache.set(f'password_reset:token:{token}', normal_email, settings.EMAIL_RETRY_DELAY)
        url = reverse('app:api_user_password_reset')
        response = self.client.patch(url, {
            'token': token,
            'password': 'short',
        })
        self.assertEqual(response.status_code, 400)

    def test_api_user_password_reset_patch_fail_common_password(self):
        token = str(uuid4())
        normal_email = self.normal_user_data['username']
        cache.set(f'password_reset:token:{token}', normal_email, settings.EMAIL_RETRY_DELAY)
        url = reverse('app:api_user_password_reset')
        response = self.client.patch(url, {
            'token': token,
            'password': '12345678',
        })
        self.assertEqual(response.status_code, 400)

    def test_api_user_password_reset_patch_fail_similar_password(self):
        token = str(uuid4())
        normal_email = self.normal_user_data['username']
        cache.set(f'password_reset:token:{token}', normal_email, settings.EMAIL_RETRY_DELAY)
        url = reverse('app:api_user_password_reset')
        response = self.client.patch(url, {
            'token': token,
            'password': normal_email.split('@')[0],
        })
        self.assertEqual(response.status_code, 400)

    def test_api_user_password_reset_patch_fail_used_token(self):
        token = str(uuid4())
        normal_email = self.normal_user_data['username']
        cache.set(f'password_reset:token:{token}', normal_email, settings.EMAIL_RETRY_DELAY)
        url = reverse('app:api_user_password_reset')
        new_password = generate_user_data()['password']
        response = self.client.patch(url, {
            'token': token,
            'password': new_password,
        })
        response = self.client.patch(url, {
            'token': token,
            'password': new_password,
        })
        self.assertEqual(response.status_code, 400)

    def test_api_user_password_reset_patch_fail_expired_token(self):
        token = str(uuid4())
        normal_email = self.normal_user_data['username']
        cache.set(f'password_reset:token:{token}', normal_email, 0)
        url = reverse('app:api_user_password_reset')
        new_password = generate_user_data()['password']
        response = self.client.patch(url, {
            'token': token,
            'password': new_password,
        })
        self.assertEqual(response.status_code, 400)

    def test_api_document_detail_get_success_admin(self):
        at = get_at(self.admin_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        url = reverse('app:api_document-detail', args=[self.document1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data['id'], self.document1.id)
        self.assertEqual(data['title'], self.document1.title)
        self.assertEqual(data['content'], self.document1.content)
        url = reverse('app:api_document-detail', args=[self.document2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data['id'], self.document2.id)
        self.assertEqual(data['title'], self.document2.title)
        self.assertEqual(data['content'], self.document2.content)
        url = reverse('app:api_document-detail', args=[self.document3.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data['id'], self.document3.id)
        self.assertEqual(data['title'], self.document3.title)
        self.assertEqual(data['content'], self.document3.content)

    def test_api_document_detail_get_success_normal(self):
        at = get_at(self.normal_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        url = reverse('app:api_document-detail', args=[self.document1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data['id'], self.document1.id)
        self.assertEqual(data['title'], self.document1.title)
        self.assertEqual(data['content'], self.document1.content)
        url = reverse('app:api_document-detail', args=[self.document2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data['id'], self.document2.id)
        self.assertEqual(data['title'], self.document2.title)
        self.assertEqual(data['content'], self.document2.content)
        url = reverse('app:api_document-detail', args=[self.document3.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data['id'], self.document3.id)
        self.assertEqual(data['title'], self.document3.title)
        self.assertEqual(data['content'], self.document3.content)

    def test_api_document_detail_get_fail_empty_token(self):
        url = reverse('app:api_document-detail', args=[self.document1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_document_detail_get_fail_invalid_token(self):
        url = reverse('app:api_document-detail', args=[self.document1.id])
        self.client.cookies[AUTH_COOKIE_ACCESS] = 'invalid_token'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_document_detail_get_fail_admin_expired_token(self):
        url = reverse('app:api_document-detail', args=[self.document1.id])
        at = get_at(self.admin_user, expired=True)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_document_detail_get_fail_normal_expired_token(self):
        url = reverse('app:api_document-detail', args=[self.document1.id])
        at = get_at(self.normal_user, expired=True)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_document_list_get_success_admin(self):
        url = reverse('app:api_document-list')
        at = get_at(self.admin_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.data['results']
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['id'], self.document3.id)
        self.assertEqual(data[0]['title'], self.document3.title)
        self.assertEqual(data[0]['content'], self.document3.content)
        self.assertEqual(data[1]['id'], self.document2.id)
        self.assertEqual(data[1]['title'], self.document2.title)
        self.assertEqual(data[1]['content'], self.document2.content)
        self.assertEqual(data[2]['id'], self.document1.id)
        self.assertEqual(data[2]['title'], self.document1.title)
        self.assertEqual(data[2]['content'], self.document1.content)

    def test_api_document_list_get_success_normal(self):
        url = reverse('app:api_document-list')
        at = get_at(self.normal_user)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.data['results']
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['id'], self.document3.id)
        self.assertEqual(data[0]['title'], self.document3.title)
        self.assertEqual(data[0]['content'], self.document3.content)
        self.assertEqual(data[1]['id'], self.document2.id)
        self.assertEqual(data[1]['title'], self.document2.title)
        self.assertEqual(data[1]['content'], self.document2.content)
        self.assertEqual(data[2]['id'], self.document1.id)
        self.assertEqual(data[2]['title'], self.document1.title)
        self.assertEqual(data[2]['content'], self.document1.content)

    def test_api_document_list_get_fail_empty_token(self):
        url = reverse('app:api_document-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_document_list_get_fail_invalid_token(self):
        url = reverse('app:api_document-list')
        self.client.cookies[AUTH_COOKIE_ACCESS] = 'invalid_token'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_document_list_get_fail_admin_expired_token(self):
        url = reverse('app:api_document-list')
        at = get_at(self.admin_user, expired=True)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_document_list_get_fail_normal_expired_token(self):
        url = reverse('app:api_document-list')
        at = get_at(self.normal_user, expired=True)
        self.client.cookies[AUTH_COOKIE_ACCESS] = str(at)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
