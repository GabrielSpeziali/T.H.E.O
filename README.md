# T.H.E.O 🤖

Assistente pessoal inteligente inspirado no conceito do J.A.R.V.I.S., focado em automação, interação por voz e integração entre dispositivos.

---

## 🚀 Funcionalidades

* Reconhecimento de voz
* Resposta por voz
* Execução de comandos
* Leitura e organização de textos *(em desenvolvimento)*
* Integração entre dispositivos *(em desenvolvimento)*

---

## 🛠️ Tecnologias

* Python
* speech_recognition
* pyttsx3
* JSON

---

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/GabrielSpeziali/T.H.E.O
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Execute o projeto

```bash
python main.py
```

---

## 🎤 Como usar

* Execute o programa
* Fale um comando no microfone
* O Theo irá reconhecer e responder

---

## 📁 Estrutura atual do projeto

```bash
T.H.E.O/
├── main.py        # Arquivo principal
├── comandos.py    # Lógica dos comandos
├── falar.py       # Sistema de resposta por voz
├── ouvir.py       # Reconhecimento de voz
```

---

## 🧠 Arquitetura do sistema (visão futura)

```
Usuário (voz/texto)
        ↓
[ Entrada ]
        ↓
[ Processamento ]
        ↓
[ Núcleo do Theo ]
        ↓
[ Ações / Módulos ]
        ↓
[ Saída (voz/interface) ]
```

---

## 🧩 Organização planejada

### 🔹 Entrada (Input)

Responsável por capturar dados do usuário

```
input/
├── voz.py
├── texto.py
├── camera.py (futuro)
```

### 🔹 Processamento (Interpretação)

```
processamento/
├── interpretar.py
├── classificador.py
├── contexto.py
```

### 🔹 Núcleo (Core)

```
core/
├── motor.py
├── gerenciador.py
├── memoria.py
```

### 🔹 Módulos (Skills)

```
modulos/
├── sistema/
├── web/
├── conhecimento/
```

### 🔹 Saída (Output)

```
output/
├── voz.py
├── tela.py
```

### 🔹 Servidor Theo (futuro)

```
server/
├── api.py
├── auth.py
├── sync.py
```

### 🔹 Cliente (dispositivos)

```
cliente/
├── client.py
```

---

## 🔄 Exemplo de fluxo

```
Usuário: "Theo, abre o navegador"

ouvir.py → texto  
↓  
comandos.py → identifica ação  
↓  
execução do comando  
↓  
falar.py → resposta ao usuário
```

---

## 🔮 Futuro do projeto

* Interface gráfica com rosto animado
* Reconhecimento facial
* Sistema multi-dispositivos
* Servidor central do Theo
* Integração com IoT

---

## 🤝 Contribuição

Sinta-se livre para contribuir com melhorias!

---

## 📄 Licença

MIT
