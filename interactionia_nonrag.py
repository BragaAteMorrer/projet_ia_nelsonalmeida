import argparse
import json

JAUNE = '\033[93m'
ROUGE = '\033[91m'
VERT = '\033[92m'
BLEU = '\033[94m'
RESET_COULEUR = '\033[0m'

def ollama_chat_non_rag(user_input, system_message, ollama_model, conversation_history):
    """Gère les conversations en utilisant uniquement le modèle (Non RAG)."""
    conversation_history.append({"role": "user", "content": user_input})
    
    messages = [
        {"role": "system", "content": system_message},
        *conversation_history
    ]
    
    response = {
        "choices": [
            {"message": {"content": f"Voici une réponse fictive pour : {user_input}"}}
        ]
    }
    
    conversation_history.append({"role": "assistant", "content": response["choices"][0]["message"]["content"]})
    return response["choices"][0]["message"]["content"]

print(JAUNE + "Démarrage du modèle sans récupération de contexte (Non RAG)" + RESET_COULEUR)

# Analyse des arguments de ligne de commande
parser = argparse.ArgumentParser(description="Ollama Chat Non RAG")
parser.add_argument("--model", default="llama3", help="Ollama model to use (default: llama3)")
args = parser.parse_args()

conversation_history = []
system_message = "Vous êtes un assistant qui répond uniquement en fonction de ses connaissances internes."

# Boucle principale
while True:
    user_input = input(BLEU + "Pose une question (ou tape 'quitter' pour quitter) : " + RESET_COULEUR)
    if user_input.lower() == 'quitter':
        break
    
    try:
        response = ollama_chat_non_rag(user_input, system_message, args.model, conversation_history)
        print(VERT + "Réponse : \n\n" + response + RESET_COULEUR)
    except Exception as e:
        print(ROUGE + f"Erreur : {e}" + RESET_COULEUR)