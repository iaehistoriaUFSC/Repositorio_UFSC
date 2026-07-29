"""Interface local, em português, para exploração dos modelos WOKE."""

from __future__ import annotations

import html
import json
import time
from pathlib import Path

import pandas as pd
import streamlit as st

import woke_analysis as analysis
from woke_catalog import CATALOG, DEFAULT_KEYS, package_by_key
from woke_models import MODEL_HOME, install_package, installed_size, is_installed, load_models


st.set_page_config(page_title="WOKE — IA & História", page_icon="◉", layout="wide")

st.markdown(
    """
<style>
:root { --ink:#172033; --muted:#64748b; --teal:#0f766e; --rose:#be185d; --paper:#f8fafc; }
.stApp { background: linear-gradient(145deg,#f8fafc 0%,#f0fdfa 50%,#fff1f2 100%); color:var(--ink); }
[data-testid="stHeader"] { background:transparent; }
.woke-hero { padding:2.2rem 2.5rem; border-radius:24px; color:white; margin-bottom:1.2rem;
 background:radial-gradient(circle at 85% 10%,rgba(255,255,255,.22),transparent 28%),linear-gradient(120deg,#0f766e,#134e4a 58%,#831843); box-shadow:0 18px 50px rgba(15,118,110,.18); }
.woke-hero h1 { font-size:3rem; margin:0; letter-spacing:.04em; }
.woke-hero p { max-width:760px; margin:.6rem 0 0; font-size:1.08rem; color:#ecfeff; }
.metric-card { background:rgba(255,255,255,.82); border:1px solid rgba(148,163,184,.24); border-radius:18px; padding:1rem 1.2rem; box-shadow:0 8px 25px rgba(15,23,42,.06); }
.small-note { color:var(--muted); font-size:.9rem; }
.about-card { background:white; border-left:5px solid #0f766e; padding:1.4rem 1.6rem; border-radius:8px 18px 18px 8px; box-shadow:0 8px 26px rgba(15,23,42,.06); }
div[data-testid="stTabs"] button { font-weight:650; }
.stButton>button { border-radius:10px; }
</style>
<section class="woke-hero">
  <h1>WOKE</h1>
  <p>Word embeddings para explorar conceitos, campos semânticos e mudanças históricas em teses e dissertações da Universidade Federal de Santa Catarina.</p>
</section>
""",
    unsafe_allow_html=True,
)


def human_size(value: int | None) -> str:
    if value is None:
        return "tamanho informado após o primeiro download"
    amount = float(value)
    for unit in ("B", "MB", "GB", "TB"):
        if amount < 1000 or unit == "TB":
            return f"{amount:.1f} {unit}" if unit != "B" else f"{int(amount)} B"
        amount /= 1000
    return f"{amount:.1f} TB"


@st.cache_resource(show_spinner="Carregando vetores do modelo…")
def cached_models(package_key: str):
    return load_models(package_by_key(package_key))


def installed_packages():
    return [package for package in CATALOG if is_installed(package)]


def render_model_manager() -> None:
    st.subheader("Biblioteca de modelos")
    st.write(
        "Os modelos ficam neste computador e são reutilizados sem internet. "
        "A série completa de História — Temporal e Incremental, Modelo 1, de 2003 a 2024 — é a seleção padrão."
    )
    st.code(str(MODEL_HOME), language=None)

    defaults_only = st.toggle("Mostrar inicialmente apenas os modelos padrão", value=True)
    visible = [package for package in CATALOG if package.key in DEFAULT_KEYS] if defaults_only else list(CATALOG)
    selected = st.multiselect(
        "Pacotes para baixar",
        options=[package.key for package in visible],
        default=[package.key for package in visible if package.key in DEFAULT_KEYS and not is_installed(package)],
        format_func=lambda key: package_by_key(key).label,
    )

    col_download, col_all = st.columns([2, 1])
    download_selected = col_download.button("Baixar os pacotes selecionados", type="primary", width="stretch")
    all_confirmed = col_all.checkbox("Confirmo: baixar todos os 28")
    download_all = col_all.button("Baixar todos os modelos", disabled=not all_confirmed, width="stretch")

    if download_selected or download_all:
        queue = list(CATALOG) if download_all else [package_by_key(key) for key in selected]
        if not queue:
            st.warning("Selecione ao menos um pacote.")
        else:
            progress = st.progress(0, text="Preparando downloads…")
            for index, package in enumerate(queue, start=1):
                with st.status(f"{package.label}", expanded=True) as status:
                    package_progress = st.progress(0, text="Conectando ao Google Drive…")

                    def update_package(downloaded: int, total: int | None) -> None:
                        if total:
                            fraction = min(downloaded / total, 1.0)
                            package_progress.progress(
                                fraction,
                                text=f"{human_size(downloaded)} de {human_size(total)}",
                            )
                        else:
                            package_progress.progress(0, text=f"{human_size(downloaded)} baixados")

                    try:
                        install_package(package, status.write, update_package)
                    except Exception as exc:
                        status.update(label=f"Falha em {package.label}", state="error")
                        st.error(f"{type(exc).__name__}: {exc}")
                        break
                    else:
                        package_progress.progress(1.0, text="Download e extração concluídos")
                        status.update(label=f"Instalado: {package.label}", state="complete")
                progress.progress(index / len(queue), text=f"{index} de {len(queue)} pacote(s)")
            cached_models.clear()
            st.success("Operação encerrada. Os modelos concluídos já estão disponíveis para análise.")

    rows = []
    for package in CATALOG:
        installed = is_installed(package)
        rows.append(
            {
                "Corpus": package.display_corpus,
                "Modo": package.mode,
                "Modelo": package.rank,
                "Recortes": package.intervals,
                "Períodos cobertos": ", ".join(package.periods),
                "Situação": "Instalado" if installed else "Disponível para download",
                "Tamanho": human_size(installed_size(package) if installed else package.known_download_bytes),
            }
        )
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch", height=430)
    st.caption(
        "Os pacotes oficiais são hospedados no Google Drive pelo projeto WOKE. "
        "Downloads interrompidos podem ser retomados. Baixar todos pode exigir dezenas de gigabytes."
    )


VISUALIZATIONS = (
    "Similaridades ao longo do tempo",
    "Vizinhos mais próximos",
    "Rede dinâmica do campo semântico",
    "Mapa de calor",
    "Estratos do tempo",
    "Vetores de palavras (PCA)",
    "Comparação entre palavras (analogia)",
    "Elemento que não combina",
    "Frequência de palavras",
    "Mudança semântica",
)


def show_result(figure=None, table: pd.DataFrame | None = None, name: str = "resultado") -> None:
    if figure is not None:
        st.plotly_chart(figure, width="stretch")
        st.download_button(
            "Baixar visualização em HTML",
            figure.to_html(include_plotlyjs="cdn").encode("utf-8"),
            file_name=f"woke_{name}.html",
            mime="text/html",
        )
    if table is not None:
        st.dataframe(table, hide_index=True, width="stretch")
        st.download_button(
            "Baixar dados em CSV",
            table.to_csv(index=False).encode("utf-8-sig"),
            file_name=f"woke_{name}.csv",
            mime="text/csv",
        )


def render_analysis() -> None:
    available = sorted(
        installed_packages(),
        key=lambda package: (package.key not in DEFAULT_KEYS, package.mode != "Incremental", package.label),
    )
    if not available:
        st.info("Baixe os modelos padrão na aba **Modelos** para começar.")
        return

    package_key = st.selectbox(
        "Série de modelos",
        [package.key for package in available],
        format_func=lambda key: package_by_key(key).label,
    )
    package = package_by_key(package_key)
    visualization = st.selectbox("Visualização", VISUALIZATIONS)
    st.caption(f"{package.intervals} recortes temporais · {package.mode} · processamento inteiramente local")

    with st.form("analysis_form"):
        central = comparisons = tokens = ""
        topn = 10
        period_index = package.intervals - 1
        a = b = c = ""
        if visualization in {"Similaridades ao longo do tempo", "Mapa de calor"}:
            central = st.text_input("Palavra central", placeholder="história")
            comparisons = st.text_area("Palavras para comparação", placeholder="memória, política, cultura")
        elif visualization in {"Vizinhos mais próximos", "Rede dinâmica do campo semântico", "Estratos do tempo"}:
            central = st.text_input("Palavra central", placeholder="democracia")
            topn = st.slider("Quantidade de vizinhos", 5, 30, 10)
        elif visualization == "Vetores de palavras (PCA)":
            tokens = st.text_area("Palavras — use vírgulas", placeholder="história, memória, política, cultura, sociedade")
            selected_period = st.select_slider("Recorte temporal", options=package.periods, value=package.periods[-1])
            period_index = package.periods.index(selected_period)
        elif visualization == "Comparação entre palavras (analogia)":
            col_a, col_b, col_c = st.columns(3)
            a = col_a.text_input("A", placeholder="homem")
            b = col_b.text_input("está para B", placeholder="mulher")
            c = col_c.text_input("como C está para…", placeholder="rei")
            topn = st.slider("Quantidade de respostas", 3, 20, 10)
        elif visualization == "Elemento que não combina":
            tokens = st.text_area("Palavras — ao menos três", placeholder="história, memória, arquivo, banana")
        elif visualization in {"Frequência de palavras", "Mudança semântica"}:
            tokens = st.text_area("Palavras — use vírgulas", placeholder="história, democracia, raça")
        submitted = st.form_submit_button("Gerar análise", type="primary", width="stretch")

    if not submitted:
        return
    try:
        models = cached_models(package_key)
        if visualization == "Similaridades ao longo do tempo":
            terms = analysis.parse_tokens(comparisons)
            analysis.require_tokens(models, [central, *terms])
            data = analysis.similarity_over_time(models, central, terms)
            show_result(analysis.similarity_figure(data, central), data, "similaridades")
        elif visualization == "Vizinhos mais próximos":
            analysis.require_tokens(models, [central])
            data = analysis.nearest_neighbors(models, central, topn)
            show_result(analysis.neighbors_figure(data), data, "vizinhos")
        elif visualization == "Rede dinâmica do campo semântico":
            analysis.require_tokens(models, [central])
            show_result(analysis.semantic_network_figure(models, central, topn), name="rede_semantica")
        elif visualization == "Mapa de calor":
            terms = analysis.parse_tokens(comparisons)
            analysis.require_tokens(models, [central, *terms])
            show_result(analysis.heatmap_figure(models, central, terms), name="mapa_calor")
        elif visualization == "Estratos do tempo":
            analysis.require_tokens(models, [central])
            show_result(analysis.time_strata_figure(models, central, topn), name="estratos")
        elif visualization == "Vetores de palavras (PCA)":
            model_name, model = models[period_index]
            parsed_tokens = analysis.parse_tokens(tokens)
            missing = [token for token in parsed_tokens if token not in model]
            if missing:
                raise ValueError(
                    f"Palavras ausentes em {analysis.period_label(model_name)}: {', '.join(missing)}"
                )
            show_result(analysis.word_vectors_figure(model_name, model, parsed_tokens), name="vetores")
        elif visualization == "Comparação entre palavras (analogia)":
            analysis.require_tokens(models, [a, b, c])
            data = analysis.analogy(models, a, b, c, topn)
            show_result(table=data, name="analogia")
        elif visualization == "Elemento que não combina":
            parsed_tokens = analysis.parse_tokens(tokens)
            if len(parsed_tokens) < 3:
                raise ValueError("Informe ao menos três palavras diferentes.")
            analysis.require_tokens(models, parsed_tokens)
            data = analysis.odd_one_out(models, parsed_tokens)
            show_result(table=data, name="elemento_destoante")
        elif visualization == "Frequência de palavras":
            data = analysis.frequency_over_time(models, analysis.parse_tokens(tokens))
            show_result(analysis.frequency_figure(data), data, "frequencia")
        elif visualization == "Mudança semântica":
            parsed_tokens = analysis.parse_tokens(tokens)
            analysis.require_tokens([models[0], models[-1]], parsed_tokens)
            data = analysis.semantic_shift(models, parsed_tokens, aligned=package.mode == "Incremental")
            show_result(analysis.semantic_shift_figure(data), data, "mudanca_semantica")
            if package.mode == "Temporal":
                st.caption("Para séries temporais treinadas separadamente, o WOKE usa a mudança de vizinhança (Jaccard); a comparação direta das coordenadas vetoriais não é interpretada.")
    except Exception as exc:
        st.error(f"Não foi possível gerar a análise: {exc}")


def render_about() -> None:
    st.subheader("Sobre o WOKE")
    st.markdown(
        """
<div class="about-card">
<h3>Equipe IA &amp; História (2023–2024)</h3>
<p><strong>Igor Caetano de Souza</strong> — Programador<br>
<strong>Franciele Dias</strong> — Curadora de Dados<br>
<strong>PI:</strong> Rodrigo Bonaldo<br>
<strong>Frontend:</strong> Rodrigo Bonaldo</p>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown("### Como o WOKE funciona")
    st.write(
        "O WOKE usa Word2Vec para transformar palavras encontradas em teses e dissertações do "
        "Repositório Institucional da UFSC em vetores numéricos. Palavras que aparecem em contextos "
        "parecidos tendem a ocupar regiões próximas nesse espaço. Como os modelos foram organizados "
        "em recortes temporais, o programa permite observar vizinhanças semânticas, similaridades, "
        "frequências e deslocamentos ao longo do tempo. Os gráficos são instrumentos exploratórios: "
        "eles mostram padrões do corpus e não definem, sozinhos, o significado histórico de um conceito."
    )
    st.markdown("### Proveniência")
    st.write(
        "Corpus acadêmico composto por textos de teses e dissertações disponibilizados pela UFSC. "
        "Os pacotes de modelos são os mesmos arquivos públicos catalogados no código original do projeto."
    )
    st.link_button("Repositório do projeto", "https://github.com/iaehistoriaUFSC/Repositorio_UFSC")


tab_analysis, tab_models, tab_about = st.tabs(["Explorar", "Modelos", "Sobre mim"])
with tab_analysis:
    render_analysis()
with tab_models:
    render_model_manager()
with tab_about:
    render_about()
