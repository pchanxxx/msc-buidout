#!/bin/python
r"""
mod_auth_tkt style cookie authentication
========================================

This module implements the session cookie format from mod_auth_tkt_. For
compatability with other implementations, pass ``mod_auth_tkt=True`` to the
``createTicket`` and ``validateTicket`` functions. This invokes the MD5_ based
double hashing scheme in the original mod_auth_tkt. If such compatability is
not required, a more secure HMAC_ SHA-256_ cryptographic hash may be used
(which is the default.)

.. _mod_auth_tkt: http://www.openfusion.com.au/labs/mod_auth_tkt/
.. _MD5: http://en.wikipedia.org/wiki/MD5
.. _HMAC: http://en.wikipedia.org/wiki/HMAC
.. _SHA-256: http://en.wikipedia.org/wiki/SHA-256

Example
-------

This is a python doctest, you may run this file to execute the test with the
command `python tktauth.py`. No output indicates success.

The protocol depends on a secret string shared between servers. From time to
time this string should be changed, so store it in a configuration file.

  >>> SECRET = 'abcdefghijklmnopqrstuvwxyz0123456789'

The tickets are only valid for a limited time. Here we will use 12 hours

  >>> TIMEOUT = 12*60*60


Cookie creation
---------------

We have a user with the following id:

  >>> userid = 'jbloggs'

We first set the timestamp that the user logged in, for the purposes of this
test 2008-07-22 11:00:

  >>> timestamp = 1216720800

We will create a mod_auth_tkt compatible ticket. In the simplest case no extra
data is supplied.

  >>> tkt = createTicket(SECRET, userid, timestamp=timestamp, mod_auth_tkt=True)
  >>> tkt
  'c7c7300ac5cf529656444123aca345294885afa0jbloggs!'

The cookie itself should be base64 encoded. We will use the built-in Cookie
module here, your web framework may supply it's own mechanism.

  >>> import Cookie, binascii
  >>> cookie = Cookie.SimpleCookie()
  >>> cookie['auth_tkt'] = binascii.b2a_base64(tkt).strip()
  >>> print cookie
  Set-Cookie: auth_tkt=YzdjNzMwMGFjNWNmNTI5NjU2NDQ0MTIzYWNhMzQ1Mjk0ODg1YWZh...


Cookie validation
-----------------

First the ticket has to be read from the cookie and unencoded:

  >>> tkt = binascii.a2b_base64(cookie['auth_tkt'].value)
  >>> tkt
  'c7c7300ac5cf529656444123aca345294885afa0jbloggs!'

Splitting the data reveals the contents (note the unicode output):

  >>> splitTicket(tkt)
  ('c7c7300ac5cf529656444123aca34529', u'jbloggs', (), u'', 1216720800)

We will validate it an hour after it was created:

  >>> NOW = timestamp + 60*60
  >>> data = validateTicket(SECRET, tkt, timeout=TIMEOUT, now=NOW, mod_auth_tkt=True)
  >>> data is not None
  True

After the timeout the ticket is no longer valid

  >>> LATER = NOW + TIMEOUT
  >>> data = validateTicket(SECRET, tkt, timeout=TIMEOUT, now=LATER, mod_auth_tkt=True)
  >>> data is not None
  False


Tokens and user data
--------------------

The format allows for optional user data and tokens. We will store the user's
full name in the user data field. We are not yet using tokens, but may do so in
the future.

  >>> user_data = 'Joe Bloggs'
  >>> tokens = ['foo', 'bar']
  >>> tkt = createTicket(SECRET, userid, tokens, user_data, timestamp=timestamp, mod_auth_tkt=True)
  >>> tkt
  'eea3630e98177bdbf0e7f803e1632b7e4885afa0jbloggs!foo,bar!Joe Bloggs'
  >>> cookie['auth_tkt'] = binascii.b2a_base64(tkt).strip()
  >>> print cookie
  Set-Cookie: auth_tkt=ZWVhMzYzMGU5ODE3N2JkYmYwZTdmODAzZTE2MzJiN2U0ODg1YWZh...
  >>> data = validateTicket(SECRET, tkt, timeout=TIMEOUT, now=NOW, mod_auth_tkt=True)
  >>> data
  ('eea3630e98177bdbf0e7f803e1632b7e', u'jbloggs', (u'foo', u'bar'), u'Joe Bloggs', 1216720800)


Using the more secure hashing scheme
------------------------------------

The HMAC SHA-256 hash must be packed raw to fit into the first 32 bytes.

  >>> tkt = createTicket(SECRET, userid, timestamp=timestamp)
  >>> tkt
  '\xf3\x08\x98\x99\x83\xb0;\xef\x95\x94\xee...\xbe\xf6X\x114885afa0jbloggs!'
  >>> data = validateTicket(SECRET, tkt, timeout=TIMEOUT, now=NOW)
  >>> data is not None
  True

"""

from socket import inet_aton
from struct import pack
import hashlib
import hmac
import time

def mod_auth_tkt_digest(secret, data1, data2):
    digest0 = hashlib.md5(data1 + secret + data2).hexdigest()
    digest = hashlib.md5(digest0 + secret).hexdigest()
    return digest


def createTicket(secret, userid, tokens=(), user_data=u'', ip='0.0.0.0', timestamp=None, encoding='utf8', mod_auth_tkt=False):
    """
    By default, use a more compatible
    """
    if timestamp is None:
        timestamp = int(time.time())

    userid = userid.encode(encoding)
    token_list = ','.join(tokens).encode(encoding)
    user_data = user_data.encode(encoding)

    # ip address is part of the format, set it to 0.0.0.0 to be ignored.
    # inet_aton packs the ip address into a 4 bytes in network byte order.
    # pack is used to convert timestamp from an unsigned integer to 4 bytes
    # in network byte order.
    data1 = inet_aton(ip) + pack("!I", timestamp)
    data2 = '\0'.join((userid, token_list, user_data))
    if mod_auth_tkt:
        digest = mod_auth_tkt_digest(secret, data1, data2)
    else:
        # a sha256 digest is the same length as an md5 hexdigest
        digest = hmac.new(secret, data1+data2, hashlib.sha256).digest()

    # digest + timestamp as an eight character hexadecimal + userid + !
    ticket = "%s%08x%s!" % (digest, timestamp, userid)
    if tokens:
        ticket += token_list + '!'
    ticket += user_data

    return ticket


def splitTicket(ticket, encoding='utf8'):
    digest = ticket[:32]
    val = ticket[32:40]
    if not val:
        raise ValueError
    timestamp = int(val, 16) # convert from hexadecimal+

    parts = ticket[40:].decode(encoding).split("!")

    if len(parts) == 2:
        userid, user_data = parts
        tokens = ()
    elif len(parts) == 3:
        userid, token_list, user_data = parts
        tokens = tuple(token_list.split(','))
    else:
        raise ValueError

    return (digest, userid, tokens, user_data, timestamp)


def validateTicket(secret, ticket, ip='0.0.0.0', timeout=0, now=None, encoding='utf8', mod_auth_tkt=False):
    """
    To validate, a new ticket is created from the data extracted from cookie
    and the shared secret. The two digests are compared and timestamp checked.
    Successful validation returns (digest, userid, tokens, user_data, timestamp).
    On failure, return None.
    """
    try:
        (digest, userid, tokens, user_data, timestamp) = data = splitTicket(ticket)
    except ValueError:
        return None
    new_ticket = createTicket(secret, userid, tokens, user_data, ip, timestamp, encoding, mod_auth_tkt)
    if new_ticket[:32] == digest:
        if not timeout:
            return data
        if now is None:
            now = time.time()
        if timestamp + timeout > now:
            return data
    return None


# doctest runner
def _test():
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)

if __name__ == "__main__":
    _test()
