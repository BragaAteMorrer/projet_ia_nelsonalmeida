
# Projet LLM - Ollama

## Description
Ce projet propose une interface pour interagir avec des fichiers texte, PDF, ou JSON en utilisant Ollama, un modèle de langage de grande taille (LLM). Il est possible de poser des questions à l'IA sur le contenu des fichiers après traitement et conversion.

Le projet inclut des fonctionnalités pour :
- Télécharger des fichiers depuis Google Drive.
- Traiter des fichiers texte, PDF, et JSON pour les transformer en données exploitables.
- Intégrer un modèle Ollama pour des discussions contextuelles sur le contenu des fichiers.

## Fonctionnalités
1. **Téléchargement de fichiers** : Téléchargez des fichiers directement depuis Google Drive ou via votre ordinateur.
2. **Extraction et analyse** :
   - Conversion de fichiers PDF en texte exploitable.
   - Chargement de fichiers texte et JSON.
   - Division du contenu en morceaux adaptés au modèle.
3. **Interaction avec l'IA** : Utilisez les modèles Ollama pour poser des questions sur les fichiers et obtenir des réponses contextuelles.

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
1. **Préparation du fichier** :
   - Lancez `upload.py` pour télécharger ou sélectionner un fichier à analyser.
   - Le fichier sera traité et le contenu sera enregistré dans `analysefichier.txt`.

2. **Analyse et discussion** :
   - Exécutez `interactionia.py` pour interagir avec le contenu du fichier en utilisant l'IA.
   - Posez vos questions à l'IA via la console pour des réponses précises et contextualisées.

3. **Exemples de commandes** :
   ```bash
   python upload.py
   python interactionia.py
   ```

## Configuration des modèles
Pour ajuster les paramètres de créativité et de température d'Ollama :
```bash
ollama run llama3
/set parameter temperature <valeur>
```

## Arborescence du projet
```
├── analysefichier.txt  # Fichier de stockage des données analysées.
├── config.yaml         # Fichier de configuration du projet.
├── interactionia.py    # Script principal pour interagir avec l'IA.
├── upload.py           # Script pour gérer le téléchargement et le traitement des fichiers.
├── requirements.txt    # Liste des dépendances.
├── vault.txt           # Exemple de contenu d'un fichier analysé.
```

## Auteurs
Ce projet a été développé pour démontrer les capacités d'interaction avec des fichiers via Ollama.

## License
Y'en a pas
