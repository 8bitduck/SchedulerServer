from rest_framework.permissions import BasePermission

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
