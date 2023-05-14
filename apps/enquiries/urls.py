from django.urls import path

from apps.enquiries.views import send_enquiry_email

urlpatterns = [path("", send_enquiry_email, name="send-enquiry")]
