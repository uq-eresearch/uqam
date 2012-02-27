from django_auth_ldap.backend import LDAPBackend
from django.contrib.auth.models import User


class StricterLDAPBackend(LDAPBackend):
    """
    Allow users to login with LDAP, but only if they already exist as a django
    user.

    Provides local control over which users can log in, while still leaving
    password and account management up to LDAP.
    """

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        return super(StricterLDAPBackend, self
                ).authenticate(username, password)

