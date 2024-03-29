from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import ocrmypdf
from subprocess import Popen

from .serializers import FileSerializer
from .models import Post

# Create your views here.
class PostViews(APIView):
    parser_classes = (MultiPartParser, FormParser)


    def get(self,request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = FileSerializer(posts, many=True)
        return Response(serializer.data)


    def post(self, request, *args, **kwargs):

        posts_serializer = FileSerializer(data=request.data)
        if posts_serializer.is_valid():
            uploaded = posts_serializer.save()
            process = Popen(['ocrmypdf', uploaded.file.path, 'output.pdf'], cwd="../media/post_files")
            posts_serializer.save(process)

            return Response(posts_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', posts_serializer.errors)
            return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
