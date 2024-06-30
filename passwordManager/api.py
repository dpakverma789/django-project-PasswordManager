from .serializer import CredentialSerializer
from rest_framework.decorators import api_view
from .models import Credentials
from rest_framework.response import Response
from .views import export


# @api_view(['GET'])
# def fetch_credentials(request, login_user=None):
#     queryset = Credentials.objects.filter(login_user=login_user)
#     serializer = CredentialSerializer(queryset, many=True)
#     return Response(serializer.data)

@api_view(['POST'])
def fetch_credentials(request):
    response = False
    login_user = request.data.get('login_user')
    queryset = Credentials.objects.filter(login_user=login_user)
    message = f"{login_user} do not exist" if login_user else "Username required"
    return_response = {'response': response, 'message': message}
    if queryset:
        response = True
        message = "Records Found"
        serializer = CredentialSerializer(queryset, many=True)
        return_response.update({'response': response, 'message': message, 'data': serializer.data})
    return Response(return_response)


@api_view(['POST'])
def delete_credentials(request):
    response = queryset = False
    message = 'Invalid Data'
    login_user = request.data.get('login_user')
    website = request.data.get('website')
    # website and login_user both are send
    if website and login_user:
        queryset = Credentials.objects.filter(website=website, login_user=login_user)
        if not queryset:
            message = f"{website} not found for user {login_user}"
    # No login user
    if not login_user and website:
        message = "Username required"
    # login user but not website
    if not website and login_user:
        queryset = Credentials.objects.filter(login_user=login_user)
        message = f"{login_user} does not exist!"
    if queryset:
        response = True
        message = f"{website} Deleted" if website else f"All website deleted for {login_user}"
        queryset.delete()
    return Response({'response': response, 'message': message})


@api_view(['POST'])
def update_credentials(request):
    response = queryset = False
    message = 'Invalid Data'
    login_user = request.data.get('login_user')
    website = request.data.get('website')
    column_name = request.data.get('columnName')
    column_value = request.data.get('columnValue')
    # website and login_user both are send
    if website and login_user:
        queryset = Credentials.objects.get(website=website, login_user=login_user)
        if not queryset:
            message = f"{website} not found for user {login_user}"
    if queryset and column_name and column_value:
        response = True
        message = f"{column_name} updated!"
        if column_name.lower() == 'website':
            queryset.website = column_value
        if column_name.lower() == 'username':
            queryset.username = column_value
        if column_name.lower() == 'password':
            queryset.password = column_value
        queryset.save()
    return Response({'response': response, 'message': message})


@api_view(['POST'])
def post_credentials(request):
    response = False
    message = "Invalid Data!"
    user_credentials = request.data
    if user_credentials:
        serializer = CredentialSerializer(data=user_credentials)
        if serializer.is_valid():
            serializer.save()
            response = True
            message = "Data Saved Successfully!"
    return Response({"response": response, "message": message})
