import datetime
import os
import pathlib

from django.core.files import File
from django.contrib.auth import get_user_model as gum
from rest_framework.test import (
    APITestCase,
    APIClient
)


from projects.models import Project

class CreateModelTest(APITestCase):
    def setUp(self) -> None:
        # set up user
        UserModel = gum()
        self.user = UserModel.objects.create(username='alexis')

        # set dates
        time_fmt = '%Y-%m-%d'
        cur_date = datetime.datetime.now()
        self.begin_date = cur_date.strftime(time_fmt)
        self.end_date = (
                cur_date + datetime.timedelta(hours=24)
            ).strftime('%Y-%m-%d')

        # set up file
        f = open('test_file.txt', 'a+')
        self.test_file = File(f)
    
    def test_create_project(self):
        new_proj = Project(
            name = 'TestProj',
            begin_date = self.begin_date,
            end_date = self.end_date,
            created_by = self.user,
            file = self.test_file)
        new_proj.save()


        self.assertEqual(new_proj.begin_date, self.begin_date)
    
    def tearDown(self) -> None:
        os.remove('./test_file.txt')
