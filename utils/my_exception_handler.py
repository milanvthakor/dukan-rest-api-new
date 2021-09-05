from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
	# Call REST framework's default exception handler first,
    # to get the standard error response.
	response = exception_handler(exc, context)

	# Update the structure of the response data.
	if response is not None:
		custom_response = {}
		custom_response['response'] = 'Error'

		print(response.data.items())
		for key, value in response.data.items():
			# if value is type of list, get the first item
			if isinstance(value, list):
				try: 		
					custom_response['message'] = value[0]
				except IndexError:
					custom_response['message'] = 'Something went wrong.'
			# if it is string
			elif isinstance(value, str):
				custom_response['message'] = value

			break	#break immediately after first error message 

		response.data = custom_response

	return response