from django.urls import path

from apps.ratings.views import create_agent_review

urlpatterns = [path("<str:profile_id>/", create_agent_review, name="create-rating")]
