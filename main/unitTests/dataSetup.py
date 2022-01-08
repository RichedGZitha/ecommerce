from rest_framework.test import APITestCase, APIClient
from main.models import CustomUser
from django.contrib.auth.models import Group

class SetupTest(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.normal_user = CustomUser.objects.create(username = 'kiing3', email = 'kiing3@g.com', password='pass', is_active = True)#self.client.post('auth/v1/users/' ,data = {'username' :'kiing3', 'email' : 'kiing3@g.com', 'password' : 'pass', 're_password':'pass'}) 
        self.normal_user.is_active = True
        self.normal_user.save()

        self.manager = CustomUser.objects.create(username = 'kiing4', email = 'kiing4@g.com', password = 'pass', is_active = True)
    
        self.merchant = CustomUser.objects.create(username = 'kiing5', email = 'kiing5@g.com', password = 'pass', is_active = True)

        manager_group = Group.objects.filter(name='Manager') 
        #manager_group.user_set.add(self.manager)

        merchant_group = Group.objects.filter(name='Merchant') 
        #merchant_group.user_set.add(self.merchant)


        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()