from django.test import TestCase
from django.urls import reverse


class BookSearchTest(TestCase):
    '''BookSearchTest This class performs the test on the backend view.

    This class performs two tests towards the backend view.
    The first method is "the direct url" for external callers.
    The second method is "the reverse url" for Django internal caller.
    '''

    def test_view_url_exists_at_desired_location(self):
        '''test_view_url_exists_at_desired_location This method checks that the url is correctly set.

        This test checks that a GET can be performed against the url and the status code is 200.
        '''
        response = self.client.get(
            '/backend/search_book/egrim')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        '''test_view_url_accessible_by_name This method checks that the reverse url is correctly set.

        This test checks that a GET can be performed against the url name and the status code is 200.
        '''
        response = self.client.get(
            reverse('search_book', kwargs={"username": "egrim"}))
        self.assertEqual(response.status_code, 200)
