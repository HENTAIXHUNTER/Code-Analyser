import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
import requests

chemin_fichier_charge = None

fenetre = tk.Tk()
fenetre.title("Assistant de Correction")
fenetre.geometry("800x600")

zone_texte = tk.Text(fenetre, wrap=tk.WORD, height=15)
zone_texte.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

zone_resultat = tk.Text(fenetre, wrap=tk.WORD, height=15, bg="#f0f0f0")
zone_resultat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

btn_frame = tk.Frame(fenetre)
btn_frame.pack(pady=10)

def charger_fichier():
    global chemin_fichier_charge
    chemin = filedialog.askopenfilename(filetypes=[
        ("Tous les fichiers", "*.*"),
        ("Fichiers texte", "*.txt"),
        ("Fichiers Python", "*.py"),
        ("Fichiers CSS", "*.css"),
        ("Fichiers JavaScript", "*.js"),
        ("Fichiers JSON", "*.json"),
        ("Fichiers HTML", "*.html")
    ])
    if chemin:
        chemin_fichier_charge = chemin
        with open(chemin, "r", encoding="utf-8") as f:
            contenu = f.read()
        zone_texte.delete("1.0", tk.END)
        zone_texte.insert(tk.END, contenu)
        zone_resultat.delete("1.0", tk.END)

def verifier_connexion_ollama():
    try:
        requests.get("http://localhost:11434", timeout=2)
        return True
    except:
        return False

def corriger_code_ollama(contenu):
    prompt = f"Corrige ce code Python et explique les erreurs :\n\n{contenu}"
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5-coder:7b",
                "prompt": prompt,
                "stream": False
            }
        )
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"❌ Erreur Ollama : {response.text}"
    except Exception as e:
        return f"❌ Erreur de connexion à Ollama : {e}"

def analyser_code_thread():
    contenu = zone_texte.get("1.0", tk.END)
    if not contenu.strip():
        messagebox.showwarning("Attention", "Aucun contenu à analyser.")
        return

    if not verifier_connexion_ollama():
        messagebox.showerror("Erreur", "Ollama n'est pas lancé.\nLance le modèle qwen2.5-coder:7b dans un terminal.")
        return

    zone_resultat.delete("1.0", tk.END)
    zone_resultat.insert(tk.END, "⏳ Analyse en cours...")

    def tache():
        correction = corriger_code_ollama(contenu)
        zone_resultat.delete("1.0", tk.END)
        zone_resultat.insert(tk.END, correction)

    threading.Thread(target=tache, daemon=True).start()

def sauvegarder_correction():
    contenu = zone_resultat.get("1.0", tk.END)
    if not contenu.strip():
        messagebox.showwarning("Attention", "Aucune correction à sauvegarder.")
        return

    extension_defaut = ".txt"
    nom_defaut = "correction"

    if chemin_fichier_charge:
        nom_fichier = os.path.basename(chemin_fichier_charge)
        nom_sans_ext, ext = os.path.splitext(nom_fichier)
        if ext in [".py", ".css", ".js", ".json", ".html", ".txt"]:
            extension_defaut = ext
        nom_defaut = f"{nom_sans_ext}_correction"

    path = filedialog.asksaveasfilename(
        defaultextension=extension_defaut,
        initialfile=nom_defaut + extension_defaut,
        filetypes=[
            ("Fichiers texte", "*.txt"),
            ("Fichiers Python", "*.py"),
            ("Fichiers CSS", "*.css"),
            ("Fichiers JavaScript", "*.js"),
            ("Fichiers JSON", "*.json"),
            ("Fichiers HTML", "*.html"),
            ("Tous les fichiers", "*.*")
        ]
    )

    if path:
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(contenu)
            messagebox.showinfo("Succès", f"Correction sauvegardée dans :\n{path}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder : {e}")

btn_charger = tk.Button(btn_frame, text="📂 Charger un fichier", command=charger_fichier)
btn_charger.pack(side=tk.LEFT, padx=5)

btn_analyser = tk.Button(btn_frame, text="🧠 Analyser le code", command=analyser_code_thread)
btn_analyser.pack(side=tk.LEFT, padx=5)

btn_sauvegarder = tk.Button(btn_frame, text="💾 Sauvegarder la correction", command=sauvegarder_correction)
btn_sauvegarder.pack(side=tk.LEFT, padx=5)

fenetre.mainloop()