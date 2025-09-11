import sys
sys.path.append('.')
import openai
from app.core.config import settings

print('Testing OpenAI API key...')
print(f'API Key configured: {bool(settings.OPENAI_API_KEY)}')
if settings.OPENAI_API_KEY:
    print(f'API Key starts with: {settings.OPENAI_API_KEY[:10]}...')
else:
    print('API Key: None')

# Test direct OpenAI client initialization
try:
    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    print('Direct OpenAI client initialized successfully')

    # Test a simple API call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=5
    )
    print('API call successful!')
    print(f'Response: {response.choices[0].message.content}')

except Exception as e:
    print(f'Direct OpenAI client error: {e}')

# Now test our service
from app.services.openai_service import OpenAIService
service = OpenAIService()
print(f'OpenAI service client initialized: {service.client is not None}')
