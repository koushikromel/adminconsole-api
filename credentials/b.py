
import inspect
import requests

# Make a request to the FastAPI endpoint
response = requests.get('http://localhost:8118/docs')  # Replace with your endpoint URL

# Retrieve the docstring from the endpoint function
path = '/absentees'  # Replace with the actual path of your API endpoint
method = 'GET'  # Replace with the actual HTTP method of your API endpoint

# Retrieve the endpoint function from the OpenAPI documentation
paths = response.json()['paths']
endpoint_info = paths.get(path, {})
endpoint = endpoint_info.get(method.lower(), {})
handler = endpoint.get('operationId')

# Retrieve the docstring from the endpoint function
docstring = inspect.getdoc(globals()[handler])

print(docstring)
