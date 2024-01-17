from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import BookReview
from api.serializers import BookReviewSerializer


class BookReviewDetailAPIView(APIView):
    def get(self, request, id):
        book_review = BookReview.objects.get(id=id)

        serializer = BookReviewSerializer(book_review)

        return Response(data=serializer.data)


class BookListAPIView(APIView):
    def get(self, request):
        book_review = BookReview.objects.all()
        serializer = BookReviewSerializer(book_review, many=True)
        return Response(data=serializer.data)