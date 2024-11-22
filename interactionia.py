import torch
import ollama
import os
from openai import OpenAI
import argparse
import json

JAUNE = '\033[93m'
ROUGE = '\033[91m'
VERT = '\033[92m'
BLEU = '\033[94m'
RESET_COULEUR = '\033[0m'

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def get_relevant_context(rewritten_input, vault_embeddings, vault_content, top_k=3):
    if vault_embeddings.nelement() == 0:
        return []
    input_embedding = ollama.embeddings(model='mxbai-embed-large', prompt=rewritten_input)["embedding"]
    cos_scores = torch.cosine_similarity(torch.tensor(input_embedding).unsqueeze(0), vault_embeddings)
    top_k = min(top_k, len(cos_scores))
    top_indices = torch.topk(cos_scores, k=top_k)[1].tolist()
    relevant_context = [vault_content[idx].strip() for idx in top_indices]
    return relevant_context

def rewrite_query(user_input_json, conversation_history, ollama_model):
    user_input = json.loads(user_input_json)["Query"]
    context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history[-2:]])
    prompt = f"""Rewrite the following query by incorporating relevant context from the conversation history.
    The rewritten query should:
    
    - Preserve the core intent and meaning of the original query
    - Expand and clarify the query to make it more specific and informative for retrieving relevant context
    - Avoid introducing new topics or queries that deviate from the original query
    - DONT EVER ANSWER the Original query, but instead focus on rephrasing and expanding it into a new query
    
    Return ONLY the rewritten query text, without any additional formatting or explanations.
    
    Conversation History:
    {context}
    
    Original query: [{user_input}]
    
    Rewritten query: 
    """
    response = client.chat.completions.create(
        model=ollama_model,
        messages=[{"role": "system", "content": prompt}],
        max_tokens=200,
        n=1,
        temperature=0.1,
    )
    rewritten_query = response.choices[0].message.content.strip()
    return json.dumps({"Rewritten Query": rewritten_query})
   
def ollama_chat(user_input, system_message, vault_embeddings, vault_content, ollama_model, conversation_history):
    conversation_history.append({"role": "user", "content": user_input})
    
    if len(conversation_history) > 1:
        query_json = {
            "Query": user_input,
            "Rewritten Query": ""
        }
        rewritten_query_json = rewrite_query(json.dumps(query_json), conversation_history, ollama_model)
        rewritten_query_data = json.loads(rewritten_query_json)
        rewritten_query = rewritten_query_data["Rewritten Query"]
        print(ROUGE + "Original Query: " + user_input + RESET_COULEUR)
        print(ROUGE + "Rewritten Query: " + rewritten_query + RESET_COULEUR)
    else:
        rewritten_query = user_input
    
    relevant_context = get_relevant_context(rewritten_query, vault_embeddings, vault_content)
    if relevant_context:
        context_str = "\n".join(relevant_context)
        print("Contenu récupéré des fichiers: \n\n" + JAUNE + context_str + RESET_COULEUR)
    else:
        print(ROUGE + "No relevant context found." + RESET_COULEUR)
    
    user_input_with_context = user_input
    if relevant_context:
        user_input_with_context = user_input + "\n\nRelevant Context:\n" + context_str
    
    conversation_history[-1]["content"] = user_input_with_context
    
    messages = [
        {"role": "system", "content": system_message},
        *conversation_history
    ]
    
    response = client.chat.completions.create(
        model=ollama_model,
        messages=messages,
        max_tokens=2000,
    )
    
    conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
    
    return response.choices[0].message.content

print(JAUNE + "Démarrage du modèle pour l'API" + RESET_COULEUR)
parser = argparse.ArgumentParser(description="Ollama Chat")
parser.add_argument("--model", default="llama3", help="Ollama model to use (default: llama3)")
args = parser.parse_args()

print(JAUNE + "Initialisation du client" + RESET_COULEUR)
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='llama3'
)

print(JAUNE + "Récupération des fichiers" + RESET_COULEUR)
vault_content = []
if os.path.exists("analysefichier.txt"):
    with open("analysefichier.txt", "r", encoding='utf-8') as vault_file:
        vault_content = vault_file.readlines()

print(JAUNE + "Génération des embeddings pour le contenu des fichiers stockés" + RESET_COULEUR)
vault_embeddings = []
for content in vault_content:
    response = ollama.embeddings(model='mxbai-embed-large', prompt=content)
    vault_embeddings.append(response["embedding"])

vault_embeddings_tensor = torch.tensor(vault_embeddings) 

print(JAUNE + "Démarrage du système" + RESET_COULEUR)
conversation_history = []
system_message = "Vous êtes un assistant utile et expert dans l'extraction des informations les plus pertinentes à partir d'un texte donné. Vous apportez également des informations supplémentaires pertinentes à la requête de l'utilisateur, même en dehors du contexte fourni."

while True:
    user_input = input(BLEU + "Pose une question a propos de tes documents (ou tape 'quitter' pour quitter ou alors CTRL+C) " + RESET_COULEUR)
    if user_input.lower() == 'quitter':
        break
    
    response = ollama_chat(user_input, system_message, vault_embeddings_tensor, vault_content, args.model, conversation_history)
    print(VERT + "Response: \n\n" + response + RESET_COULEUR)
