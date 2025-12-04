#include <Servo.h>

// Definição dos Pinos
const int ledVermelhoPin = 9;
const int ledVerdePin = 10;
const int servoPin = 11;

Servo minhaPorta;

const int POSICAO_FECHADA = 0;
const int POSICAO_ABERTA = 90;

// Variáveis para controle de tempo (millis)
unsigned long tempoAbertura = 0;
const long duracaoAberta = 10000; // Porta aberta por 10 segundos (10000 ms)
const long duracaoAlerta = 1500; // LED Vermelho aceso por 1.5 segundos

// Variável de estado para saber o que o Arduino está fazendo
enum Estado { FECHADA, ABRINDO, ALERTA };
Estado estadoAtual = FECHADA;

void setup() {
  pinMode(ledVermelhoPin, OUTPUT);
  pinMode(ledVerdePin, OUTPUT);
  Serial.begin(9600);
  minhaPorta.attach(servoPin);
  minhaPorta.write(POSICAO_FECHADA);
  Serial.println("Sistema de Porta Automática Pronto.");
  // Garante que os LEDs estejam apagados no início
  digitalWrite(ledVermelhoPin, LOW);
  digitalWrite(ledVerdePin, LOW);
}

void loop() {
  unsigned long tempoAtual = millis();

  // 1. Lógica de Comunicação Serial (Não-Bloqueante)
  if (Serial.available() > 0) {
    char comando = Serial.read();

    if (comando == 'V') {
      // Recebeu comando de Acesso Permitido
      if (estadoAtual == FECHADA) {
        digitalWrite(ledVerdePin, HIGH);
        digitalWrite(ledVermelhoPin, LOW);
        minhaPorta.write(POSICAO_ABERTA);
        tempoAbertura = tempoAtual; // Marca o tempo que a porta foi aberta
        estadoAtual = ABRINDO;
        Serial.println("Acesso Permitido: Porta ABRINDO.");
      }
    } else if (comando == 'R') {
      // Recebeu comando de Acesso Negado
      if (estadoAtual != ABRINDO) { // Não interrompe o ciclo de abertura
        digitalWrite(ledVerdePin, LOW);
        digitalWrite(ledVermelhoPin, HIGH);
        minhaPorta.write(POSICAO_FECHADA);
        tempoAbertura = tempoAtual; // Reutiliza a variável para o tempo de alerta
        estadoAtual = ALERTA;
        Serial.println("Acesso Negado: Alerta Vermelho.");
      }
    }
    // Comando 'P' para finalizar (enviado pelo Python ao sair)
    else if (comando == 'P') {
      digitalWrite(ledVerdePin, LOW);
      digitalWrite(ledVermelhoPin, LOW);
      minhaPorta.write(POSICAO_FECHADA);
      estadoAtual = FECHADA;
      Serial.println("Sistema Desligado/Resetado.");
    }
  }
  
  // 2. Lógica de Controle de Estado (Não-Bloqueante)
  
  // Se a porta estiver ABRINDO e o tempo expirou, feche
  if (estadoAtual == ABRINDO && tempoAtual - tempoAbertura >= duracaoAberta) {
    minhaPorta.write(POSICAO_FECHADA);
    digitalWrite(ledVerdePin, LOW);
    estadoAtual = FECHADA;
    Serial.println("Porta FECHADA automaticamente.");
  }
  
  // Se estiver em ALERTA (LED vermelho aceso) e o tempo expirou, apague
  if (estadoAtual == ALERTA && tempoAtual - tempoAbertura >= duracaoAlerta) {
    digitalWrite(ledVermelhoPin, LOW);
    estadoAtual = FECHADA;
    Serial.println("Alerta Encerrado.");
  }
}