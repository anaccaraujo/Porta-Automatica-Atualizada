import cv2
import os

# Pergunta nome
nome = input("Digite o nome da pessoa: ").strip()

# Cria a pasta
pasta = os.path.join("pessoas_autorizadas", nome)
os.makedirs(pasta, exist_ok=True)

print(f"[INFO] Salvando fotos na pasta: {pasta}")

# Inicia a webcam
cam = cv2.VideoCapture(0)

contador = 0
TOTAL_FOTOS = 100

while contador < TOTAL_FOTOS:
    ret, frame = cam.read()
    if not ret:
        break

    cv2.imshow("Captura de Fotos", frame)

    # Salva a foto automaticamente
    caminho_foto = os.path.join(pasta, f"{contador}.jpg")
    cv2.imwrite(caminho_foto, frame)

    print(f"[INFO] Foto {contador + 1}/{TOTAL_FOTOS} salva.")

    contador += 1
    cv2.waitKey(200)  # espera 200ms entre fotos

print("[OK] Captura finalizada!")

cam.release()
cv2.destroyAllWindows()