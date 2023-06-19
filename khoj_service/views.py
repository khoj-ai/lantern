import requests
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from khoj_service.models import RoutingTable


class DefaultRedirectApiView(APIView):
    permission_classes = [IsAuthenticated]
    routing_table = RoutingTable.objects.all()

    def get(self, request):
        user = request.user
        request_path = request.get_full_path()
        service_url = self.routing_table.get_service_url_by_user(user)
        if service_url is None:
            return Response(
                {"error": "user does not have a service with Khoj"},
                status=status.HTTP_404_NOT_FOUND,
            )

        khoj_response = requests.get(f"{service_url}{request_path}")
        return HttpResponse(khoj_response)


class RedirectToKhojStaticAssets(APIView):
    permission_classes = [IsAuthenticated]
    routing_table = RoutingTable.objects.all()

    def get(self, request):
        user = request.user
        request_path = request.get_full_path()
        service_url = self.routing_table.get_service_url_by_user(user)
        if service_url is None:
            return Response(
                {"error": "user does not have a service with Khoj"},
                status=status.HTTP_404_NOT_FOUND,
            )
        request_path = request_path[5:]
        khoj_response = requests.get(f"{service_url}{request_path}")
        content_type = khoj_response.headers.get("Content-Type")
        return HttpResponse(khoj_response, content_type=content_type)


class RedirectToKhojHomePage(APIView):
    permission_classes = [IsAuthenticated]
    routing_table = RoutingTable.objects.all()

    def get(self, request):
        user = request.user
        service_url = self.routing_table.get_service_url_by_user(user)
        if service_url is None:
            # TODO: We probably want to redirect to a Sign-Up page here.
            return Response(
                {"error": "user does not have a service with Khoj"},
                status=status.HTTP_404_NOT_FOUND,
            )
        khoj_response = requests.get(service_url)
        return HttpResponse(khoj_response)
