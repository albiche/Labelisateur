import os
from openai import OpenAI

# main.py
import os

try:
    from config import api_key
except ImportError:
    api_key = os.getenv('API_KEY')  # Utilisation d'une variable d'environnement comme fallback

client = OpenAI(api_key=api_key)


def test_gpt4_api():
    try:
        response = client.chat.completions.create(
            model="gpt-4-0613",
            messages=[
                {
                    "role": "user",
                    "content": "Dites-moi quelque chose d'intéressant sur les étoiles."
                }
            ],
            max_tokens=50
        )
        print("Réponse du modèle :")
        print(response.choices[0].message.content.strip())
    except Exception as e:
        print("Erreur lors de l'appel à l'API :", e)

test_gpt4_api()