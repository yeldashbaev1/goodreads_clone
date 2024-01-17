from django.urls import path
from rest_framework.routers import DefaultRouter

# from api.views import BookReviewDetailAPIView, BookReviewsAPIView
from api.views import BookReviewViewSet

app_name = "api"

router = DefaultRouter()
router.register('reviews', BookReviewViewSet, basename='review')
urlpatterns = router.urls
