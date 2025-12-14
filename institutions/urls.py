from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import add_review, RecordListView, RecordCreateView, RecordUpdateView, RecordDeleteView
from allauth.account.views import LoginView

urlpatterns = [
    path("", views.EducationView.as_view()),
    path("accounts/", include("allauth.urls")),
    path("login/", LoginView.as_view(template_name="education/login.html"), name="login"),  # Вход
    # path("profile/", views.logout_view, name="profile"),  # Профиль
    path("profile/", views.profile_view, name="profile"),
    path("logout/", views.logout_view, name="logout"),

    path("register/", views.register, name="register"),  # Регистрация
    path("admin-panel/", views.admin_panel_redirect, name="admin_panel"),

    path("filter/", views.FilterInstitutionView.as_view(), name="filter"),
    path("search/", views.Search.as_view(), name="search"),
    path("add-rating/", views.AddStarRating.as_view(), name="add_rating"),
    path("<slug:slug>/", views.InstitutionDetailView.as_view(), name="institution_detail"),
    path("<slug:slug>/", views.InstitutionDetailView.as_view(), name="education_detail"),
    path('add_review/<int:institution_id>/', add_review, name='add_review'),
]

