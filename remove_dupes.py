#!/usr/bin/env python3
"""
Script pour supprimer les images dupliquées dans un dossier.
Utilise le hash perceptuel (pHash) pour identifier les images visuellement similaires.
"""

import sys
from pathlib import Path

import imagehash
from PIL import Image

# Seuil de différence: plus c'est bas, plus les images doivent être similaires
# 0 = identique, 5-10 = très similaire, >15 = probablement différent
HASH_THRESHOLD = 12


def get_perceptual_hash(filepath):
    """Calcule le hash perceptuel d'une image."""
    try:
        img = Image.open(filepath)
        return imagehash.phash(img)
    except Exception as e:
        print(f"  ⚠️ Erreur lecture {filepath.name}: {e}")
        return None


def find_and_remove_duplicates(folder, dry_run=True, threshold=HASH_THRESHOLD):
    """
    Trouve et supprime les images visuellement similaires.
    
    Args:
        folder: Chemin du dossier à analyser
        dry_run: Si True, affiche seulement ce qui serait supprimé sans supprimer
        threshold: Seuil de différence (0=identique, plus c'est haut, plus tolérant)
    """
    extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'}
    
    # Liste de tuples: (hash, filepath)
    hashes = []
    duplicates = []
    
    folder_path = Path(folder)
    
    # Parcourir tous les fichiers images
    files = sorted([f for f in folder_path.iterdir() 
                   if f.is_file() and f.suffix.lower() in extensions])
    
    print(f"Analyse de {len(files)} images dans {folder}...")
    print(f"Seuil de similarité: {threshold} (0=identique)\n")
    
    for filepath in files:
        img_hash = get_perceptual_hash(filepath)
        
        if img_hash is None:
            continue
        
        # Chercher si une image similaire existe déjà
        is_duplicate = False
        for existing_hash, existing_path in hashes:
            diff = img_hash - existing_hash  # Différence entre les hashes
            if diff <= threshold:
                duplicates.append((filepath, existing_path, diff))
                print(f"Doublon trouvé: {filepath.name}")
                print(f"  -> Similaire à: {existing_path.name} (diff={diff})")
                is_duplicate = True
                break
        
        if not is_duplicate:
            hashes.append((img_hash, filepath))
    
    print(f"\n{'='*50}")
    print(f"Total: {len(duplicates)} doublon(s) trouvé(s)")
    
    if duplicates:
        if dry_run:
            print("\n⚠️  Mode simulation (dry-run). Aucun fichier supprimé.")
            print("Pour supprimer réellement, relancez avec --delete")
        else:
            print("\nSuppression des doublons...")
            for dup, original, diff in duplicates:
                dup.unlink()
                print(f"  Supprimé: {dup.name}")
            print(f"\n✅ {len(duplicates)} fichier(s) supprimé(s)")
    
    return duplicates

if __name__ == "__main__":
    # Par défaut, utilise le dossier courant ou celui passé en argument
    folder = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else "."
    
    # --delete pour supprimer réellement
    dry_run = "--delete" not in sys.argv
    
    find_and_remove_duplicates(folder, dry_run)
