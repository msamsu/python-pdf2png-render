from rest_framework import status

from endpoints.models import Work
from endpoints.tests.v1_tests import V1TestCase
from swarm.tasks import process_pdf


class TasksTestCase(V1TestCase):

    def test_process_work(self):
        """
        Process work.
        """
        response = self._create_new_work()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'created')

        process_pdf(response.data['id'])
        work = Work.objects.get(id=response.data['id'])
        self.assertEqual(work.status, 'done')
        self.assertEqual(work.page_count, 1)
        self.assertEqual(work.outputs.count(), 1)
