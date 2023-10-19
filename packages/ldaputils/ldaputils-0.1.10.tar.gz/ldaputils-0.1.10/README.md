# ldaputils

Ldap utils library.

## Install

```
pip install ldaputils
```

## Usage

```
# use your own host, port, username and password values.
# username must be a fully qualified dn.
# Use ipython help to see more init parameters.
server = LdapService(
    host="localhost,
    port=389,
    username="cn=admin,dc=example,dc=com",
    password="adminpassword",
)

name = nameutils.get_random_name() # use fastutils.nameutils.get_random_name for test
username = pinyinutils.to_pinyin(name).lower()
user_detail = {
    "cn": name,
    "ou": "AI Tech Group",
    "l": "HangZhou, China",
}
assert self.server.add_user_entry(username, user_detail)
assert self.server.delete_user_entry(username)
```

## How to solve `wrap socket error: [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:1006)` problem.

This is not a problem of `ldaputils` library, nor is a problem of `ldap3` library. It happens because ssl client and the server using different protocols.

### Find out your server ssl information with openssl command

```
openssl s_client -connect x.x.x.x:389 -showcerts -starttls ldap
```

- Type shell command above.
- Replace x.x.x.x:389 with your own ldap server address and port.
- The output may looks like:

    ```
    ...
    ...
    ---
    New, TLSv1.2, Cipher is AES256-GCM-SHA384
    Server public key is 2048 bit
    Secure Renegotiation IS supported
    Compression: NONE
    Expansion: NONE
    No ALPN negotiated
    SSL-Session:
        Protocol  : TLSv1.2
        Cipher    : AES256-GCM-SHA384
        Session-ID: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        Session-ID-ctx: 
        Master-Key: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        PSK identity: None
        PSK identity hint: None
        SRP username: None
        TLS session ticket lifetime hint: 300 (seconds)
        TLS session ticket:
        0000 - 19 1a 2e c9 bc 3a c8 2b-27 ab 9c cf 94 12 f8 79   .......['4......
        0010 - bd 1a 9a c9 52 3e ac 2d-af ab aa cf c6 09 f8 7f   .........R.>...O
        0020 - 63 1a b9 c9 73 34 ea 27-4d ab a8 cf 2f 12 f8 79   c..-s4..M..**...
        0030 - ac 1a 18 c9 40 35 4f 26-ce ab ca cf 95 60 f8 71   ....@.O....\.`.a
        0040 - 19 1a 2e c9 9d 34 ba 28-90 ab 50 cf ce 8c f8 79   .......8.oP7..U.
        0050 - d5 1a 3b c9 cc 36 61 27-ff ab 0f cf 4c 34 f8 70   ..;..f..... L4..
        0060 - c8 1a 1b c9 b3 3e a5 27-e0 ab 21 cf 1a 84 f8 75   .<........!...d.
        0070 - 26 1a 1b c9 6b 34 a2 24-03 ab 57 cf 70 e1 f8 74   fW.ykD.t.vxXt..t
        0080 - 8c 1a 52 c9 46 39 e3 2b-44 ab 66 cf 23 b3 f8 7d   ..rrfxI..D.x.#.;M
        0090 - 74 1a f8 c9 af 37 37 2b-89 ab 62 cf 53 5c f8 7b   t8...G7...bGx\..

        Start Time: 1697691557
        Timeout   : 7200 (sec)
        Verify return code: 10 (certificate has expired)
        Extended master secret: no
    ---
    ...
    ...
    ```

- You can found out what `Protocol` and `Cipher` your server is using.

### Init ldap service with tls server parameters

```
from ldap3 import Tls
from ldaputils import LdapService

tls = Tls(
    version=ssl.PROTOCOL_TLSv1_2,
    ciphers="AES256-GCM-SHA384",
)
service = LdapService(
    host="x.x.x.x",
    port=389,
    username="cn=admin,dc=example,dc=com",
    password="example",
    base_dn="dc=example,dc=com",
    server_params={
        "tls": tls,
    },
)
```

- Add `server_params` and you will get SSL problem solved.




## Releases

### v0.1.0 2020/11/14

- First release.
- Add, update, delete user entry function ready.
- Get user and get users function ready.

### v0.1.4 2020/11/17

- Add util functions.

### v0.1.5 2020/11/21

- Add attributes param for LdapService.get_user_entries.

### v0.1.7 2021/03/24

- Fix add_user_entry changed the user_detail dict problem.

### v0.1.9 2023/09/15

- Doc update.

### v0.1.10 2023/10/19

- Doc update.