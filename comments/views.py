from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Comment
from .serializers.common import CommentSerializer
from .serializers.populated import PopulatedCommentSerializer

class CommentListView(APIView):
    permission_classes =(IsAuthenticatedOrReadOnly,)

    def get(self, request):
        event_id = request.query_params.get('event_id')

        if event_id:
            comments = Comment.objects.filter(event_id=event_id)
        else:
            comments = Comment.objects.all()

        serialized_comments = PopulatedCommentSerializer(comments, many=True)
        return Response(serialized_comments.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        request.data['user'] = request.user.id

        comment_to_add = CommentSerializer(data=request.data)
        try:
            comment_to_add.is_valid(raise_exception=True)
            comment_to_add.save()
            saved_comment = Comment.objects.get(pk=comment_to_add.data['id'])
            return Response(
                PopulatedCommentSerializer(saved_comment).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                e.__dict__ if e.__dict__ else str(e),
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

class CommentDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_comment(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound(detail="Can't find that comment")

    def get(self, _request, pk):
        comment = self.get_comment(pk=pk)
        serialized_comment = PopulatedCommentSerializer(comment)
        return Response(serialized_comment.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        comment_to_update = self.get_comment(pk=pk)

        if comment_to_update.user != request.user:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        updated_comment = CommentSerializer(
            comment_to_update,
            data=request.data,
            partial=True
        )

        if updated_comment.is_valid():
            updated_comment.save()
            return Response(
                PopulatedCommentSerializer(comment_to_update).data,
                status=status.HTTP_202_ACCEPTED
            )

        return Response(
            updated_comment.errors,
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    
    def delete(self, request, pk):
        comment_to_delete = self.get_comment(pk=pk)

        if comment_to_delete.user != request.user:
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        comment_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   


