"""URL patterns for the openedx_unidigital plugin."""

from django.urls import include, path

app_name = "openedx_unidigital"

urlpatterns = [
    path(
        "api/",
        include(
            "openedx_unidigital.api.urls",
            namespace="openedx-unidigital-api",
        ),
    ),
]
