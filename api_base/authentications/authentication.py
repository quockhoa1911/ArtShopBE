from rest_framework_simplejwt.authentication import JWTAuthentication


class AdminAuthentication(JWTAuthentication):
    def authenticate(self, request):
        pass
