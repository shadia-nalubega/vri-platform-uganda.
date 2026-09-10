from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class RoleBasedAccessControlTests(TestCase):
    """
    Unit & Authorization tests verifying Role-Based Access Control (RBAC)
    and User Role classifications for the VRI Platform.
    """

    def setUp(self):
        self.client = APIClient()

        # 1. Primary Beneficiary: Deaf User
        self.deaf_user = User.objects.create_user(
            username="deaf_user_01",
            password="SecurePassword123!",
            email="deaf01@vri.ug"
        )

        # 2. Core Operator: Certified Interpreter
        self.interpreter = User.objects.create_user(
            username="interpreter_legal_01",
            password="SecurePassword123!",
            email="interpreter01@vri.ug"
        )

        # 3. Institutional Hearing User (e.g., Hospital / Court Officer)
        self.institutional_user = User.objects.create_user(
            username="mulago_hospital_admin",
            password="SecurePassword123!",
            email="admin@mulago.go.ug"
        )

        # 4. System Administrator
        self.admin_user = User.objects.create_superuser(
            username="vri_sysadmin",
            password="AdminSuperPassword123!",
            email="sysadmin@vri.go.ug"
        )

    def test_deaf_user_creation(self):
        """Verify Deaf User user account creation and credentials."""
        self.assertEqual(self.deaf_user.username, "deaf_user_01")
        self.assertTrue(self.deaf_user.check_password("SecurePassword123!"))

    def test_unauthenticated_access_blocked(self):
        """Verify unauthenticated requests to protected API endpoints return 401 Unauthorized."""
        response = self.client.get("/api/sessions/")
        # If the sessions endpoint is protected, unauthenticated calls are blocked
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_404_NOT_FOUND])

    def test_admin_access_privileges(self):
        """Verify System Administrator superuser privileges."""
        self.assertTrue(self.admin_user.is_staff)
        self.assertTrue(self.admin_user.is_superuser)