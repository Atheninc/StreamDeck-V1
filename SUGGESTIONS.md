# Suggestions d'amélioration – StreamDeck-V1

Liste des pistes d'évolution identifiées pour le projet StreamDeck-V1.

---

## 1. Migration vers l'API OBS WebSocket v5

**Contexte :** OBS 28+ intègre nativement le WebSocket v5 (port 5005). Le script actuel utilise la bibliothèque `obs-websocket-py` (v4) qui n'est plus maintenue activement.  
**Amélioration :** Réécrire `obs_control.py` avec `obsws-python` (v5) pour assurer la compatibilité avec les versions récentes d'OBS et bénéficier des nouvelles fonctionnalités (événements, filtres, sources…).

---

## 2. Ajout de boutons et actions supplémentaires

**Contexte :** Le projet est limité à 4 boutons mappés à 4 scènes.  
**Amélioration :** Étendre le firmware et le script pour prendre en charge :
- Plus de 4 boutons (jusqu'aux 18 GPIO disponibles sur le Pro Micro).
- Des actions autres que le changement de scène : démarrer/arrêter l'enregistrement, couper le micro, activer une source, déclencher une transition, etc.
- Un mapping configurable via un fichier de configuration JSON ou YAML.

---

## 3. Fichier de configuration externe

**Contexte :** Les paramètres (`OBS_PASS`, `SERIAL_PORT`, `OBS_PORT`, etc.) sont codés en dur dans le script.  
**Amélioration :** Charger la configuration depuis un fichier `config.json` ou `.env` afin de ne pas exposer le mot de passe dans le code source et de faciliter le déploiement sur différentes machines.

---

## 4. Interface graphique (GUI) de configuration

**Contexte :** La configuration et le lancement se font en ligne de commande.  
**Amélioration :** Créer une petite interface graphique (Tkinter, PyQt ou web) permettant de :
- Sélectionner le port série dans une liste déroulante.
- Visualiser les scènes OBS et affecter chaque bouton à n'importe quelle scène.
- Démarrer/arrêter le service en un clic.

---

## 5. Détection automatique du port série

**Contexte :** L'utilisateur doit connaître et renseigner manuellement le port COM.  
**Amélioration :** Implémenter une détection automatique de l'Arduino Pro Micro par son VID/PID USB (`0x1B4F:0x9206` pour SparkFun) via `serial.tools.list_ports`, avec repli sur un port configurable.

---

## 6. Reconnexion automatique

**Contexte :** Si OBS est redémarré ou le câble USB débranché, le script plante.  
**Amélioration :** Ajouter une logique de reconnexion automatique (retry avec backoff exponentiel) pour le WebSocket OBS et le port série, afin de rendre l'outil plus robuste en conditions réelles.

---

## 7. Retour visuel sur les boutons (LEDs)

**Contexte :** L'utilisateur n'a aucun retour visuel indiquant quelle scène est active.  
**Amélioration :** Connecter des LEDs (ou un ruban NeoPixel) aux sorties du Pro Micro. Le script Python envoie en retour le numéro de scène active via le port série pour allumer la LED correspondante.

---

## 8. Support multiplateforme et packaging

**Contexte :** Le script fonctionne mais n'est pas empaqueté ; l'installation de dépendances est manuelle.  
**Amélioration :**
- Ajouter un `requirements.txt` pour simplifier l'installation (`pip install -r requirements.txt`).
- Créer un exécutable standalone avec PyInstaller pour Windows/macOS/Linux.
- Proposer un service systemd (Linux) ou une tâche planifiée (Windows) pour un lancement automatique au démarrage.

---

## 9. Tests automatisés

**Contexte :** Le projet ne comporte aucun test.  
**Amélioration :** Ajouter des tests unitaires Python (`pytest`) avec mock du port série et du WebSocket OBS pour valider le parsing des messages et la logique de mapping sans matériel physique.

---

## 10. Encodeurs rotatifs et afficheur OLED

**Contexte :** Les seuls contrôles sont des boutons poussoirs.  
**Amélioration :** Intégrer des encodeurs rotatifs pour le contrôle du volume ou du zoom caméra, et un petit écran OLED (I2C) affichant la scène active et l'état de l'enregistrement, comme sur un Stream Deck commercial.

---

*Ces suggestions peuvent servir de base à de futures issues GitHub et contributions.*
