import pickle

caminho_arquivo = "votos.pkl"

try:
    with open(caminho_arquivo, "rb") as f:
        votos = pickle.load(f)
        print("Conteudo do arquivo votos.pkl:")
        for voto in votos:
            print(voto)
except FileNotFoundError:
    print(f"Arquivo {caminho_arquivo} nao encontrado!")
except Exception as e:
    print(f"Erro ao carregar o arquivo: {e}")
