import tweepy as tw
import sys
from datetime import datetime, timedelta 
import unicodedata
import re
from IA import Naive 
import matplotlib.pyplot as plt
import numpy as np
import Auth_key


## Classe responsável pelos gráficos
def grafico(cPos,cNeg,aPos,aNeg,bPos,bNeg,dPos,dNeg,ePos,eNeg,d1,d2,d3,d4,d5):
        d1=d1.strftime('%d/%m')
        d2=d2.strftime('%d/%m')
        d3=d3.strftime('%d/%m')
        d4=d4.strftime('%d/%m')
        d5=d5.strftime('%d/%m')
        labels = [d5,d4,d3,d2,d1]
        neg = [eNeg,dNeg,cNeg,bNeg,aNeg]
        posi = [ePos,dPos,cPos,bPos,aPos]
        
        ## Posição e largura das colunas
        x = np.arange(len(labels))
        width = 0.35  

        ## Passa os atributos da barra de tweets negativos e positivos
        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, neg, width, label='Tweets Negativos')
        rects2 = ax.bar(x + width/2, posi, width, label='Tweets Positivos')

        ## Gera um gráfico para cada label
        ax.set_title('Dados dos últimos 5 dias')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()


        def autolabel(rects):
            ## Quantidade de tweets de cada coluna
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')


        autolabel(rects1)
        autolabel(rects2)

        fig.tight_layout()

        plt.show()

        ## Inicializa a classe de manipulação e raspagem de tweets
class TwitterClient():

    
    ## Passa as chaves de autenticação para integrar com a API do Twitter
    def stream_tweets(stream):
         auth = tw.OAuthHandler(Auth_key.API_Key, Auth_key.APi_Secret)
         auth.set_access_token(Auth_key.Acess_Token, Auth_key.Acess_Token_Secret)
         twitter = tw.API(auth)
         api = tw.API(auth)

         ## Recebe a palavra a ser filtrada, remove retweets.
         search_words =stream + "-filter:retweets"
         ## Inicializa os contadores de cada barra do gráfico
         cPos=0
         cNeg=0
         aPos=0
         aNeg=0
         bPos=0
         bNeg=0
         dPos=0
         dNeg=0
         ePos=0
         eNeg=0

         ## As variáveis recebem o dia de hoje menos o dia para cada pesquisa
         d1 = datetime.today() - timedelta(days=5)
         d2 = datetime.today() - timedelta(days=4)
         d3 = datetime.today() - timedelta(days=3)
         d4 = datetime.today() - timedelta(days=2)
         d5 = datetime.today()

        ## O cursor que faz a raspagem dos tweets recebe os dados para fazer as buscas
         tweets = tw.Cursor(api.search, q=search_words, since =d1.date(), until = d5.date()).items(1000)



         ## Inicializo a variável da IA
         t= Naive

         ## Manipulação dos tweets recebidos pelo cursor
         for tweet in tweets:

                ## Printa a data no console para fazer validação
               print (tweet.created_at)

               ## Remove caracteres especiais
               nfkd = unicodedata.normalize('NFKD', tweet.text)
               acento = u"".join([c for c in nfkd if not unicodedata.combining(c)])
               limpar =re.sub('[^a-zA-Z0-9 \\\]', '', acento) 
           
               ## Recebe o tweet de acordo com a data criada
               if  d5.date() ==  tweet.created_at.date():
                   ## Passa o tweet pela IA e verifica e armazena na coluna positiva ou negativa
                      if t.principal(limpar) == 1:
                          ePos = ePos + 1
                      else: eNeg = eNeg + 1

               elif d4.date() ==  tweet.created_at.date():
                    if t.principal(limpar) == 1:
                          dPos = dPos + 1
                    else: dNeg =dNeg + 1

               elif d3.date() ==  tweet.created_at.date():

                    if t.principal(limpar) == 1:
                          cPos = cPos + 1
                    else: cNeg =cNeg + 1

               elif d2.date() ==  tweet.created_at.date():

                    if t.principal(limpar) == 1:
                          bPos = bPos + 1
                    else: bNeg =bNeg + 1

               elif d1.date() ==  tweet.created_at.date():
                    if t.principal(limpar) == 1:
                          aPos = aPos + 1
                    else: aNeg =aNeg + 1

                    ## A classe do gráfico recebe os dados das variáveis e monta o gráfico.
         grafico(cPos,cNeg,aPos,aNeg,bPos,bNeg,dPos,dNeg,ePos,eNeg,d1,d2,d3,d4,d5)