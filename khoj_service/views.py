import requests
from django.http import HttpResponse
from rest_framework.views import APIView


class DefaultRedirectApiView(APIView):
    def get(self, request):
        print(request)
        # Get the url of the request
        url = request.get_full_path()
        print(url)
        attempt = requests.get(f"https://dd16-73-222-140-214.ngrok-free.app{url}")
        return HttpResponse(attempt)


class RedirectToKhojStaticAssets(APIView):
    def get(self, request):
        print(request)
        # Get the url of the request
        url = request.get_full_path()
        print(url)
        # Strip the /khoj/ from the url
        url = url[5:]
        attempt = requests.get(f"https://dd16-73-222-140-214.ngrok-free.app{url}")
        print(attempt)
        content_type = attempt.headers.get("Content-Type")
        return HttpResponse(attempt, content_type=content_type)


class RedirectToKhojHomePage(APIView):
    def get(self, request):
        attempt = requests.get("https://dd16-73-222-140-214.ngrok-free.app/")
        print(attempt)
        return HttpResponse(attempt)
