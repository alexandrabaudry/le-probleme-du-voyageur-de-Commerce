# Nom du fichier exécutable (avec l'extension .py)
EXECUTABLE = python50.py

# Commande pour exécuter le script Python
PYTHON = python3

# Règle par défaut
all: run

# Règle pour exécuter le programme
run: $(EXECUTABLE)
	$(PYTHON) $(EXECUTABLE)

# Règle pour nettoyer les fichiers générés
clean:
	rm -f *.pyc

.PHONY: all run clean
