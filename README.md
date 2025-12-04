# 🚪🔐 Sistema de Porta Automática com Reconhecimento Facial

Este projeto implementa um sistema completo de porta automática inteligente utilizando Python, C++ (Arduino) e Inteligência Artificial, com reconhecimento facial em tempo real para controle de acesso.

O sistema cadastra rostos em um banco de dados, reconhece usuários com DeepFace, e controla LEDs e Servo Motor via Arduino, abrindo automaticamente a porta para usuários autorizados.

## 🧠 Funcionalidades

✅ Cadastro automático de usuários por fotos  
✅ Criação de banco de dados por pastas  
✅ Reconhecimento facial com IA (DeepFace - SFace)  
✅ Detecção de rosto real com Haar Cascade  
✅ Verificação de luminosidade da imagem  
✅ Comunicação Serial com Arduino  
✅ Controle de LED Verde e LED Vermelho  
✅ Controle de Servo Motor para abertura da porta  
✅ Abertura automática por 10 segundos  
✅ Alerta de acesso negado por 1,5 segundos  
✅ Reset automático do sistema  
✅ Interface visual em tempo real com OpenCV  

## 🏗️ Arquitetura do Sistema

### 1. Módulo de Cadastro (Python)

- Captura imagens pela webcam  
- Cria automaticamente a pasta do usuário  
- Salva 100 fotos por pessoa  

Estrutura do banco:

### 2. Módulo de Reconhecimento Facial (Python + IA)

Responsável por:
- Capturar imagem em tempo real  
- Verificar luminosidade mínima  
- Detectar rosto real com Haar Cascade  
- Reconhecer rosto com DeepFace  
- Comparar com o banco de dados  
- Enviar comando para o Arduino  

### 3. Módulo de Controle de Hardware (C++ / Arduino)

Responsável por:
- Receber comandos seriais:
  - 'V' → Acesso permitido  
  - 'R' → Acesso negado  
  - 'P' → Reset do sistema  
- Acender LEDs  
- Controlar o servo motor  
- Abrir a porta por 10 segundos  
- Fechar automaticamente  
- Controlar tempo sem delay usando millis()  

## 🔁 Fluxo de Funcionamento

1. O usuário executa o sistema de cadastro  
2. Digita o nome da pessoa  
3. O sistema tira 100 fotos automaticamente  
4. As imagens são salvas no banco  
5. O sistema principal inicia:
   - Se o rosto existir:
     - LED Verde acende  
     - Servo abre a porta  
     - Porta fecha após 10 segundos  
   - Se o rosto não existir:
     - LED Vermelho acende por 1,5 segundos  
6. O sistema retorna ao modo de espera  

## 🛠️ Tecnologias Utilizadas

### Linguagens
- Python  3.10.0
- C++ (Arduino)  

### Bibliotecas Python
- opencv-python → Processamento de imagem  
- deepface → Reconhecimento facial com IA  
- pyserial → Comunicação com Arduino  
- os → Manipulação de diretórios  
- time → Controle de tempo  

### Bibliotecas Arduino
- Servo.h → Controle do servo motor  

## ⚙️ Requisitos do Sistema

- Python 3.8+  
- Webcam  
- Arduino Uno  
- Servo motor  
- LED Verde  
- LED Vermelho  
- Resistores  
- Jumpers  
- Protoboard  
- Arduino IDE  
