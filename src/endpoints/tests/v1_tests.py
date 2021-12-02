from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase


class V1TestCase(APITestCase):

    def _create_new_work(self) -> Response:
        url = reverse('v1:work-list')
        with open('/sample/invoice-cs-CZ.pdf', 'br') as sample:
            response = self.client.post(url, {'pdf_file': sample}, format='multipart')
        return response

    def test_create_work(self):
        """
        Create new work.
        """
        response = self._create_new_work()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['status'], 'created')
        self.assertEqual(response.data['orig_pdf_name'], 'invoice-cs-CZ.pdf')

    def test_list_work(self):
        """
        Get work list.
        """
        self._create_new_work()
        url = reverse('v1:work-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_work(self):
        """
        Get work detail.
        """
        response = self._create_new_work()
        url = reverse('v1:work-detail', args=(response.data['id'], ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'created')
        self.assertEqual(response.data['orig_pdf_name'], 'invoice-cs-CZ.pdf')

    def test_create_work_forbidden(self):
        """
        When sending wrong input creation is refused.
        """
        url = reverse('v1:work-list')
        response = self.client.post(url, {'pdf_file': 'aaaaa'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['pdf_file'], ['The submitted data was not a file. Check the encoding type on the form.'])

    def test_manage_work_forbidden(self):
        """
        Put, patch and delete methods are not allowed.
        """
        url = reverse('v1:work-detail', args=(1, ))
        for method_name in ('patch', 'put', 'delete'):
            method = getattr(self.client, method_name)
            response = method(url, {'status': 'foo'}, format='json')
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
