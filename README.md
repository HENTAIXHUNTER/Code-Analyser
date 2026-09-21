Voici la description revue, sans emojis et avec un ton plus professionnel :

---

## Code Analyser — Assistant de Correction de Code

### Présentation

Application de bureau Windows développée en Python (Tkinter) permettant d'analyser et de corriger du code source via un modèle de langage exécuté localement avec Ollama (Qwen 2.5 Coder 7B). L'outil s'adresse aux développeurs souhaitant obtenir des suggestions de correction et des explications d'erreurs directement depuis leur poste, sans dépendance à un service cloud.

### Fonctionnalités

| Fonction | Description |
|---|---|
| **Chargement de fichier** | Sélection et ouverture d'un fichier source (`.py`, `.js`, `.css`, `.html`, `.json`, `.txt`) dans l'éditeur intégré |
| **Analyse du code** | Envoi du contenu au modèle Qwen 2.5 Coder 7B via Ollama, qui retourne le code corrigé accompagné d'explications sur les erreurs détectées |
| **Sauvegarde du résultat** | Export du résultat de l'analyse dans un fichier, avec nommage automatique (`*_correction.*`) conservant l'extension d'origine |

### Architecture

- [assistant_gui.py](assistant_gui.py) — Point d'entrée unique de l'application (~130 lignes). Interface Tkinter composée de deux zones de texte (code source / résultat d'analyse) et de trois boutons d'action.
- [assistant_gui.spec](assistant_gui.spec) — Fichier de configuration PyInstaller pour la compilation en exécutable Windows autonome (mode fenêtré, compression UPX).
- [dist/](dist/) — Répertoire contenant l'exécutable compilé.
- [build/](build/) — Artefacts de build PyInstaller (archives, analyse de dépendances, référence croisée des modules).

### Stack technique

| Composant | Technologie |
|---|---|
| Interface graphique | Python Tkinter |
| Modèle de langage | Ollama (local), Qwen 2.5 Coder 7B |
| Communication | API REST Ollama (`localhost:11434`) via la bibliothèque `requests` |
| Distribution | PyInstaller — exécutable Windows unique |

### Prérequis

L'utilisation de l'application nécessite qu'Ollama soit démarré localement avec le modèle `qwen2.5-coder:7b` préalablement téléchargé. L'analyse s'exécute dans un thread dédié afin de maintenir la réactivité de l'interface.
