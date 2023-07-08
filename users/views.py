from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import CustomUser
from users.serializers import MyTokenObtainPairSerializer, UserSerializer
from rest_framework.views import APIView

def is_user_admin(request):
        """
        Check if the user is admin

        :param request: request object

        :return: boolean
        """
        token = AccessToken(request.headers.get('Authorization', None).split(' ')[1])
        decoded_token = token.payload
        # is_admin = CustomUser.objects.get(id=decoded_token['user_id']).is_admin
        is_admin = decoded_token['is_admin']

        return is_admin
            
class CreateUserAPIView(APIView):
    
    def post(self, request):
        """
        Create a new user

        :param request: request object

        :return: JSON response
        """
        user = request.data
        
        if is_user_admin(request):
            serializer = UserSerializer(data=user)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({"message":"401"},status=status.HTTP_401_UNAUTHORIZED)
    
class UpadteUserAPIView(APIView):
    
    def put(self, request, pk):
        """
        Update a user

        :param request: request object

        :return: JSON response
        """
        password = request.data['password']
        
        if is_user_admin(request):
            try:
                user = CustomUser.objects.get(id=pk)
                if password:
                    # Get the new password from the request data
                    serializer = UserSerializer(user, data=request.data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return JsonResponse(serializer.data, status=status.HTTP_200_OK)
                else:
                    msg = {'error': 'password not found in request'}
                    raise Exception(msg)
            except Exception as e:
                
                return JsonResponse(str(e),status=status.HTTP_400_BAD_REQUEST)

        else:
            return JsonResponse({"message":"401"},status=status.HTTP_401_UNAUTHORIZED)
    

class MyTokenObtainPairView(TokenObtainPairView):
     
     def post(self, request, *args, **kwargs):
        '''Customize the token response with user role
        
        :param request: request object
        :param args: arguments
        :param kwargs: keyword arguments
        
        :return: JSON response
        '''
        username = request.data['username']
        password = request.data['password']

        user = CustomUser.objects.get(username=username, password=password)
        
        refresh = MyTokenObtainPairSerializer.get_token(user)
        super().get_authenticate_header(request)
        return JsonResponse({
                            'refresh':str(refresh),
                            'access':str(refresh.access_token) 
                            },
                            status=status.HTTP_200_OK)
        

class LogoutView(APIView):

    def post(self, request):
        '''
        Logout a user

        :param request: request object

        :return: JSON response
        '''
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(request.data.get('refresh'))
            token.blacklist()
            return JsonResponse({"message":"Logged out"},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return JsonResponse({"message":"403"},status=status.HTTP_400_BAD_REQUEST)

