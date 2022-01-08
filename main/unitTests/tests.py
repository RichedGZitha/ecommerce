from django.urls import reverse
from .dataSetup import SetupTest


'''

            from rest_framework.authtoken.models import Token
            from rest_framework.test import APIClient

            # Include an appropriate `Authorization:` header on all requests.
            token = Token.objects.get(user__username=self.clark_user.username)
            client = APIClient()
            client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

            response = client.patch(self.url_people, serializer.data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            client.logout()


'''



# Create your tests here.
class MainAppTest(SetupTest):

    def test_fetch_profile_without_loging_in(self):

        get_profile_url = reverse('get-user-profile', kwargs={'pk': self.normal_user.userprofile.pk})
        response = self.client.get(get_profile_url)

        # 401 unathorized request, without logging.
        self.assertEqual(response.status_code,401)

    def test_fetch_profile_after_loging_in(self):
        get_profile_url = reverse('get-user-profile', kwargs={'pk': self.normal_user.userprofile.pk})
        
        # login
        resp = self.client.post('/auth/v1/jwt/create/', data={'email':self.normal_user.email, 'password': 'pass'})

        print(resp.content)
        #response = self.client.get(get_profile_url, data={'Authorization bearer': resp.access})

        # 401 unathorized request, without logging.
        #self.assertEqual(response.status_code, 200)