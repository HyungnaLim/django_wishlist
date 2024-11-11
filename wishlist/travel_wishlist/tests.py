from django.test import TestCase
from django.urls import reverse
from .models import Place


class TestHomePage(TestCase):
    def test_home_page_shows_empty_list_message_for_empty_database(self):
        home_page_url = reverse('place_list')
        response = self.client.get(home_page_url)   # make a request and save the response using "client"
        # django will automatically make an empty for each test database, and it will destroy it after the test
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'You have no places in your wishlist')


class TestWishList(TestCase):
    fixtures = ['test_places']  # test fixture data in "fixtures" dir is loaded into the database before running tests
    # Fixtures are assumed to be in the fixtures directory and be in JSON or YAML format

    def test_wishlist_contains_not_visited_places(self):
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'San Francisco')
        self.assertNotContains(response, 'Moab')


class TestVisitedPage(TestCase):
    def test_message_for_empty_visited_list(self):
        visited_page_url = reverse('places_visited')
        response = self.client.get(visited_page_url)
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'You have not visited any places yet')


class TestVisitedList(TestCase):
    fixtures = ['test_places']

    def test_visited_page_contains_correct_data(self):
        visited_page_url = reverse('places_visited')
        response = self.client.get(visited_page_url)
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertNotContains(response, 'Tokyo')
        self.assertNotContains(response, 'New York')
        self.assertContains(response, 'San Francisco')
        self.assertContains(response, 'Moab')


class TestAddNewPlace(TestCase):
    def test_add_new_unvisited_place(self):
        add_place_url = reverse('place_list')
        new_place_data = {'name':'Tokyo', 'visited':False}
        response = self.client.post(add_place_url, new_place_data, follow=True)
        # if another request is made as a result of the first request, it will follow the redirect

        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        response_places = response.context['places']
        self.assertEqual(1, len(response_places))  # check only one place is added

        tokyo = response_places[0]
        tokyo_from_database = Place.objects.get(name='Tokyo', visited=False)
        self.assertEqual(tokyo_from_database, tokyo)


class TestVisitPlace(TestCase):
    fixtures = ['test_places']

    def test_visit_place(self):
        visit_place_url = reverse('place_was_visited', args=(2, ))    # argument is tuple, so keep the comma
        response = self.client.post(visit_place_url, follow=True)

        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertNotContains(response, 'New York')
        self.assertContains(response, 'Tokyo')

        new_york = Place.objects.get(pk=2)
        self.assertTrue(new_york.visited)

    def test_non_existent_place(self):
        visit_place_url = reverse('place_was_visited', args=(235245, ))
        response = self.client.post(visit_place_url, follow=True)
        self.assertEqual(404, response.status_code)
