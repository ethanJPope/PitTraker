# PitTraker/myapp/views.py
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import LoanedTool, CustomUser
from .forms import LoanedToolForm, LoginForm, CustomUserCreationForm, UserEditForm


def is_admin(user):
    return user.is_authenticated and user.is_staff


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect("home")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def home(request):
    return render(request, "home.html")


@login_required
def loaned_tools(request):
    tools = LoanedTool.objects.all()
    total_count = tools.count()
    active_count = tools.filter(returned=False).count()
    returned_count = tools.filter(returned=True).count()

    context = {
        "tools": tools,
        "total_count": total_count,
        "active_count": active_count,
        "returned_count": returned_count,
    }
    return render(request, "loaned_tools.html", context)


@login_required
def add_tool_loan(request):
    if request.method == "POST":
        form = LoanedToolForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tool loan recorded successfully!")
            return redirect("loaned_tools")
    else:
        form = LoanedToolForm()
    return render(request, "tool_loan_form.html", {"form": form, "action": "Add"})


@login_required
def edit_tool_loan(request, tool_id):
    tool = get_object_or_404(LoanedTool, id=tool_id)
    if request.method == "POST":
        form = LoanedToolForm(request.POST, instance=tool)
        if form.is_valid():
            form.save()
            messages.success(request, "Tool loan updated successfully!")
            return redirect("loaned_tools")
    else:
        form = LoanedToolForm(instance=tool)
    return render(
        request, "tool_loan_form.html", {"form": form, "action": "Edit", "tool": tool}
    )


@login_required
def return_tool(request, tool_id):
    tool = get_object_or_404(LoanedTool, id=tool_id)
    if request.method == "POST":
        tool.returned = "returned" in request.POST
        if tool.returned:
            tool.date_returned = timezone.now()
        else:
            tool.date_returned = None
        tool.save()
        status = "returned" if tool.returned else "marked as out"
        messages.success(request, f"Tool {status} successfully!")
    return redirect("loaned_tools")


@user_passes_test(is_admin)
def manage_users(request):
    users = CustomUser.objects.all().order_by("username")
    return render(request, "manage_users.html", {"users": users})


@user_passes_test(is_admin)
def create_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, f"User {user.username} has been created successfully."
            )
            return redirect("manage_users")
    else:
        form = CustomUserCreationForm()

    return render(request, "create_user.html", {"form": form})


@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            updated_user = form.save()
            admin_status = (
                "with admin privileges"
                if updated_user.is_staff
                else "without admin privileges"
            )
            messages.success(
                request,
                f"User {updated_user.username} updated successfully {admin_status}!",
            )
            return redirect("manage_users")
    else:
        form = UserEditForm(instance=user)
    return render(
        request, "edit_user.html", {"form": form, "user": user, "action": "Edit"}
    )


@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        if user != request.user:  # Prevent self-deletion
            username = user.username
            user.delete()
            messages.success(request, f"User {username} deleted successfully!")
        else:
            messages.error(request, "You cannot delete your own account!")
    return redirect("manage_users")
