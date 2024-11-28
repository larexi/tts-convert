from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ttsconvert.models import ConversionRequest
from ttsconvert.serializers import ConversionRequestSerializer


class TTSConversionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
    CRUD endpoint for managing ConversionRequests

    GET /tts-convert/?id=id
    POST /tts-convert/
    DELETE /tts-convert/
    """

    def get(self, request):
        pk = request.GET.get('request_id')
        conversion_request = get_object_or_404(ConversionRequest, pk=pk, created_by=request.user.id)
        serializer = ConversionRequestSerializer(conversion_request)

        return JsonResponse(serializer.data)
        

    def post(self, request):
        data = JSONParser().parse(request)
        data.update({'created_by': request.user.id})
        serializer = ConversionRequestSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
        return JsonResponse(serializer.errors, status=400)


    def delete(self, request):
        
        pk = request.data.get('id')

        conversion_request = get_object_or_404(ConversionRequest, pk=pk, created_by=request.user.id)
        conversion_request.delete()

        return HttpResponse(status=200)
    