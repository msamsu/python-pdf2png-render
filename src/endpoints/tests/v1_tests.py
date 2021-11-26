import inspect
import json

from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase

from endpoints import views
from endpoints.models import Work

__author__ = 'martin'


def jc(item):
    return json.loads(item.decode('utf8'))


class V1TestCase(TestCase):

    API_VERSION = 'v1'
    WORKS_VIEW = views.WorkViewSet
    DIVIDER = '------------------------------------------------------------------------------------------'

    def _create_test_request(self, method, url, data=None):
        request = getattr(RequestFactory(), method)(url, data or {}, 'application/json')
        # Messages framework bugfix
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        return request

    def _create_work(self):
        view = self.WORKS_VIEW.as_view({'post': 'create'})
        data = {'pdf_file': 'aaaaaaaaaaaaaaa'}
        response = view(self._create_test_request('post', f'/api/{self.API_VERSION}/works/', data))
        return response

    def test_work_creation_forbidden(self, *args, **kwargs):
        print(f'{self.DIVIDER} {inspect.currentframe().f_code.co_name}')
        view = self.WORKS_VIEW.as_view({'post': 'create'})
        data = {'pdf_file': 'aaaaaaaaaaaaaaa'}
        response = view(self._create_test_request('post', f'/api/{self.API_VERSION}/works/', data))
        print(response)
        print(response.status_code)
        print(jc(response.content))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(jc(response.content), ['creation of work not permitted'])

    def test_work_creation(self, *args, **kwargs):
        print(f'{self.DIVIDER} {inspect.currentframe().f_code.co_name}')
        response = self._create_work()
        print(response)
        print(response.status_code)
        print(jc(response.content))
        self.assertEqual(response.status_code, 201)

    def test_work_update_forbidden(self, *args, **kwargs):
        print(f'{self.DIVIDER} {inspect.currentframe().f_code.co_name}')
        self._create_work()
        work = Work.objects.get(pk=1)
        view = self.WORKS_VIEW.as_view({'patch': 'update'})
        data = {'status': 'ready'}
        response = view(self._create_test_request('patch', f'/api/{self.API_VERSION}/works/{work.id}/', data), pk=work.id)
        print(response)
        print(response.status_code)
        print(jc(response.content))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(jc(response.content), {'error': 'not permitted'})

    def test_work_list(self, *args, **kwargs):
        print(f'{self.DIVIDER} {inspect.currentframe().f_code.co_name}')
        view = self.WORKS_VIEW.as_view({'get': 'list'})
        response = view(self._create_test_request('get', f'/api/{self.API_VERSION}/works'))
        print(response)
        print(response.status_code)
        print(jc(response.content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(jc(response.content), [])
