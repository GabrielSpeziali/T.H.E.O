import speech_recognition as sr
from comandos import executar_comando
from organizador import organizar_conhecimento
import threading
import os
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from fuzzywuzzy import fuzz
import asyncio
import edge_tts
import playsound
import uuid

nltk.download('punkt_tab')
nltk.download('stopwords')

PASTA_LIVROS = "livros_txt"
ARQUIVO_CONHECIMENTO = "memoria_conhecimento.json"

lock = threading.Lock()

async def falar_async(texto):
    with lock:
        nome_arquivo = f"fala_{uuid.uuid4().hex}.mp3"
        communicate = edge_tts.Communicate(texto, voice="pt-BR-AntonioNeural", rate="+20%")
        await communicate.save(nome_arquivo)
        playsound.playsound(nome_arquivo)
        os.remove(nome_arquivo)

def falar(texto):
    asyncio.run(falar_async(texto))

def ouvir():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ouvindo...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    try:
        comando = recognizer.recognize_google(audio, language="pt-BR")
        print(f"Reconhecido: {comando}")
        return comando.lower()
    except sr.UnknownValueError:
        return "não entendi"
    except sr.RequestError:
        return "erro ao se conectar"

def extrair_palavras_chave(texto, n=5):
    palavras = word_tokenize(texto.lower())  
    stop_words = set(stopwords.words('portuguese'))
    palavras_filtradas = [p for p in palavras if p.isalpha() and p not in stop_words]
    frequencia = Counter(palavras_filtradas)
    return [palavra for palavra, freq in frequencia.most_common(n)]

def carregar_conhecimento():
    if os.path.exists(ARQUIVO_CONHECIMENTO):
        with open(ARQUIVO_CONHECIMENTO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_conhecimento(dados):
    with open(ARQUIVO_CONHECIMENTO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def adicionar_conhecimento_por_tema(conhecimento, tema, texto):
    if tema in conhecimento:
        conhecimento[tema].append(texto)
    else:
        conhecimento[tema] = [texto]

def escolher_tema_automatico(texto):
    palavras_chave = extrair_palavras_chave(texto)
    return ", ".join(palavras_chave)

def ler_e_organizar_todos_livros():
    conhecimento = carregar_conhecimento()
    if not os.path.exists(PASTA_LIVROS):
        falar(f"A pasta {PASTA_LIVROS} não existe.")
        return
    arquivos = [f for f in os.listdir(PASTA_LIVROS) if f.endswith(".txt")]
    if not arquivos:
        falar("Não encontrei nenhum livro na pasta.")
        return
    
    for arquivo in arquivos:
        caminho = os.path.join(PASTA_LIVROS, arquivo)
        with open(caminho, "r", encoding="utf-8") as f:
            texto = f.read()
        tema = escolher_tema_automatico(texto)
        adicionar_conhecimento_por_tema(conhecimento, tema, texto)
    
    salvar_conhecimento(conhecimento)

falar("Olá! Como posso ajudar?")

modo_texto = input("Modo texto? (s/n): ").strip().lower() == "s"

while True:
    comando = input("Digite seu comando: ").lower() if modo_texto else ouvir()

    if fuzz.partial_ratio(comando, "ler livro") >= 70 or fuzz.partial_ratio(comando, "ler livros") >= 70:
        try:
            ler_e_organizar_todos_livros()
            falar("Terminei de ler todos os livros e organizar o conhecimento por temas.")
            organizar_conhecimento()
            falar("Conhecimento organizado com subtópicos.")
        except Exception as e:
            falar("Deu um problema ao ler os livros.")
            print(f"Erro: {e}")
    else:
        executar_comando(comando, falar, ouvir)
