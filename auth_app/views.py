
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

User = get_user_model()


def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"detail": "Username and password required"},
                             status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is None or not user.is_active:
            return Response({"detail": "Invalid credentials"},
                             status=status.HTTP_401_UNAUTHORIZED)

        tokens = get_tokens(user)
        res = Response({
            "success": True,
            "user": {"id": user.id, "username": user.username},
        })

        res.set_cookie(
            key="access_token",
            value=tokens["access"],
            max_age=60 * 30,
            secure=not settings.DEBUG,
            httponly=True,
            samesite="Strict",
        )
        res.set_cookie(
            key="refresh_token",
            value=tokens["refresh"],
            max_age=60 * 60 * 24 * 3,
            secure=not settings.DEBUG,
            httponly=True,
            samesite="Strict",
            path="/api/auth/token/refresh/",
        )
        return res


@method_decorator(csrf_exempt, name='dispatch')
class RefreshView(APIView):
    def post(self, request):
        old_refresh_token = request.COOKIES.get("refresh_token")
        if not old_refresh_token:
            return Response({"detail": "No refresh token"}, status=401)

        try:
            old_refresh = RefreshToken(old_refresh_token)
            user_id = old_refresh["user_id"]
            user = User.objects.get(id=user_id)

            old_refresh.blacklist()
            new_tokens = get_tokens(user)
        except (TokenError, User.DoesNotExist):
            return Response({"detail": "Invalid refresh token"}, status=401)

        res = Response({"success": True})
        res.set_cookie(
            key="access_token", value=new_tokens["access"], max_age=60 * 30,
            secure=not settings.DEBUG, httponly=True, samesite="Strict",
        )
        res.set_cookie(
            key="refresh_token", value=new_tokens["refresh"],
            max_age=60 * 60 * 24 * 3,
            secure=not settings.DEBUG, httponly=True, samesite="Strict",
            path="/api/auth/token/refresh/",
        )
        return res


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                pass

        res = Response({"success": True})
        res.delete_cookie("access_token")
        res.delete_cookie("refresh_token", path="/api/auth/token/refresh/")
        return res