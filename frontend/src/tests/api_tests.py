import httpx
from rich import print

url = "http://127.0.0.1:8000/api/v1/reviews/stats/LWY12"

response = httpx.get(url)

print(response.status_code)
print(response.json())
