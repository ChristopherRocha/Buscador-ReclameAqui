from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from empresa import Empresa
import pandas as pd
import time


# Lista de empresas que posteriormente será usada para armazenar os objetos
listaEmpresas = []

# options para tentar ignorar os erros ssl
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--ignore-certificate-errors-spki-list")
options.add_argument("--ignore-ssl-errors")
options.add_argument('log-level=3')


# Inicializar o ChromeDriver
navegador = webdriver.Chrome(options=options)


# Método para escolher o segmento da análise
def escolherItem():

    # Achar o elemento contendo o texto de "Moda Infantil"
    itemModa = navegador.find_element(
        "xpath",  '//button[@title="Moda Infantil"]')

    # Trecho para remover o elemento que estava tampando o "Moda infantil"
    try:
        anuncio = navegador.find_element(
            "class name", "adopt-c-jOLxaA")
        navegador.execute_script(
            "arguments[0].remove();", anuncio)
        print("Anúncio fechado.")

    except:
        print("Nenhum anúncio encontrado.")

    itemModa.click()
    print("cliquei em moda infantil")
    time.sleep(3)


# Método para clicar no menu dropdown
def abrirMenu():
    # Achar o elemento do menu com base no texto dele
    menuDropdown = navegador.find_element(
        "xpath", '//input[@placeholder="Selecione ou busque uma categoria"]')
    menuDropdown.click()
    print("menu dropdown clicado!")
    time.sleep(2)
    escolherItem()

# Método usado para voltar a tela inicial do reclame aqui


def abrirTelaInicial():
    # Abre/Volta para a tela inicial do RA
    navegador.get("https://www.reclameaqui.com.br/")
    time.sleep(4)
    abrirMenu()


# Cria um objeto da classe empresa
def criarObjeto(_nome, _notaCons, _notaEmp, _recRespondidas, _volNegoc, _indSolucao):
    tmpEmpresa = Empresa(
        _nome,
        _notaCons,
        _notaEmp,
        _recRespondidas,
        _volNegoc,
        _indSolucao
    )

    return tmpEmpresa


# Utiliza do BeautiFulSoup para pegar todos os elementos strong da pagina
def rasparDados(html, nome, nota):

    conteudo = BeautifulSoup(html, "html.parser")
    palavras = conteudo.find_all("strong")

    # se nao tiver nenhum strong gera uma exception para parar o código
    if not palavras:
        print("nao achei nada")
        return Exception

    nomeEmpresa = nome
    notaEmpresa = nota
    recRespondidas = palavras[1].text
    notaConsumidor = palavras[4].text
    volNegocio = palavras[5].text
    indSolucao = palavras[6].text

    # Armazeno o objeto Empresa que foi criado
    listaEmpresas.append(criarObjeto(
        nomeEmpresa, notaConsumidor, notaEmpresa, recRespondidas, volNegocio, indSolucao))

    print("deu pra criar o objeto!")


# Escolhe a empresa a ser selecionada com base em um contador
def escolherEmpresas(piores: bool):
    cont = 0
    while cont < 3:
        try:

            # IF para poder definir quando rodar sobre as piores empresas
            if (piores):
                mudarOpcao = navegador.find_element(
                    "xpath", "//li[@data-testid='tab-worst']")
                mudarOpcao.click()
                time.sleep(2)

            # Reencontrar a lista de empresas do RA a cada iteração pois estava dando erro quando coloquei fora do loop
            tmpEmpresas = navegador.find_elements(
                "id", "home_ranking_segmento_card_empresa"
            )

            # Verificar se a lista de empresas do RA está vazia
            if not tmpEmpresas:
                print("Nenhuma empresa encontrada!")
                break

            # Pegar o elemento atual
            item = tmpEmpresas[cont]

            # Exibir o que foi escolhido
            conteudo = item.text.split("\n")
            print("quantidade de dados pushados: ", len(conteudo))

            # Trecho para ignorar os textos das imagens das empresas quando nao houver uma
            if (len(conteudo) == 4):
                nomeEmpresa = conteudo[2]
                notaEmpresa = conteudo[3]
            else:
                nomeEmpresa = conteudo[1]
                notaEmpresa = conteudo[2]

            # entrar na empresa
            try:
                item.click()
            except:
                print("Não foi possível clicar no link.")

            # tempo para fazer o captcha
            print("estou no captcha!!!")
            time.sleep(7)
            # tempo para web scrapping
            print("estou no webscrapping!!!")
            time.sleep(3)
            rasparDados(navegador.page_source, nomeEmpresa, notaEmpresa)

            # Incrementar contador para ir para a próxima empresa do RA
            cont += 1

            # Voltar a pagina inicial e repetir o processo
            print("estou voltando ao inicio!!!")
            abrirTelaInicial()

        except Exception as e:
            print(f"Erro na empresa: {cont} / erro: {e}")
            time.sleep(10)


# -----------------começo do código-----------------

# Deixar em FullScreen
navegador.maximize_window()
# Primeira chamada do método para abrir o site do RA
abrirTelaInicial()
# Escolher melhores 3 empresas
escolherEmpresas(False)
# Escolher as piores 3 empresas
escolherEmpresas(True)


print("----finalizei o processo de criação dos objetos----")


# Estrutura de dados para o panda

tabelaPandas = []

# Verificar o que foi criado e criar a planilha do pandas
for empresa in listaEmpresas:
    print("------xxx------")
    print(empresa)

    tabelaPandas.append(
        {
            "Nome": empresa.nome,
            "Nota no RA": empresa.notaEmpresa,
            "Nota dos consumidores": empresa.notaConsumidor,
            "Reclamações respondidas": empresa.recRespondidas,
            "Voltariam a fazer negócio": empresa.volNegocio,
            "Índice de solução": empresa.indSolucao
        }
    )


print("----saída da tabela do Pandas----")

# Conversão de lista de objetos para DataFrame
dfPandas = pd.DataFrame(tabelaPandas)
print(dfPandas)

# Saída do arquivo em forma de planilha do Excel
dfPandas.to_excel("consulta Empresas.xlsx", engine="openpyxl")

time.sleep(5)
