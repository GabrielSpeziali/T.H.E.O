import nltk
import json

nltk.download('punkt_tab')

from nltk.tokenize import sent_tokenize

def limpar_sentenca(s):
    s = s.strip()
    if len(s) < 30 or 'http' in s or '@' in s:
        return False
    if s[0].isdigit():
        return False
    return True

def extrair_conhecimento_do_livro(caminho_arquivo_txt):
    with open(caminho_arquivo_txt, 'r', encoding='utf-8') as f:
        texto = f.read()
    texto = texto.replace('\n', ' ')
    sentencas = sent_tokenize(texto)  
    sentencas_filtradas = [
        s for s in sentencas if 30 < len(s) < 200 and limpar_sentenca(s)
    ]
    conhecimento = {"sentencas": sentencas_filtradas}
    return conhecimento

def salvar_conhecimento_json(conhecimento, caminho_arquivo_json):
    with open(caminho_arquivo_json, 'w', encoding='utf-8') as f:
        json.dump(conhecimento, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    conhecimento = extrair_conhecimento_do_livro('livros_txt/Logica_prog.txt')
    salvar_conhecimento_json(conhecimento, 'memoria_conhecimento.json')
