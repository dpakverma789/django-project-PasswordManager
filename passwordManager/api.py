from .serializer import CredentialSerializer
from rest_framework.decorators import api_view
from .models import Credentials
from rest_framework.response import Response


@api_view(['GET'])
def fetch_credentials(request, login_user=None):
    queryset = Credentials.objects.filter(login_user=login_user)
    serializer = CredentialSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def post_credentials(request):
    status = 'Failed'
    message = f"{request.data.get('website')} already exist in {request.data.get('login_user')} account"
    serializer = CredentialSerializer(data=request.data)
    if Credentials.objects.filter(website=request.data.get('website'), login_user=request.data.get('login_user')).count() == 0:
        message = "Invalid Data Format"
        if serializer.is_valid():
            serializer.save()
            status = 'Success'
            message = 'Data Saved!'
    return Response({'status': status, 'message': message})