from deepface import DeepFace
import cv2
import os
import serial
import time

# --- CONFIG SERIAL COM O ARDUINO IDE. ---
PORTA_SERIAL = 'COM4'
BAUD_RATE = 9600
arduino = None

try:
    arduino = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=1)
    print(f"[INFO] Conectado ao Arduino ({PORTA_SERIAL})")
    time.sleep(2)
except Exception as e:
    print(f"[ERRO] Falha ao conectar no Arduino: {e}")

# --- CONFIG DO SISTEMA PARA ENCONTRAR OS CAMINHOS PARA O BANCO DE DADOS. ---
DB_PATH = r"C:\Users\anacc\Trabalho_Final_IA"
THRESHOLD = 0.35
MODEL = "SFace"

# ---- DETECTOR DE ROSTO (Haar Cascade) NA CAMERA ----
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def existe_rosto(frame_gray):
    faces = face_cascade.detectMultiScale(frame_gray, 1.2, 5)
    return len(faces) > 0

# --- CAMERA ---
camera = cv2.VideoCapture(0)
camera.set(3, 640)
camera.set(4, 480)

frame_count = 0
INTERVALO = 10

ultimo_nome = "Aguardando..."
cor = (255, 255, 255)

acesso_concedido = False
tempo_ultimo_acesso = 0

def enviar_comando_led(comando):
    if arduino is not None:
        try:
            arduino.write(comando.encode())
        except:
            print("[ERRO SERIAL] Não foi possível enviar o comando.")

print("[INFO] Sistema iniciado. Pressione Q para sair.")

while True:
    ret, frame = camera.read()
    if not ret:
        continue

    frame_count += 1
    tempo_atual = cv2.getTickCount() / cv2.getTickFrequency()

    # Reset do ciclo 
    if acesso_concedido and tempo_atual - tempo_ultimo_acesso > 5:
        acesso_concedido = False
        ultimo_nome = "Porta Fechada. Aguardando..."
        cor = (255, 255, 255)

    # A CADA X FRAMES 
    if frame_count % INTERVALO == 0:

        # --- VERIFICA LUMINOSIDADE ---
        luminosidade = frame.mean()
        if luminosidade < 40:
            if not acesso_concedido:
                ultimo_nome = "Imagem escura"
                cor = (0, 0, 255)
                enviar_comando_led('R')
            cv2.putText(frame, ultimo_nome, (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, cor, 2)
            cv2.imshow("Porta Automática", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        # --- VERIFICA ROSTO REAL ---
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if not existe_rosto(gray):
            if not acesso_concedido:
                ultimo_nome = "Nenhum rosto detectado"
                cor = (0, 0, 255)
                enviar_comando_led('R')
            cv2.putText(frame, ultimo_nome, (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, cor, 2)
            cv2.imshow("Porta Automática", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        # --- RECONHECIMENTO ----
        small_frame = cv2.resize(frame, (320, 240))
        rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        try:
            resultado = DeepFace.find(
                img_path=rgb,
                db_path=DB_PATH,
                model_name=MODEL,
                enforce_detection=False,
                threshold=THRESHOLD
            )

            if len(resultado[0]) > 0:
                # Acesso permitido
                if not acesso_concedido:
                    caminho = resultado[0]["identity"][0]
                    nome = os.path.basename(os.path.dirname(caminho))

                    ultimo_nome = f"ACESSO PERMITIDO: {nome}"
                    cor = (0, 255, 0)

                    enviar_comando_led('V')
                    acesso_concedido = True
                    tempo_ultimo_acesso = tempo_atual
            else:
                # Acesso negado
                if not acesso_concedido:
                    ultimo_nome = "NEGADO!"
                    cor = (0, 0, 255)
                    enviar_comando_led('R')

        except:
            if not acesso_concedido:
                ultimo_nome = "Erro ao reconhecer"
                cor = (0, 0, 255)
                enviar_comando_led('R')

    # --- MOSTRAR TELA ---
    cv2.putText(frame, ultimo_nome, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, cor, 2)

    cv2.imshow("Porta Automática", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()

if arduino is not None:
    enviar_comando_led('P')
    arduino.close()

cv2.destroyAllWindows()
print("[INFO] Finalizado.")