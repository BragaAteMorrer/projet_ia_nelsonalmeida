import os
import tkinter as tk
from tkinter import filedialog, simpledialog, ttk
import PyPDF2
import re
import json
import requests
import csv

def reinitialiser_fichier():
    with open("analysefichier.txt", "w", encoding="utf-8") as fichier_coffre:
        fichier_coffre.write("")
    print("Fichier 'analysefichier.txt' réinitialisé.")

def telecharger_depuis_google_drive():
    lien = simpledialog.askstring("Google Drive", "Entrez le lien de partage Google Drive :")
    if lien:
        try:
            if "id=" in lien:
                fichier_id = lien.split("id=")[1]
            elif "/d/" in lien:
                fichier_id = lien.split("/d/")[1].split("/")[0]
            else:
                print("Lien Google Drive invalide.")
                return
            
            url = f"https://drive.google.com/uc?id={fichier_id}&export=download"
            reponse = requests.get(url, stream=True)
            if reponse.status_code != 200:
                print("Erreur lors du téléchargement : Vérifiez le lien Google Drive.")
                return
            
            chemin_temp = "fichier_temporaire.pdf"
            with open(chemin_temp, "wb") as fichier:
                for chunk in reponse.iter_content(chunk_size=8192):
                    fichier.write(chunk)
            
            print("Fichier téléchargé avec succès depuis Google Drive.")
            reinitialiser_fichier()
            convertir_pdf_en_texte(chemin_temp)
            os.remove(chemin_temp)
        except Exception as e:
            print(f"Erreur lors du téléchargement depuis Google Drive : {str(e)}")

def convertir_pdf_en_texte(chemin_fichier=None):
    if not chemin_fichier:
        chemin_fichier = filedialog.askopenfilename(filetypes=[("Fichiers PDF", "*.pdf")])
    if chemin_fichier:
        try:
            with open(chemin_fichier, 'rb') as fichier_pdf:
                lecteur_pdf = PyPDF2.PdfReader(fichier_pdf)
                texte = ''
                for page in lecteur_pdf.pages:
                    if page.extract_text():
                        texte += page.extract_text() + " "
                
                texte = re.sub(r'\s+', ' ', texte).strip()
                
                phrases = re.split(r'(?<=[.!?]) +', texte)
                morceaux = []
                morceau_actuel = ""
                for phrase in phrases:
                    if len(morceau_actuel) + len(phrase) + 1 < 1000:
                        morceau_actuel += (phrase + " ").strip()
                    else:
                        morceaux.append(morceau_actuel)
                        morceau_actuel = phrase + " "
                if morceau_actuel:
                    morceaux.append(morceau_actuel)

                reinitialiser_fichier()

                with open("analysefichier.txt", "a", encoding="utf-8") as fichier_coffre:
                    for morceau in morceaux:
                        fichier_coffre.write(morceau.strip() + "\n")
                print("Contenu du PDF ajouté à 'analysefichier.txt'.")
        except Exception as e:
            print(f"Erreur lors de la conversion du PDF : {str(e)}")

def televerser_fichier_texte():
    chemin_fichier = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt")])
    if chemin_fichier:
        try:
            with open(chemin_fichier, 'r', encoding="utf-8") as fichier_texte:
                texte = fichier_texte.read()
                
                texte = re.sub(r'\s+', ' ', texte).strip()
                
                phrases = re.split(r'(?<=[.!?]) +', texte)
                morceaux = []
                morceau_actuel = ""
                for phrase in phrases:
                    if len(morceau_actuel) + len(phrase) + 1 < 1000:
                        morceau_actuel += (phrase + " ").strip()
                    else:
                        morceaux.append(morceau_actuel)
                        morceau_actuel = phrase + " "
                if morceau_actuel:
                    morceaux.append(morceau_actuel)

                reinitialiser_fichier()

                with open("analysefichier.txt", "a", encoding="utf-8") as fichier_coffre:
                    for morceau in morceaux:
                        fichier_coffre.write(morceau.strip() + "\n")
                print("Contenu du fichier texte ajouté à 'analysefichier.txt'.")
        except Exception as e:
            print(f"Erreur lors de l'ajout du fichier texte : {str(e)}")

def televerser_fichier_json():
    chemin_fichier = filedialog.askopenfilename(filetypes=[("Fichiers JSON", "*.json")])
    if chemin_fichier:
        try:
            with open(chemin_fichier, 'r', encoding="utf-8") as fichier_json:
                donnees = json.load(fichier_json)
                
                texte = json.dumps(donnees, ensure_ascii=False)
                
                texte = re.sub(r'\s+', ' ', texte).strip()
                
                phrases = re.split(r'(?<=[.!?]) +', texte)
                morceaux = []
                morceau_actuel = ""
                for phrase in phrases:
                    if len(morceau_actuel) + len(phrase) + 1 < 1000:
                        morceau_actuel += (phrase + " ").strip()
                    else:
                        morceaux.append(morceau_actuel)
                        morceau_actuel = phrase + " "
                if morceau_actuel:
                    morceaux.append(morceau_actuel)

                reinitialiser_fichier()

                with open("analysefichier.txt", "a", encoding="utf-8") as fichier_coffre:
                    for morceau in morceaux:
                        fichier_coffre.write(morceau.strip() + "\n")
                print("Contenu du fichier JSON ajouté à 'analysefichier.txt'.")
        except Exception as e:
            print(f"Erreur lors de l'ajout du fichier JSON : {str(e)}")

def telecharger_google_docs():
    lien = simpledialog.askstring("Google Docs", "Entrez le lien de partage Google Docs :")
    if lien:
        try:
            if "document/d/" in lien:
                fichier_id = lien.split("document/d/")[1].split("/")[0]
            else:
                print("Lien Google Docs invalide.")
                return
            
            url = f"https://docs.google.com/feeds/download/documents/export/Export?id={fichier_id}&exportFormat=txt"
            reponse = requests.get(url)
            if reponse.status_code != 200:
                print("Erreur lors du téléchargement : Vérifiez le lien Google Docs.")
                return
            
            texte = reponse.text.strip()
            with open("analysefichier.txt", "w", encoding="utf-8") as fichier:
                fichier.write(texte)
            
            print("Contenu de Google Docs ajouté à 'analysefichier.txt'.")
        except Exception as e:
            print(f"Erreur lors du téléchargement depuis Google Docs : {str(e)}")

def telecharger_google_sheets():
    lien = simpledialog.askstring("Google Sheets", "Entrez le lien de partage Google Sheets :")
    if lien:
        try:
            if "spreadsheets/d/" in lien:
                fichier_id = lien.split("spreadsheets/d/")[1].split("/")[0]
            else:
                print("Lien Google Sheets invalide.")
                return
            
            url = f"https://docs.google.com/spreadsheets/d/{fichier_id}/export?format=csv"
            reponse = requests.get(url)
            if reponse.status_code != 200:
                print("Erreur lors du téléchargement : Vérifiez le lien Google Sheets.")
                return
            
            contenu = reponse.text.strip()
            lignes = contenu.splitlines()
            texte = ""
            for ligne in csv.reader(lignes):
                texte += " ".join(ligne) + ". "

            with open("analysefichier.txt", "w", encoding="utf-8") as fichier:
                fichier.write(texte)
            
            print("Contenu de Google Sheets ajouté à 'analysefichier.txt'.")
        except Exception as e:
            print(f"Erreur lors du téléchargement depuis Google Sheets : {str(e)}")

def creer_interface():
    fenetre = tk.Tk()
    fenetre.title("IA de la galère (Nelson Almeida)")
    fenetre.geometry("500x400")
    fenetre.configure(bg="#f0f0f0")

    titre_label = tk.Label(
        fenetre,
        text="Gestion de fichiers",
        font=("Helvetica", 18, "bold"),
        bg="#f0f0f0",
        fg="#333333"
    )
    titre_label.pack(pady=20)

    cadre_boutons = tk.Frame(fenetre, bg="#ffffff", bd=2, relief="groove")
    cadre_boutons.pack(pady=20, padx=20, fill="both", expand=True)

    style_bouton = {
        "font": ("Helvetica", 12),
        "bg": "#4caf50",
        "fg": "white",
        "activebackground": "#45a049",
        "activeforeground": "white",
        "relief": "raised",
        "bd": 3,
        "width": 30
    }

    bouton_pdf = tk.Button(
        cadre_boutons,
        text="Téléverser un PDF local",
        command=lambda: convertir_pdf_en_texte(),
        **style_bouton
    )
    bouton_pdf.pack(pady=10)

    bouton_google_drive = tk.Button(
        cadre_boutons,
        text="Télécharger un fichier depuis Google Drive",
        command=telecharger_depuis_google_drive,
        **style_bouton
    )
    bouton_google_drive.pack(pady=10)

    bouton_texte = tk.Button(
        cadre_boutons,
        text="Téléverser un fichier texte",
        command=televerser_fichier_texte,
        **style_bouton
    )
    bouton_texte.pack(pady=10)

    bouton_json = tk.Button(
        cadre_boutons,
        text="Téléverser un fichier JSON",
        command=televerser_fichier_json,
        **style_bouton
    )
    bouton_json.pack(pady=10)

    bouton_docs = tk.Button(
        cadre_boutons,
        text="Télécharger un fichier Google Docs",
        command=telecharger_google_docs,
        **style_bouton
    )
    bouton_docs.pack(pady=10)

    bouton_sheets = tk.Button(
        cadre_boutons,
        text="Télécharger un fichier Google Sheets",
        command=telecharger_google_sheets,
        **style_bouton
    )
    bouton_sheets.pack(pady=10)

    footer_label = tk.Label(
        fenetre,
        text="Développé par Nelson Almeida",
        font=("Helvetica", 10),
        bg="#f0f0f0",
        fg="#666666"
    )
    footer_label.pack(side="bottom", pady=10)

    fenetre.mainloop()

creer_interface()
