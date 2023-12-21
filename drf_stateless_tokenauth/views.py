from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from .backends import get_stateless_auth_token_signer


class ObtainStatelessAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        # validate user credentials
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # create stateless auth token
        signer = get_stateless_auth_token_signer()
        token = signer.sign(user.pk)

        # return response
        return Response({'token': token})
