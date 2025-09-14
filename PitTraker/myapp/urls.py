# PitTraker/myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.home, name="home"),
    path("tools/", views.loaned_tools, name="loaned_tools"),
    path("add-loan/", views.add_tool_loan, name="add_tool_loan"),
    path("edit-loan/<int:tool_id>/", views.edit_tool_loan, name="edit_tool_loan"),
    path("return-tool/<int:tool_id>/", views.return_tool, name="return_tool"),
    path("users/", views.manage_users, name="manage_users"),
    path("users/create/", views.create_user, name="create_user"),
    path("users/edit/<int:user_id>/", views.edit_user, name="edit_user"),
    path("users/delete/<int:user_id>/", views.delete_user, name="delete_user"),
]
