import requests
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from khoj_service.models import RoutingTable
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect
from django.http import StreamingHttpResponse
from khoj_service.constants import KHOJ_HOME


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

    def post(self, request):
        user = request.user
        request_path = request.get_full_path()
        service_url = self.routing_table.get_service_url_by_user(user)
        if service_url is None:
            return Response(
                {"error": "user does not have a service with Khoj"},
                status=status.HTTP_404_NOT_FOUND,
            )
        body = request.data
        khoj_response = requests.post(
            f"{service_url}{request_path}", json=body, headers=request.headers
        )
        return HttpResponse(khoj_response)


class StreamingApiView(APIView):
    permission_classes = [IsAuthenticated]
    routing_table = RoutingTable.objects.all()

    def _streaming_response(self, response):
        aggregator = b""
        for chunk in response.iter_content(100):
            # This indicates that the compiled references are coming. We want to batch this response in a single chunk.
            # Bear in mind it's possible that the compiled references indicator is split across two chunks. In this case, rendering will fail.
            if (
                len(aggregator) != 0
                or str(chunk).find("### compiled references:") != -1
            ):
                aggregator += chunk
                continue
            yield chunk
        yield aggregator

    def get(self, request):
        user = request.user
        request_path = request.get_full_path()
        service_url = self.routing_table.get_service_url_by_user(user)
        if service_url is None:
            return Response(
                {"error": "user does not have a service with Khoj"},
                status=status.HTTP_404_NOT_FOUND,
            )
        response = requests.get(f"{service_url}{request_path}", stream=True)
        return StreamingHttpResponse(
            streaming_content=self._streaming_response(response),
            content_type=response.headers["Content-Type"],
        )


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
    routing_table = RoutingTable.objects.all()

    def get(self, request):
        user = request.user
        if isinstance(user, AnonymousUser):
            return redirect(f"{KHOJ_HOME}/login/")

        service_url = self.routing_table.get_service_url_by_user(user)
        if service_url is None:
            # TODO: We probably want to redirect to a Sign-Up page here.
            return Response(
                {"error": "user does not have a service with Khoj"},
                status=status.HTTP_404_NOT_FOUND,
            )
        khoj_response = requests.get(service_url)
        return HttpResponse(khoj_response)
