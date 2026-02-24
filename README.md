"# StreamDeck-V1

Un Stream Deck DIY à 4 boutons physiques pour contrôler **OBS Studio** via une liaison série Arduino → Python.

---

## Table des matières

- [Aperçu](#aperçu)
- [Matériel requis](#matériel-requis)
- [Installation](#installation)
  - [1. Firmware Arduino](#1-firmware-arduino)
  - [2. Dépendances Python](#2-dépendances-python)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Cas de figure](#cas-de-figure)
- [Détails techniques](#détails-techniques)
- [Suggestions d'amélioration](#suggestions-damélioration)

---

## Aperçu

StreamDeck-V1 relie 4 boutons physiques connectés à un **Arduino Pro Micro** à **OBS Studio** grâce au protocole WebSocket OBS (API v4). Chaque appui sur un bouton commute OBS vers la scène correspondante en temps quasi-réel.

```
[Bouton 1-4]  →  Arduino Pro Micro  →  USB/Série  →  obs_control.py  →  OBS WebSocket  →  Changement de scène
```

---

## Matériel requis

| Composant | Quantité | Notes |
|-----------|----------|-------|
| Arduino Pro Micro (5 V / 3,3 V) | 1 | Testé avec la variante 5 V |
| Boutons poussoirs momentanés | 4 | N.O. (normalement ouvert) |
| Câble USB Micro-B | 1 | Connexion PC |
| Fils de connexion / breadboard | — | Montage libre |

---

## Installation

### 1. Firmware Arduino

1. Installez l'**Arduino IDE** (≥ 1.8) depuis [arduino.cc](https://www.arduino.cc/en/software).
2. Dans l'IDE, ajoutez le board **SparkFun Pro Micro** si ce n'est pas déjà fait :  
   `Fichier → Préférences → URL de gestionnaire` :  
   `https://raw.githubusercontent.com/sparkfun/Arduino_Boards/main/IDE_Board_Manager/package_sparkfun_index.json`
3. Sélectionnez la carte : `Outils → Type de carte → SparkFun Pro Micro` (5 V, 16 MHz).
4. Branchez l'Arduino, sélectionnez le bon **Port** dans `Outils → Port`.
5. Ouvrez `arduino.ino` et cliquez sur **Téléverser**.

> **Câblage des boutons :** chaque bouton relie la broche numérique (2, 3, 4 ou 5) à la masse (GND). La résistance de tirage interne (`INPUT_PULLUP`) est activée par le code — aucune résistance externe nécessaire.

```
Pin 2 ── [Bouton 1] ── GND
Pin 3 ── [Bouton 2] ── GND
Pin 4 ── [Bouton 3] ── GND
Pin 5 ── [Bouton 4] ── GND
```

### 2. Dépendances Python

Python 3.7+ requis.

```bash
pip install pyserial obs-websocket-py
```

> Le paquet `obs-websocket-py` implémente l'**API WebSocket v4** d'OBS.  
> Si vous utilisez OBS 28+ avec le plugin WebSocket v5, consultez la section [Cas de figure](#cas-de-figure).

---

## Configuration

Éditez les constantes en tête de `obs_control.py` :

| Variable | Valeur par défaut | Description |
|----------|------------------|-------------|
| `OBS_HOST` | `"localhost"` | Adresse IP de la machine OBS |
| `OBS_PORT` | `4444` | Port WebSocket OBS (v4 = 4444) |
| `OBS_PASS` | `"XXXX"` | Mot de passe du WebSocket OBS |
| `SERIAL_PORT` | `"COM8"` | Port série de l'Arduino (`/dev/ttyACM0` sous Linux/macOS) |
| `BAUD` | `115200` | Débit en bauds (doit correspondre au firmware) |

**Activer le WebSocket dans OBS :**  
`Outils → Paramètres WebSocket` → activer, définir le port et le mot de passe.

---

## Utilisation

1. Branchez l'Arduino sur le PC.
2. Lancez OBS Studio et vérifiez que le plugin WebSocket est actif.
3. Exécutez le script Python :

```bash
python obs_control.py
```

4. La console affiche les scènes détectées :

```
Scènes OBS : ['Jeu', 'Caméra', 'Écran partagé', 'Pause']
Connecté à COM8 / 115200
```

5. Appuyez sur un bouton physique → OBS commute vers la scène correspondante :

```
Reçu: SC1
→ Scène: Jeu
```

6. Pour quitter proprement, appuyez sur **Ctrl+C** dans le terminal.

---

## Cas de figure

### ✅ Fonctionnement normal

- 4 scènes ou plus configurées dans OBS.
- Bouton 1 → 1re scène, Bouton 2 → 2e scène, etc.

### ⚠️ Moins de 4 scènes dans OBS

Si OBS contient moins de scènes que de boutons mappés, le script affiche :

```
Avertissement: moins de 4 scènes disponibles.
```

Le bouton correspondant est alors ignoré ; les autres fonctionnent normalement.

### ⚠️ Port série introuvable

```
serial.SerialException: could not open port COM8
```

**Solution :** Modifiez `SERIAL_PORT` dans `obs_control.py` avec le bon port.  
- Windows : `COM3`, `COM4`, etc. (visible dans le Gestionnaire de périphériques)  
- Linux : `/dev/ttyACM0` ou `/dev/ttyUSB0`  
- macOS : `/dev/cu.usbmodem*`

### ⚠️ Échec de connexion OBS WebSocket

```
ConnectionRefusedError
```

**Solutions :**
- Vérifiez qu'OBS est lancé et que le WebSocket est activé.
- Vérifiez `OBS_HOST`, `OBS_PORT` et `OBS_PASS`.

### ⚠️ OBS 28+ / WebSocket v5

OBS 28 intègre nativement le WebSocket **v5** (port 5005 par défaut). Le script actuel utilise l'API v4. Pour migrer :

1. Installez `obsws-python` : `pip install obsws-python`
2. Adaptez `obs_control.py` pour utiliser les appels v5 (ex. `SetCurrentProgramScene`).

### ⚠️ Bouton qui déclenche plusieurs fois

Si un bouton produit plusieurs changements de scène par appui, augmentez la valeur `DEBOUNCE` dans `arduino.ino` (valeur actuelle : 35 ms) :

```cpp
const unsigned long DEBOUNCE = 80;  // augmenter si nécessaire
```

---

## Détails techniques

### Firmware Arduino (`arduino.ino`)

| Paramètre | Valeur |
|-----------|--------|
| Broches utilisées | 2, 3, 4, 5 (INPUT_PULLUP) |
| Messages envoyés | `SC1`, `SC2`, `SC3`, `SC4` |
| Débit série | 115 200 baud |
| Anti-rebond (debounce) | 35 ms |
| Délai de démarrage | 1 200 ms |

**Logique de détection :**  
Le firmware lit l'état de chaque broche à chaque itération de `loop()`. Un appui est détecté quand la broche passe de `HIGH` à `LOW` (bouton enfoncé) **et** que le délai de debounce est écoulé depuis le dernier changement d'état. Le message correspondant est envoyé sur le port série uniquement sur le front descendant.

### Script Python (`obs_control.py`)

| Paramètre | Valeur |
|-----------|--------|
| Bibliothèque OBS | `obs-websocket-py` (API v4) |
| Bibliothèque série | `pyserial` |
| Timeout lecture série | 1 s |
| Décodage | UTF-8 (erreurs ignorées) |

**Flux d'exécution :**
1. Connexion au WebSocket OBS → récupération de la liste des scènes.
2. Ouverture du port série.
3. Boucle infinie : lecture d'une ligne série → correspondance dans `index_map` → appel `SetCurrentScene`.
4. À l'interruption (Ctrl+C) : fermeture propre du port série et déconnexion WebSocket.

---

## Suggestions d'amélioration

Consultez [SUGGESTIONS.md](SUGGESTIONS.md) pour la liste complète des pistes d'évolution du projet.
" 
