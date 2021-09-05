from rest_framework import serializers

from user.models import User

class RegistrationSerializer(serializers.ModelSerializer):

	# as password 2 field is not in Account, so manually adding that to serializer
	password2 = serializers.CharField(style={'input_type': 'password'}, 
			write_only=True,
			error_messages={'required': 'Confirm Password is required.'}
		)

	class Meta:
		model = User
		# name of fields need for registration
		fields = ['email', 'password', 'password2', 'name', 'date_of_birth', 'phone', 'gender', 'city']
		# for security, password will not readable when passed to the server
		extra_kwargs = {
			'password': {'write_only': True},
			# changed the validation message with the custom one
			'email': {'error_messages': {'required': 'Email address is required.'}},
			'password': {'error_messages': {'required': 'Password is required.'}},
			'date_of_birth': {'error_messages': {'invalid': 'Date of Birth must have format of YYYY-MM-DD.'}},
			'gender': {'error_messages': {'invalid_choice': 'Gender must be either Male, Female or Other.'}}
		}

	# before saving this user into database, we need to make sure that both passwords are matching
	def save(self):
		user = User(
				email = self.validated_data['email'],
				name = self.validated_data.get('name', None), # if the name exists then only get that value
				date_of_birth = self.validated_data.get('date_of_birth', None),
				phone = self.validated_data.get('phone', None),
				gender = self.validated_data.get('gender', None),
				city = self.validated_data.get('city', None),
			)
		password 	= self.validated_data['password']
		password2 	= self.validated_data['password2']

		if password != password2:
			raise serializers.ValidationError({
					'message': 'Both passwords are different.'
				})

		user.set_password(password)
		user.save()

		return user