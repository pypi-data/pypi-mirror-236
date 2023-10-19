import uuid
import random
import unittest
from fastutils import nameutils
from fastutils import pinyinutils
from fastutils import hashutils
from ldaputils import LdapService
from ldaputils_local_settings import server_host
from ldaputils_local_settings import server_port
from ldaputils_local_settings import server_username
from ldaputils_local_settings import server_password
from ldaputils_local_settings import user_base_dn_template
from ldaputils_local_settings import user_dn_template
from ldaputils_local_settings import user_search_template
from ldaputils_local_settings import user_attr_object_classes

class TestLdapService(unittest.TestCase):

    def setUp(self):
        self.server = LdapService(
            host=server_host,
            port=server_port,
            username=server_username,
            password=server_password,
            default_user_base_dn_template=user_base_dn_template,
            default_user_dn_template=user_dn_template,
            default_user_search_template=user_search_template,
            default_user_attr_object_classes=user_attr_object_classes,
        )

    def test01(self):
        uid = str(uuid.uuid4())
        uidNumber = random.randint(10000, 1000000)
        mobile = random.randint(13810001000, 13890009000)
        password = str(uuid.uuid4())
        user_detail = {
            "uid": uid,
            "cn": uid,
            "sn": uid,
            "mobile": mobile,
            "mail": uid + "@example.com",
            "id1": uid,
            "ou": uid,
            "l": uid,
            "userPassword": "{SHA}" + hashutils.get_sha1_base64(password),
            "employeeType": uid,
        }
        assert self.server.add_user_entry(uid, user_detail)
        assert self.server.authenticate(uid, password)
        user = self.server.get_user(uid)
        assert user["uid"] == user_detail["uid"]
        assert user["cn"] == user_detail["cn"]

        uidNumber = random.randint(10000, 1000000)
        mobile = random.randint(13810001000, 13890009000)
        user_detail = {
            "uid": uid,
            "cn": uid,
            "sn": uid,
            "uidNumber": uidNumber,
            "gidNumber": uidNumber,
            "homeDirectory": "/home/" + uid, 
            "mobile": mobile,
            "mail": uid + "@example.com",
            "id1": uid,
            "ou": uid,
            "l": uid,
            "userPassword": "{SHA}" + hashutils.get_sha1_base64(password),
            "employeeType": uid,
        }
        assert self.server.update_user_entry(uid, user_detail)

        new_password = str(uuid.uuid4())
        assert self.server.modify_user_password(uid, new_password)
        assert self.server.authenticate(uid, password) == False
        assert self.server.authenticate(uid, new_password)

        password = new_password
        new_password = str(uuid.uuid4())
        new_password_hashed = "{SHA}" + hashutils.get_sha1_base64(new_password)
        assert self.server.modify_user_password_by_encoded_password(uid, new_password_hashed)
        assert self.server.authenticate(uid, password) == False
        assert self.server.authenticate(uid, new_password)

        users = self.server.get_users(paged_size=2)
        assert len(users)

        assert self.server.delete_user_entry(uid)


    def test02(self):
        name = nameutils.get_random_name()
        username = pinyinutils.to_pinyin(name).lower()
        user_detail = {
            "uid": username,
            "cn": name,
            "ou": "公司",
            "l": "中国",
        }
        assert self.server.add_user_entry(username, user_detail)
        assert self.server.delete_user_entry(username)

    def test03(self):
        name = nameutils.get_random_name()
        username = pinyinutils.to_pinyin(name).lower()
        assert self.server.add_user_entry(username)
        assert self.server.delete_user_entry(username)
        
