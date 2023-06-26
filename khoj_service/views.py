import requests
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from khoj_service.models import RoutingTable
import time
import logging

logger = logging.getLogger(__name__)


class DefaultRedirectApiView(APIView):
    permission_classes = [IsAuthenticated]
    routing_table = RoutingTable.objects.all()

    def get(self, request):
        start_time = time.time()
        user = request.user
        end_time = time.time()
        latency = end_time - start_time
        logging.info(f"Latency for getting user {user.username}: {latency:.3f}s")

        start_time = time.time()
        request_path = request.get_full_path()
        end_time = time.time()
        latency = end_time - start_time
        logging.info(f"Latency for getting request path: {latency:.3f}s")

        start_time = time.time()
        service_url = self.routing_table.get_service_url_by_user(user)
        end_time = time.time()
        latency = end_time - start_time
        logging.info(f"Latency for getting service url: {latency:.3f}s")

        start_time = time.time()
        if service_url is None:
            return Response(
                {"error": "user does not have a service with Khoj"},
                status=status.HTTP_404_NOT_FOUND,
            )
        end_time = time.time()
        latency = end_time - start_time
        logging.info(f"Latency for checking service url: {latency:.3f}s")

        start_time = time.time()
        khoj_response = requests.get(f"{service_url}{request_path}")
        end_time = time.time()
        latency = end_time - start_time
        logging.info(f"Latency for making request to service: {latency:.3f}s")

        start_time = time.time()
        respond = HttpResponse(khoj_response)
        end_time = time.time()
        latency = end_time - start_time
        logging.info(f"Latency for responding to request: {latency:.3f}s")
        return respond

    def post(self, request):
        start_time = time.time()
        user = request.user
        end_time = time.time()
        latency = end_time - start_time
        logging.info(f"Latency for getting user {user.username}: {latency:.3f}s")

        start_time = time.time()
        request_path = request.get_full_path()
        end_time = time.time()
        latency = end_time - start_time
        logging.info(f"Latency for getting request path: {latency:.3f}s")

        start_time = time.time()
        service_url = self.routing_table.get_service_url_by_user(user)
        end_time = time.time()
        latency = end_time - start_time
        logging.info(f"Latency for getting service url: {latency:.3f}s")

        start_time = time.time()
        if service_url is None:
            return Response(
                {"error": "user does not have a service with Khoj"},
                status=status.HTTP_404_NOT_FOUND,
            )
        end_time = time.time()
        latency = end_time - start_time
        logging.info(f"Latency for checking service url: {latency:.3f}s")

        start_time = time.time()
        body = request.data
        end_time = time.time()
        latency = end_time - start_time
        logging.info(f"Latency for getting request body: {latency:.3f}s")

        start_time = time.time()
        khoj_response = requests.post(
            f"{service_url}{request_path}", json=body, headers=request.headers
        )
        end_time = time.time()
        latency = end_time - start_time
        logging.info(f"Latency for making request to service: {latency:.3f}s")

        start_time = time.time()
        respond = HttpResponse(khoj_response)
        end_time = time.time()
        latency = end_time - start_time
        logging.info(f"Latency for responding to request: {latency:.3f}s")

        return respond


class RedirectToKhojAncilliaryAssets(APIView):
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
