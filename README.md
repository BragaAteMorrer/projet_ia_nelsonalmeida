
# Projet LLM - Ollama

## Description
Ce projet propose une interface pour interagir avec des fichiers texte, PDF, ou JSON en utilisant Ollama, un modèle de langage de grande taille (LLM). Il est possible de poser des questions à l'IA sur le contenu des fichiers après traitement et conversion.

Le projet inclut des fonctionnalités pour :
- Télécharger des fichiers depuis Google Drive.
- Traiter des fichiers texte, PDF, et JSON pour les transformer en données exploitables.
- Intégrer un modèle Ollama pour des discussions contextuelles ou non-contextuelles (Non-RAG).

## Fonctionnalités
1. **Téléchargement de fichiers** : Téléchargez des fichiers directement depuis Google Drive ou via votre ordinateur.
2. **Extraction et analyse** :
   - Conversion de fichiers PDF en texte exploitable.
   - Chargement de fichiers texte et JSON.
   - Division du contenu en morceaux adaptés au modèle.
3. **Interaction avec l'IA** :
   - Mode RAG (Récupération Assistée par Génération) : Posez des questions contextualisées basées sur les documents.
   - Mode Non-RAG : Posez des questions sans se baser sur un contexte externe, pour des réponses générées uniquement à partir des connaissances internes du modèle.

## Prérequis
- Python 3.12 ou plus récent.
- Ollama installé (instructions ci-dessous).
- Environnements compatibles avec les bibliothèques nécessaires (voir `requirements.txt`).

## Installation
1. Clonez ce dépôt ou téléchargez les fichiers.
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
3. Téléchargez et installez Ollama depuis [leur site officiel](https://ollama.com/download).
4. Préparez les modèles nécessaires :
   ```bash
   ollama pull llama3
   ollama pull mxbai-embed-large
   ```

## Utilisation
### Mode RAG
1. **Préparation du fichier** :
   - Lancez `upload.py` pour télécharger ou sélectionner un fichier à analyser.
   - Le fichier sera traité et le contenu sera enregistré dans `analysefichier.txt`.

2. **Interaction contextualisée** :
   - Exécutez `interactionia.py` pour interagir avec le contenu du fichier.
   - Posez vos questions en vous basant sur le contenu analysé.

3. **Exemple de commande** :
   ```bash
   python interactionia.py --model llama3 --temperature 0.7
   ```

### Mode Non-RAG
1. **Interaction non-contextualisée** :
   - Exécutez `interactionia_nonrag.py` pour interagir avec le modèle sans utiliser de contexte externe.
   - Le modèle répond uniquement en fonction de ses connaissances internes.

2. **Exemple de commande** :
   ```bash
   python interactionia_nonrag.py --model llama3 --temperature 0.5
   ```

## Configuration des modèles
### Paramètre de température
La température contrôle la créativité du modèle :
- Valeurs basses (e.g., 0.1) : Réponses plus déterministes et précises.
- Valeurs élevées (e.g., 0.8) : Réponses plus variées et créatives.

Pour ajuster la température, vous suffira de modifier cet ligne de code afin de pouvoir avoir la réponse la plus déterministe comme la plus créative (entre 0.1 et 1.0)
```bash
    response = client.chat.completions.create(
        model=ollama_model,
        messages=[{"role": "system", "content": prompt}],
        max_tokens=200,
        n=1,
        **temperature=0.1,**
    )
```

## Arborescence du projet
```
├── analysefichier.txt  # Fichier de stockage des données analysées.
├── config.yaml         # Fichier de configuration du projet.
├── interactionia.py    # Script principal pour le mode RAG.
├── interactionia_nonrag.py  # Script principal pour le mode Non-RAG.
├── upload.py           # Script pour gérer le téléchargement et le traitement des fichiers.
├── requirements.txt    # Liste des dépendances.
├── vault.txt           # Exemple de contenu d'un fichier analysé.
```

## Auteurs
Ce projet a été développé pour démontrer les capacités d'interaction avec des fichiers via Ollama.
