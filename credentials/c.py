
import requests

def get_current_time():
  """Gets the current time from the API.

  Returns:
    A datetime object representing the current time.

  Raises:
     requests.exceptions.HTTPError: If the API call fails.
  """

  response = requests.get("http://localhost:8118/absentees")
  if response.status_code != 200:
    raise requests.exceptions.HTTPError(response)

  # current_time = response.json()["time"]
  return current_time

if __name__ == "__main__":
  current_time = get_current_time()
  print(current_time)