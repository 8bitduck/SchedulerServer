from rest_framework.permissions import BasePermission
from Crypto.Cipher import AES
from Crypto import Random
import base64

class OAuthTokenIsValid(BasePermission):
    """
    The request has a valid OAuth token (either a client or resource owner).
    """

    def has_permission(self, request, view):
        token = request.auth

        if not token:
            return False

        return token.is_valid()

class OAuthTokenHasResourceOwner(BasePermission):
    """
    The request has a valid OAuth token that is authenticated as a resource owner.
    """

    def has_permission(self, request, view):
        user = request.user
        token = request.auth

        if not user or not user.is_authenticated():
            return False

        return token.is_valid()

class TokenHasScope(BasePermission):
    """
    The request is authenticated as a user and the token used has the right scope
    """

    def has_permission(self, request, view):
        token = request.auth

        if not token:
            return False

        if hasattr(token, 'scope'):  # OAuth 2
            required_scopes = self.get_scopes(request, view)
            log.debug("Required scopes to access resource: {0}".format(required_scopes))

            return token.is_valid(required_scopes)

        assert False, ('TokenHasScope requires either the'
                       '`oauth2_provider.rest_framework.OAuth2Authentication` authentication '
                       'class to be used.')

    def get_scopes(self, request, view):
        try:
            return getattr(view, 'required_scopes')
        except AttributeError:
            raise ImproperlyConfigured(
                'TokenHasScope requires the view to define the required_scopes attribute')

class AESCipher:
    def __init__(self, key):
        self.bs = 32
        if len(key) >= 32:
            self.key = key[:32]
        else:
            self.key = self._pad(key)

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]
