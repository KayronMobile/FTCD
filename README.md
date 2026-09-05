# Notícias UFRN sobre EAJ

Projeto acadêmico de ingestão de dados por web scraping. O objetivo é coletar as notícias da UFRN encontradas pela busca com a palavra-chave `EAJ`, salvar o ano e a URL de cada notícia e visualizar a quantidade de publicações por ano.

## Solução escolhida

O scraping é feito exclusivamente com **Scrapy**, por ser uma ferramenta adequada para organizar requisições, controlar paginação e exportar dados. O dashboard é feito com **Streamlit**.

O projeto foi configurado para reduzir o impacto sobre o site:

- `ROBOTSTXT_OBEY = True`
- uma requisição concorrente por vez
- atraso de 2 segundos entre requisições
- AutoThrottle ativado
- limite de atraso de até 10 segundos
- novas tentativas limitadas a 2
- resultados salvos em CSV para evitar novas coletas ao abrir o dashboard

## Estrutura

```text
projeto-eaj/
├── app.py
├── scrapy.cfg
├── requirements.txt
├── README.md
├── data/
├── eaj_scraper/
│   ├── items.py
│   ├── settings.py
│   └── spiders/
│       └── ufrn_news.py
└── tests/
    └── test_spider.py
```

## Instalação

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Executar a coleta

A partir da raiz do projeto:

```powershell
scrapy crawl ufrn_news
```

O arquivo `data/noticias_eaj.csv` será gerado com as colunas `titulo`, `ano` e `url`.

Antes da primeira coleta, confira a política do site e mantenha o atraso configurado. Não execute o spider repetidamente sem necessidade.

## Abrir o dashboard

Depois de gerar o CSV:

```powershell
streamlit run app.py
```

O dashboard apresenta o total de notícias, uma tabela com os resultados e um gráfico de barras com a quantidade de notícias por ano.

## Testes

```powershell
pytest -q
```

Os testes não fazem requisições reais à UFRN.
