from openai import OpenAI
import os

modele_1 = "ft:gpt-3.5-turbo-0125:efrei:180624chatfalcon:9bTYWnRd:ckpt-step-909"
modele_2 = "ft:gpt-3.5-turbo-0125:efrei:180624chatfalcon:9bTYWlQl:ckpt-step-1818"
modele_3 = "ft:gpt-3.5-turbo-0125:efrei:180624chatfalcon:9bTYWi82"

try:
    from config import api_key
except ImportError:
    api_key = os.getenv('API_KEY')  # Utilisation d'une variable d'environnement comme fallback

client = OpenAI(api_key=api_key)

def get_gpt_response(system_prompt, user_prompt, model):
    # Prepare the messages as a list of dictionaries
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # Call the OpenAI API to get the response
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model
    )

    # Extract and return the response text
    return chat_completion.choices[0].message.content


# Example usage
system_prompt = """<CONTEXTE>
Tu es linguiste spécialisé dans le FALC, Facile à Lire et à Comprendre (easy to read en anglais), qui est une méthode de simplification de textes pour les rendre plus accessibles à une partie de la population Francophone. 

Ton objectif est de transcrire un texte en français vers le FALC.
</CONTEXTE>

<EXEMPLE>
Input : 
"Le CVS est un lieu d’expression qui permet à toutes les personnes concernées par la vie de l'établissement de donner leur avis, d'être informés, de communiquer et de se concerter afin de trouver des solutions pertinentes."

Output : 
"Le CVS permet à toutes les personnes concernées de :

 - Donner leur avis
 - Être informés
 - Discuter
 - Se concerter, trouver des solutions"
</EXEMPLE>"""

user_prompt = "Actuellement en dernière année d'école d'ingénieur à l'EFREI Paris, spécialité Systèmes Embarqués, je suis à la recherche d'une opportunité d'alternance d'une durée de 12 mois débutant en novembre 2024, disponible pour une mobilité sur toute la France.Avec une solide formation en systèmes embarqués et une expérience significative en conception et développement de solutions embarquées, je suis prêt à relever de nouveaux défis et contribuer à des projets innovants au sein de votre entreprise."

# Get the response from the model
response = get_gpt_response(system_prompt, user_prompt, modele_1)

print("Model Response:", response)