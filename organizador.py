import os
import json
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import Counter

nltk.download('punkt')
nltk.download('stopwords')

PASTA_LIVROS = "livros_txt"
ARQUIVO_CONHECIMENTO = "memoria_conhecimento.json"

IGNORAR_PALAVRAS = {"ah", "então", "pois", "agora", "certo", "forma", "tipo", "bem", "aí", "assim", "já", "hoje", "br", "vai"}

def limpar_texto(texto):
    texto = texto.replace('\n', ' ').replace('\t', ' ')
    while '  ' in texto:
        texto = texto.replace('  ', ' ')
    return texto.strip()

def extrair_temas_principais(texto):
    palavras = word_tokenize(texto.lower(), language='portuguese')
    palavras_filtradas = [p for p in palavras if p.isalpha() and p not in stopwords.words('portuguese') and p not in IGNORAR_PALAVRAS]
    
    contagem = Counter(palavras_filtradas)
    temas = [palavra for palavra, _ in contagem.most_common(5)]
    return temas

def organizar_frases_por_tema(texto, temas):
    frases = [f.strip() for f in sent_tokenize(texto, language='portuguese') if 30 < len(f.strip()) < 200]
    
    conhecimento = {}
    for tema in temas:
        conhecimento[tema] = []
        for frase in frases:
            if tema in frase.lower():
                conhecimento[tema].append(frase)
                if len(conhecimento[tema]) >= 5:
                    break
    
    return conhecimento

def processar_livro(texto):
    texto_limpo = limpar_texto(texto)
    temas = extrair_temas_principais(texto_limpo)
    conhecimento = organizar_frases_por_tema(texto_limpo, temas)
    return conhecimento

def organizar_conhecimento():
    conhecimento = {"temas": {}}

    if not os.path.exists(PASTA_LIVROS):
        print(f"A pasta {PASTA_LIVROS} não existe.")
        return

    arquivos = [f for f in os.listdir(PASTA_LIVROS) if f.endswith('.txt')]
    if not arquivos:
        print("Não há livros para organizar.")
        return

    for arquivo in arquivos:
        try:
            with open(os.path.join(PASTA_LIVROS, arquivo), 'r', encoding='utf-8') as f:
                texto = f.read()
                livro_processado = processar_livro(texto)
                
                for tema, frases in livro_processado.items():
                    if tema not in conhecimento["temas"]:
                        conhecimento["temas"][tema] = []
                    conhecimento["temas"][tema].extend(frases)
                    
        except Exception as e:
            print(f"Erro ao processar {arquivo}: {str(e)}")
            continue

    with open(ARQUIVO_CONHECIMENTO, 'w', encoding='utf-8') as f:
        json.dump(conhecimento, f, indent=2, ensure_ascii=False)

    print("Conhecimento organizado com sucesso.")

if __name__ == '__main__':
    organizar_conhecimento()