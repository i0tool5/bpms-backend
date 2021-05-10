from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    pass


class CustomUser(AbstractUser):
    objects = CustomUserManager()

    class Meta:
        ordering = ['username']

    def user_projects(self):
        return self.projects.count()

    def user_deals(self):
        return self.deals_created.count()

    def user_assigned_deals(self):
        return self.deals.count()

    def user_tasks(self):
        return self.tasks_created.count()

    def user_assigned_tasks(self):
        return self.tasks.count()

    def __str__(self):
        return self.first_name + ' ' + self.last_name
