from api_auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken


class UserServices:

    @classmethod
    def login(cls, data):
        user = User.objects.filter(email=data['email'])
        if user.exists():
            user = user.first()
            if not check_password(data['password'], user.password): raise Exception("Password is not correct!")

            token = RefreshToken.for_user(user)
            token["email"] = user.email
            token["name"] = user.name
            token["role"] = user.role.name
            data = {
                "access_token": str(token.access_token),
                "refresh_token": str(token),
                "email": user.email,
                "role": user.role.name,
                "name": user.name,
                "is_completed": user.is_completed
            }
            return data
        else:
            raise Exception("Email is not correct")

    def update_user(self, pk, data):
        User.objects.filter(pk=pk).update(**data, is_completed=True)
