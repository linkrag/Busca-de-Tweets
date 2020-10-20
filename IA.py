from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB

## Estabelece quando a frase é positiva e quando ela é negativa
def exibir_resultado(valor):
    frase, resultado = valor
    resultado = "Frase positiva" if resultado[0] == '1' else "Frase negativa"
    print(frase, ":", resultado)

    ## Recebe uma frase para analisar
def analisar_frase(classificador, vetorizador, frase):
        return frase, classificador.predict(vetorizador.transform([frase]))

    ## Recebe uma análise pre pronta da análise de sentimentos
def obter_dados_das_fontes():

        diretorio_base = "C:\\Users\\Felipe Pinto\\source\\repos\\APS_51\\APS_51\\treino.txt"

        with open(diretorio_base , "r") as arquivo_texto:
            dados = arquivo_texto.read().split('\n')
         
        return dados

    ## Prepara os dados para o treinamento
def tratamento_dos_dados(dados):
        dados_tratados = []
        for dado in dados:
            if len(dado.split("\t")) == 2 and dado.split("\t")[1] != "":
                dados_tratados.append(dado.split("\t"))

        return dados_tratados

    ## Prepara os dados para o treinamento
def dividir_dados_para_treino_e_validacao(dados):
        quantidade_total = len(dados)
        percentual_para_treino = 0.75
        treino = []
        validacao = []

        for indice in range(0, quantidade_total):
            if indice < quantidade_total * percentual_para_treino:
                treino.append(dados[indice])
            else:
                validacao.append(dados[indice])

        return treino, validacao

    ## Prepara os dados para o treinamento
def pre_processamento():
        dados = obter_dados_das_fontes()
        dados_tratados = tratamento_dos_dados(dados)

        return dividir_dados_para_treino_e_validacao(dados_tratados)

    ## Realiza o treinamento utilizando os dados preparados
def realizar_treinamento(registros_de_treino, vetorizador):
        treino_comentarios = [registro_treino[0] for registro_treino in registros_de_treino]
        treino_respostas = [registro_treino[1] for registro_treino in registros_de_treino]

        treino_comentarios = vetorizador.fit_transform(treino_comentarios)

        return BernoulliNB().fit(treino_comentarios, treino_respostas)

    ## Avalia a frase recebida e retorna se ela é positiva ou negativa (sem tratamento de falsos)
def realizar_avaliacao_simples(registros_para_avaliacao):
        avaliacao_comentarios = [registro_avaliacao[0] for registro_avaliacao in registros_para_avaliacao]
        avaliacao_respostas = [registro_avaliacao[1] for registro_avaliacao in registros_para_avaliacao]

        total = len(avaliacao_comentarios)
        acertos = 0
        for indice in range(0, total):
            resultado_analise = analisar_frase(classificador, vetorizador, avaliacao_comentarios[indice])
            frase, resultado = resultado_analise
            acertos += 1 if resultado[0] == avaliacao_respostas[indice] else 0

        return acertos * 100 / total
    ## Avalia a frase recebida e retorna se ela é positiva ou negativa (com tratamento de falsos)
def realizar_avaliacao_completa(registros_para_avaliacao):
        avaliacao_comentarios = [registro_avaliacao[0] for registro_avaliacao in registros_para_avaliacao]
        avaliacao_respostas = [registro_avaliacao[1] for registro_avaliacao in registros_para_avaliacao]

        total = len(avaliacao_comentarios)
        verdadeiros_positivos = 0
        verdadeiros_negativos = 0
        falsos_positivos = 0
        falsos_negativos = 0

        for indice in range(0, total):
            resultado_analise = analisar_frase(classificador, vetorizador, avaliacao_comentarios[indice])
            frase, resultado = resultado_analise
            if resultado[0] == '0':
                verdadeiros_negativos += 1 if avaliacao_respostas[indice] == '0' else 0
                falsos_negativos += 1 if avaliacao_respostas[indice] != '0' else 0
            else:
                verdadeiros_positivos += 1 if avaliacao_respostas[indice] == '1' else 0
                falsos_positivos += 1 if avaliacao_respostas[indice] != '1' else 0

        return (verdadeiros_positivos * 100 / total, 
                 verdadeiros_negativos * 100 / total,
                 falsos_positivos * 100 / total,
                 falsos_negativos * 100 / total)    


 ## Classe para ser utilizada fora e analisar os tweets
class Naive:
    def principal(palavra):
       registros_de_treino, registros_para_avaliacao = pre_processamento()
       vetorizador = CountVectorizer(binary = 'true')
       classificador = realizar_treinamento(registros_de_treino, vetorizador)
       var=0
       if analisar_frase(classificador, vetorizador,palavra)[1] == '1':
               var = var + 1
        
       return var                    