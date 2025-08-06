import webbrowser
from datetime import datetime
from fuzzywuzzy import fuzz
import json
import os
import sys
import subprocess
import wikipedia

wikipedia.set_lang("pt")
ARQUIVO_COMANDOS = "comandos_personalizados.json"
ARQUIVO_CONHECIMENTO = "memoria_conhecimento.json"

def carregar_comandos_personalizados():
    if os.path.exists(ARQUIVO_COMANDOS):
        with open(ARQUIVO_COMANDOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_comando_personalizado(comando, resposta):
    dados = carregar_comandos_personalizados()
    dados[comando] = resposta
    with open(ARQUIVO_COMANDOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def pesquisar_wikipedia(comando, falar, ouvir):
    termo = comando.replace("pesquisar sobre", "").strip()
    if not termo:
        falar("Sobre o que você quer saber?")
        termo = ouvir()
    try:
        resumo = wikipedia.summary(termo, sentences=2)
        falar(resumo)
    except wikipedia.exceptions.DisambiguationError:
        falar("Seja mais específico. Tem muitos resultados parecidos.")
    except wikipedia.exceptions.PageError:
        falar("Não encontrei nada sobre isso.")
    except Exception:
        falar("Ocorreu um erro ao buscar a informação.")

def consultar_conhecimento_por_tema(falar, ouvir):
    if not os.path.exists(ARQUIVO_CONHECIMENTO):
        falar("Ainda não tenho nenhum conhecimento armazenado.")
        return

    with open(ARQUIVO_CONHECIMENTO, "r", encoding="utf-8") as f:
        dados = json.load(f)

    if not dados:
        falar("Ainda não aprendi nada.")
        return

    falar("Sobre qual tema você quer saber?")
    tema_usuario = ouvir()

    melhor_tema = None
    maior_similaridade = 0

    for tema in dados:
        similaridade = fuzz.partial_ratio(tema_usuario.lower(), tema.lower())
        if similaridade > maior_similaridade:
            maior_similaridade = similaridade
            melhor_tema = tema

    if maior_similaridade >= 60:
        falar(f"Encontrei algo relacionado a {melhor_tema}.")
        paragrafos = dados[melhor_tema]
        for p in paragrafos[:3]:
            falar(p)
    else:
        falar("Não encontrei nenhum tema parecido.")

def executar_comando(comando, falar, ouvir, reativar_microfone=None):
    comandos_fixos = {
        "seu nome": lambda: falar("Meu nome é Theo!"),
        "que horas são": lambda: falar(f"Agora são {datetime.now().strftime('%H:%M')}"),
        "abrir navegador": lambda: (falar("Abrindo navegador."), webbrowser.open("https://www.google.com")),
        "sair": lambda: (falar("Até logo!"), sys.exit()),
        "como você está": lambda: falar("Estou ótimo, obrigado por perguntar!"),
        "abra o youtube": lambda: (falar("Abrindo YouTube."), webbrowser.open("https://www.youtube.com")),
        "abra o google": lambda: (falar("Abrindo Google."), webbrowser.open("https://www.google.com")),
        "qual é a data de hoje": lambda: falar(f"Hoje é {datetime.now().strftime('%d/%m/%Y')}"),
        "abra o spotify": lambda: (falar("Abrindo Spotify."), webbrowser.open("https://open.spotify.com")),
        "abra o bloco de notas": lambda: (falar("Abrindo bloco de notas."), subprocess.Popen("notepad")),
        "qual é a sua função": lambda: falar("Eu sou seu assistente pessoal, pronto para ajudar no que precisar."),
        "pesquisar sobre": lambda: pesquisar_wikipedia(comando, falar, ouvir),
        "consultar conhecimento": lambda: consultar_conhecimento_por_tema(falar, ouvir),
    }

    comandos_perso = carregar_comandos_personalizados()
    comandos_perso_funcoes = {
        k: (lambda r=resposta: lambda: falar(r))() for k, resposta in comandos_perso.items()
    }

    comandos_todos = {**comandos_fixos, **comandos_perso_funcoes}

    melhor_comando = None
    maior_similaridade = 0

    for chave in comandos_todos:
        similaridade = fuzz.partial_ratio(comando, chave)
        if similaridade > maior_similaridade:
            maior_similaridade = similaridade
            melhor_comando = chave

    if maior_similaridade >= 70:
        comandos_todos[melhor_comando]()
    else:
        falar("Não conheço esse comando. Deseja me ensinar? Diga sim ou não.")
        resposta = ouvir()

        if "sim" in resposta:
            falar("O que devo responder quando ouvir esse comando?")
            nova_resposta = ouvir()
            salvar_comando_personalizado(comando, nova_resposta)
            falar("Comando aprendido com sucesso!")
        else:
            falar("Tudo bem. Vamos continuar.")

        if reativar_microfone:
            reativar_microfone()
