import requests, os
from dotenv import load_dotenv
load_dotenv()

r = requests.get(
    'https://openrouter.ai/api/v1/models',
    headers={'Authorization': f'Bearer {os.getenv("OPENROUTER_API_KEY")}'}
)
models = [m['id'] for m in r.json()['data'] if ':free' in m['id']]
print('\n'.join(sorted(models)))
