from django.contrib.auth import get_user_model

User = get_user_model()


class UserService:
    @staticmethod
    def register_user(data: dict) -> User:
        user = User.objects.create_user(
            username=data.get('username') or data['email'].split('@')[0],
            email=data['email'],
            first_name=data.get('first_name', ''),
            password=data['password'],
            role=User.Role.CUSTOMER
        )
        return user
