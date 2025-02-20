Este projeto é um script de raspagem de dados desenvolvido em Python para extrair dados do site Reclame Aqui. Ele utiliza bibliotecas como Selenium e Beautiful Soup para coletar informações sobre reclamações respondidas, indíces de solução e notas das empresas
e exporta em forma de arquivo .xlsx para posterior modificação no Excel

Tecnologias Utilizadas

Python: Linguagem do projeto.

Selenium: Para navegação na web.

BeautifulSoup: Para extração e manipulação de dados HTML.

Pandas: Para análise e exportação dos dados extraídos.

Funcionalidades

Coleta de dados das 3 melhores e 3 piores empresas de algum ramo do reclame aqui.

Exportação dos dados para CSV ou Excel para análises futuras.

Bibliotecas necessárias para rodar o programa

BeautiFulSoup4, Pandas, Selenium e openpyxl

Observações!!

1- Por algum motivo o reclame aqui em horário comercial tem altas chances de gerar erros SSL
caso o código seja executado em horário com alto volume de usuários e não seja carregado em até 5 segundos 
é preciso parar o carregamento do site manualmente ou pode acabar gerando erros SSL, basta clicar no X onde fica o botão de atualizar a página, após a primeira raspagem não tem mais necessidades de parar o site.

2- O script não está passando de captchas, então antes da primeira rapsagem é preciso passar manualmente do captcha, nas outras tentativas não tem necessidade pois o captcha não reaparece.
