from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.saas.models import (
    Organization,
    OrganizationMember,
    Plan,
    Project,
    Role,
    Task,
)


class SaasBaseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.plan = Plan.objects.create(
            name="Basic", price_id="price_basic", user_limit=5, project_limit=5
        )

        # Organization 1 and User 1
        self.user1 = User.objects.create_user(
            email="user1@example.com",
            password="password123",
            first_name="User",
            last_name="One",
        )
        self.org1 = Organization.objects.create(
            name="Org One", slug="org-one", owner=self.user1, plan=self.plan
        )
        OrganizationMember.objects.create(
            organization=self.org1, user=self.user1, role=Role.ADMIN
        )
        self.project1_org1 = Project.objects.create(
            organization=self.org1, name="Project 1 Org 1"
        )
        self.task1_org1 = Task.objects.create(
            project=self.project1_org1, name="Task 1 Org 1"
        )

        # Organization 2 and User 2
        self.user2 = User.objects.create_user(
            email="user2@example.com",
            password="password123",
            first_name="User",
            last_name="Two",
        )
        self.org2 = Organization.objects.create(
            name="Org Two", slug="org-two", owner=self.user2, plan=self.plan
        )
        OrganizationMember.objects.create(
            organization=self.org2, user=self.user2, role=Role.ADMIN
        )
        self.project1_org2 = Project.objects.create(
            organization=self.org2, name="Project 1 Org 2"
        )
        self.task1_org2 = Task.objects.create(
            project=self.project1_org2, name="Task 1 Org 2"
        )


class ProjectAccessTests(SaasBaseTestCase):
    def test_user_cannot_access_other_organization_projects(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse("project-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 1
        )  # Should only see their own project
        self.assertEqual(response.data[0]["name"], self.project1_org1.name)

        self.client.force_authenticate(user=self.user2)
        response = self.client.get(reverse("project-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.project1_org2.name)

    def test_admin_can_create_project(self):
        self.client.force_authenticate(user=self.user1)
        data = {"name": "New Project Org 1"}
        response = self.client.post(reverse("project-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Project.objects_in_org.get_queryset(self.org1).count(), 2
        )

    def test_member_cannot_create_project(self):
        member_user = User.objects.create_user(
            email="member@example.com", password="password123"
        )
        OrganizationMember.objects.create(
            organization=self.org1, user=member_user, role=Role.MEMBER
        )
        self.client.force_authenticate(user=member_user)
        data = {"name": "New Project by Member"}
        response = self.client.post(reverse("project-list"), data)
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )  # Should be forbidden
        self.assertEqual(
            Project.objects_in_org.get_queryset(self.org1).count(), 1
        )  # No new project created


class TaskAccessTests(SaasBaseTestCase):
    def test_user_cannot_access_other_organization_tasks(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse("task-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.task1_org1.name)

        self.client.force_authenticate(user=self.user2)
        response = self.client.get(reverse("task-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.task1_org2.name)

    def test_admin_can_create_task(self):
        self.client.force_authenticate(user=self.user1)
        data = {"project": self.project1_org1.id, "name": "New Task Org 1"}
        response = self.client.post(reverse("task-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Task.objects_in_org.get_queryset(self.org1).count(), 2
        )

    def test_member_cannot_create_task(self):
        member_user = User.objects.create_user(
            email="member2@example.com", password="password123"
        )
        OrganizationMember.objects.create(
            organization=self.org1, user=member_user, role=Role.MEMBER
        )
        self.client.force_authenticate(user=member_user)
        data = {"project": self.project1_org1.id, "name": "New Task by Member"}
        response = self.client.post(reverse("task-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            Task.objects_in_org.get_queryset(self.org1).count(), 1
        )
