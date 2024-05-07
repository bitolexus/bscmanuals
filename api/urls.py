from django.urls import re_path
from .views import ManualUploadView, ManualSectionView

urlpatterns = [
    re_path(r'^manual/upload$', ManualUploadView.as_view(), name='manual-upload'),
    re_path(r'^manual/(?P<id>[0-9]+)/(?P<section_name>[a-zA-Z0-9_]+)$', ManualSectionView.as_view(), name='manual-section'),
]