from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from user.api.serializers import RegistrationSerializer
from user.models import User

@api_view(['POST'])
def api_registration_view(request):

	if request.method == 'POST':
		
		data = {}
		email = request.data.get('email', '0').lower()

		if validate_email(email) != None:
			data['response'] = 'Error'
			data['message'] = 'Email address already exists.'
			return Response(data)

		serializer = RegistrationSerializer(data=request.data)
		# raise_exception is required for custom_exception to trigger
		if serializer.is_valid(raise_exception=True):
			user = serializer.save()
			token = Token.objects.get(user=user)

			data['response'] = 'Success'
			data['message'] = 'Registered Successfully.'
			data['pk'] = user.pk
			data['email'] = user.email
			data['token'] = token.key

			return Response(data)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# check if email already exists in db or not
def validate_email(email):
	user = None
	
	try:
		user = User.objects.get(email=email)
	except User.DoesNotExist:
		return None
	
	if user != None:
		return email

# login
# class based view (Custom Obtain Auth Token View)
class APILoginView(APIView):

	authentication_classes = []
	permission_classes = []

	def post(self, request):
		context = {}

		email = request.POST.get('email')
		password = request.POST.get('password')
		# authenticate user via email and password
		user = authenticate(email=email, password=password)
		if user:
			# if there is no token then create one
			try:
				token = Token.objects.get(user=user)
			except Token.DoesNotExist:
				token = Token.objects.create(user=user)

			context['response'] = 'Success'
			context['message'] = 'Login Successfully.'
			context['pk'] = user.pk
			context['email'] = user.email
			context['token'] = token.key
		else:
			context['response'] = 'Error'
			context['message'] = 'Invalid email or password.'

		return Response(context)