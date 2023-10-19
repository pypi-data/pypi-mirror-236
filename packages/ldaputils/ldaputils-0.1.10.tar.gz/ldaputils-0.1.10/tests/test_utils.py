import unittest
import ldaputils

class TestLdapUtils(unittest.TestCase):

    def test01(self):
        assert ldaputils.get_base_dn_from_domain("example.com") == "dc=example,dc=com"

    def test02(self):
        assert ldaputils.get_dn_from_path("users.accounts.example.com") == "cn=users,cn=accounts,dc=example,dc=com"
        assert ldaputils.get_dn_from_path("users.accounts", "example.com") == "cn=users,cn=accounts,dc=example,dc=com"
    