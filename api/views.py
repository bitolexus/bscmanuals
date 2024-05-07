# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework import views, status
from rest_framework.response import Response
from .models import Manual
from .serializers import ManualSerializer
from .utils.user_manual_processing import main as process_manual

class ManualUploadView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = ManualSerializer(data=request.data)
        if serializer.is_valid():
            manual = serializer.save()

            return Response({"manual_id": manual.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ManualSectionView(views.APIView):
    def get(self, request, id, section_name, *args, **kwargs):
        try:
            manual = Manual.objects.get(id=id)
            if not manual.result:
                uploaded_file_path = manual.file.path
                manual.result = process_manual(uploaded_file_path)
                manual.save()
        except Manual.DoesNotExist:
            return Response({"error": "Manual not found."}, status=status.HTTP_404_NOT_FOUND)


        return Response( manual.result)


