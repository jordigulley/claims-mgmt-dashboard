from django.urls import path

from . import views

appname = "dashboard"
urlpatterns = [
    path("", views.index, name="index"),
    path("claim_details", views.get_claim_details, name="claim_details"),
    path("add_note", views.add_note, name="add_note"),
    path("get_claims_table_page", views.get_claims_table_page_view, name="get_claims_table_page")
]