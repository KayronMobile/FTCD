from pathlib import Path
import subprocess
import sys
import time

import pandas as pd
import streamlit as st


DATA_PATH = Path(__file__).parent / "data" / "noticias_eaj.csv"

st.set_page_config(page_title="Notícias UFRN sobre EAJ", layout="wide")
st.title("Notícias da UFRN que citam EAJ")
st.caption("Visualização dos resultados coletados pelo spider Scrapy.")

if st.button("Coletar dados", icon=":material/download:", type="primary"):
    started_at = time.perf_counter()
    with st.status("Coletando notícias da UFRN...", expanded=False) as status:
        result = subprocess.run(
            [sys.executable, "-m", "scrapy", "crawl", "ufrn_news", "-L", "INFO"],
            cwd=DATA_PATH.parent.parent,
            capture_output=True,
            text=True,
            check=False,
        )
        elapsed_seconds = time.perf_counter() - started_at
        st.session_state["last_collection_seconds"] = elapsed_seconds

        if result.returncode == 0:
            status.update(label="Dados coletados com sucesso.", state="complete")
            st.success(
                f"O CSV foi atualizado em {elapsed_seconds:.1f} segundos. "
                "Os dados abaixo já refletem a nova coleta."
            )
        else:
            status.update(label="A coleta falhou.", state="error")
            st.error(f"Não foi possível coletar os dados após {elapsed_seconds:.1f} segundos.")
            st.code(result.stderr[-4000:] or result.stdout[-4000:], language="text")

if "last_collection_seconds" in st.session_state:
    st.caption(f"Última coleta: {st.session_state['last_collection_seconds']:.1f} segundos")

if not DATA_PATH.exists():
    st.warning("Arquivo de dados ainda não encontrado. Execute o spider antes de abrir o dashboard.")
    st.code("scrapy crawl ufrn_news", language="bash")
    st.stop()

st.download_button(
    "Baixar CSV",
    data=DATA_PATH.read_bytes(),
    file_name="noticias_eaj.csv",
    mime="text/csv",
    icon=":material/download:",
)

try:
    news = pd.read_csv(DATA_PATH)
except pd.errors.EmptyDataError:
    st.info("O arquivo de dados está vazio. Execute o spider para coletar notícias.")
    st.code("scrapy crawl ufrn_news", language="bash")
    st.stop()

news["ano"] = pd.to_numeric(news["ano"], errors="coerce")
news = news.dropna(subset=["ano"]).copy()
news["ano"] = news["ano"].astype(int)
counts = news.groupby("ano").size().rename("noticias").sort_index()

metric_col, chart_col = st.columns([1, 3])
with metric_col:
    st.metric("Total de notícias", len(news))
    st.metric("Anos encontrados", news["ano"].nunique())
with chart_col:
    st.subheader("Quantidade de notícias por ano")
    st.bar_chart(counts)

st.subheader("Notícias coletadas")
st.dataframe(news.sort_values(["ano", "titulo"], ascending=[False, True]), width="stretch")
