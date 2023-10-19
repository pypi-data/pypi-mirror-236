from django.urls import path
from django.views.generic import TemplateView

from django_silica.tests.components.ConcurrencyTest import ConcurrencyTest
from django_silica.tests.components.Lifecycle import Lifecycle
from django_silica.tests.components.TagProps import TagProps

class ConcurrencyTestView(TemplateView):
    template_name = "concurrency_test_view.html"

class TagPropsView(TemplateView):
    template_name = "tag_props_view.html"

urlpatterns = [
    path("lifecycle", Lifecycle.as_view(), name="lifecycle"),
    path("silica/tests/concurrency", ConcurrencyTestView.as_view()),
    path("silica/tests/tag-props", TagPropsView.as_view()),
    # ... add more testing URLs as needed
]
