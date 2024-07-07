import openai

# Modèles spécifiés
modele_1 = "ft:gpt-3.5-turbo-0125:efrei:180624chatfalcon:9bTYWnRd:ckpt-step-909"
modele_2 = "ft:gpt-3.5-turbo-0125:efrei:180624chatfalcon:9bTYWlQl:ckpt-step-1818"
modele_3 = "ft:gpt-3.5-turbo-0125:efrei:180624chatfalcon:9bTYWi82"
models = [modele_1, modele_2, modele_3]

def is_valid_api_key(api_key):
    try:
        openai.api_key = api_key
        openai.Model.list()  # Effectue une requête simple pour vérifier la validité
        return True
    except Exception:
        return False

def get_gpt_response(system_prompt, user_prompt, model):
    # Prepare the messages as a list of dictionaries
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # Call the OpenAI API to get the response
    chat_completion = openai.ChatCompletion.create(
        messages=messages,
        model=model
    )

    # Extract and return the response text
    return chat_completion.choices[0].message['content']

def translate_to_falc(text):
    system_prompt = "Transforme ce texte en FALC:"
    user_prompt = text
    for model in models:
        try:
            falc_text = get_gpt_response(system_prompt, user_prompt, model)
            return falc_text
        except Exception as e:
            print(f"Erreur avec le modèle {model}: {e}")
            continue
    return "Erreur: Aucun modèle n'a pu générer une traduction FALC."

