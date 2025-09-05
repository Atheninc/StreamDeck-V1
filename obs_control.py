import serial, time, sys
from obswebsocket import obsws, requests  # v4 API

OBS_HOST = "localhost"
OBS_PORT = 4444           # v4 par défaut
OBS_PASS = "XXXX"
SERIAL_PORT = "COM8"      # remplace par ton port
BAUD = 115200

def main():
    # Connexion OBS
    ws = obsws(OBS_HOST, OBS_PORT, OBS_PASS)
    ws.connect()

    scenes_resp = ws.call(requests.GetSceneList())
    scene_names = [s['name'] for s in scenes_resp.getScenes()]
    print("Scènes OBS :", scene_names)

    # Map des 4 boutons -> 4 premières scènes (par ordre dans OBS)
    index_map = {"SC1":0, "SC2":1, "SC3":2, "SC4":3}

    # Série
    ser = serial.Serial(SERIAL_PORT, BAUD, timeout=1)
    print(f"Connecté à {SERIAL_PORT} / {BAUD}")

    try:
        while True:
            line = ser.readline().decode(errors="ignore").strip()
            if not line:
                continue
            print("Reçu:", line)
            if line in index_map:
                idx = index_map[line]
                if idx < len(scene_names):
                    ws.call(requests.SetCurrentScene(scene_names[idx]))  # v4
                    print("→ Scène:", scene_names[idx])
                else:
                    print("Avertissement: moins de 4 scènes disponibles.")
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()
        ws.disconnect()

if __name__ == "__main__":
    main()
