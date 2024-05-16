""" URL patterns for the Open edX Unidigital API."""

from django.urls import include, path

app_name = "openedx_unidigital"

urlpatterns = [
    path(
        "v1/",
        include("openedx_unidigital.api.v1.urls", namespace="v1"),
    ),
]
