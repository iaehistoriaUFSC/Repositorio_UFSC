"""Operações analíticas do WOKE adaptadas da interface de terminal original."""

from __future__ import annotations

import re
import unicodedata
from collections import Counter

import networkx as nx
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from gensim.models import KeyedVectors
from sklearn.decomposition import PCA


ModelSeries = list[tuple[str, KeyedVectors]]


def normalize_token(token: str) -> str:
    """Normaliza a consulta sem apagar distinções lexicais do vocabulário.

    Os modelos WOKE preservam diacríticos: ``história`` (português) e
    ``historia`` (espanhol) são tokens diferentes. A antiga decomposição NFKD
    removia os acentos e podia consultar silenciosamente o vetor errado.
    """
    token = unicodedata.normalize("NFC", token.strip().lower())
    return re.sub(r"\s+", "_", token)


def parse_tokens(text: str) -> list[str]:
    return list(dict.fromkeys(normalize_token(item) for item in re.split(r"[,;\n]+", text) if item.strip()))


def period_label(name: str) -> str:
    years = re.findall(r"(?:19|20)\d{2}", name)
    return "–".join(years[-2:]) if len(years) >= 2 else name


def missing_tokens(models: ModelSeries, tokens: list[str], every_period: bool = True) -> list[str]:
    tokens = list(dict.fromkeys(normalize_token(token) for token in tokens))
    if every_period:
        return [token for token in tokens if any(token not in model for _, model in models)]
    return [token for token in tokens if all(token not in model for _, model in models)]


def missing_tokens_by_period(models: ModelSeries, tokens: list[str]) -> dict[str, list[str]]:
    """Retorna os tokens ausentes agrupados pelo período do modelo."""
    normalized = list(dict.fromkeys(normalize_token(token) for token in tokens))
    return {
        period_label(name): [token for token in normalized if token not in model]
        for name, model in models
        if any(token not in model for token in normalized)
    }


def require_tokens(models: ModelSeries, tokens: list[str]) -> None:
    """Produz um erro legível antes de operações vetoriais multiperíodo."""
    missing = missing_tokens_by_period(models, tokens)
    if not missing:
        return
    details = "; ".join(
        f"{period}: {', '.join(period_tokens)}"
        for period, period_tokens in missing.items()
    )
    raise ValueError(f"Palavras ausentes no vocabulário — {details}")


def similarity_over_time(models: ModelSeries, central: str, compared: list[str]) -> pd.DataFrame:
    central = normalize_token(central)
    compared = [normalize_token(token) for token in compared]
    rows = []
    for name, model in models:
        for token in compared:
            rows.append({
                "Período": period_label(name),
                "Palavra": token,
                "Similaridade": float(model.similarity(central, token)),
            })
    return pd.DataFrame(rows)


def similarity_figure(data: pd.DataFrame, central: str) -> go.Figure:
    fig = px.line(
        data,
        x="Período",
        y="Similaridade",
        color="Palavra",
        markers=True,
        title=f'Similaridade com “{normalize_token(central)}” ao longo do tempo',
        template="plotly_white",
    )
    fig.update_yaxes(range=[-1, 1], zeroline=True)
    return fig


def nearest_neighbors(models: ModelSeries, token: str, topn: int = 10) -> pd.DataFrame:
    token = normalize_token(token)
    rows = []
    for name, model in models:
        for neighbor, score in model.most_similar(token, topn=topn):
            rows.append({"Período": period_label(name), "Vizinho": neighbor, "Similaridade": float(score)})
    return pd.DataFrame(rows)


def neighbors_figure(data: pd.DataFrame) -> go.Figure:
    periods = list(dict.fromkeys(data["Período"]))
    selected = periods[-1]
    frame = data[data["Período"] == selected].sort_values("Similaridade")
    fig = px.bar(
        frame,
        x="Similaridade",
        y="Vizinho",
        orientation="h",
        title=f"Vizinhos mais próximos — {selected}",
        template="plotly_white",
        color="Similaridade",
        color_continuous_scale="Tealgrn",
    )
    fig.update_layout(coloraxis_showscale=False)
    return fig


def heatmap_figure(models: ModelSeries, central: str, compared: list[str]) -> go.Figure:
    data = similarity_over_time(models, central, compared)
    matrix = data.pivot(index="Palavra", columns="Período", values="Similaridade")
    return px.imshow(
        matrix,
        text_auto=".2f",
        zmin=-1,
        zmax=1,
        color_continuous_scale="RdBu_r",
        title=f'Mapa de calor das similaridades com “{normalize_token(central)}”',
        aspect="auto",
    )


def semantic_network_figure(models: ModelSeries, token: str, topn: int = 8) -> go.Figure:
    token = normalize_token(token)
    graph = nx.Graph()
    graph.add_node(token, central=True)
    for name, model in models:
        period = period_label(name)
        for neighbor, score in model.most_similar(token, topn=topn):
            graph.add_node(neighbor, central=False)
            graph.add_edge(token, neighbor, weight=float(score), period=period)
    positions = nx.spring_layout(graph, seed=42, weight="weight")
    edge_x, edge_y = [], []
    for source, target in graph.edges():
        x0, y0 = positions[source]
        x1, y1 = positions[target]
        edge_x.extend((x0, x1, None))
        edge_y.extend((y0, y1, None))
    edges = go.Scatter(x=edge_x, y=edge_y, mode="lines", line={"width": 1, "color": "#94a3b8"}, hoverinfo="none")
    nodes = list(graph.nodes())
    node_trace = go.Scatter(
        x=[positions[node][0] for node in nodes],
        y=[positions[node][1] for node in nodes],
        mode="markers+text",
        text=nodes,
        textposition="top center",
        marker={
            "size": [28 if node == token else 13 + graph.degree(node) for node in nodes],
            "color": ["#ec4899" if node == token else "#14b8a6" for node in nodes],
            "line": {"width": 1, "color": "white"},
        },
        hovertemplate="%{text}<extra></extra>",
    )
    fig = go.Figure((edges, node_trace))
    fig.update_layout(
        title=f'Rede do campo semântico de “{token}”',
        template="plotly_white",
        showlegend=False,
        xaxis={"visible": False},
        yaxis={"visible": False},
        margin={"l": 20, "r": 20, "t": 70, "b": 20},
    )
    return fig


def time_strata_figure(models: ModelSeries, token: str, topn: int = 8) -> go.Figure:
    token = normalize_token(token)
    vocabulary: Counter[str] = Counter()
    neighbors_by_period: dict[str, dict[str, float]] = {}
    for name, model in models:
        period = period_label(name)
        values = dict(model.most_similar(token, topn=topn))
        neighbors_by_period[period] = values
        vocabulary.update(values)
    terms = [term for term, _ in vocabulary.most_common(min(30, len(vocabulary)))]
    matrix = pd.DataFrame({period: {term: values.get(term, np.nan) for term in terms} for period, values in neighbors_by_period.items()})
    return px.imshow(
        matrix,
        text_auto=".2f",
        zmin=0,
        zmax=1,
        color_continuous_scale="Viridis",
        title=f'Estratos temporais do campo semântico de “{token}”',
        aspect="auto",
    )


def word_vectors_figure(model_name: str, model: KeyedVectors, tokens: list[str]) -> go.Figure:
    tokens = [normalize_token(token) for token in tokens if normalize_token(token) in model]
    if len(tokens) < 3:
        raise ValueError("Selecione ao menos três palavras presentes no modelo.")
    coordinates = PCA(n_components=2).fit_transform(np.vstack([model[token] for token in tokens]))
    data = pd.DataFrame({"x": coordinates[:, 0], "y": coordinates[:, 1], "Palavra": tokens})
    fig = px.scatter(data, x="x", y="y", text="Palavra", title=f"Vetores de palavras — {period_label(model_name)}", template="plotly_white")
    fig.update_traces(marker={"size": 13, "color": "#14b8a6"}, textposition="top center")
    fig.update_xaxes(title="Componente principal 1")
    fig.update_yaxes(title="Componente principal 2")
    return fig


def analogy(models: ModelSeries, a: str, b: str, c: str, topn: int = 10) -> pd.DataFrame:
    a, b, c = map(normalize_token, (a, b, c))
    rows = []
    for name, model in models:
        for answer, score in model.most_similar(positive=[b, c], negative=[a], topn=topn):
            rows.append({"Período": period_label(name), "Resultado": answer, "Similaridade": float(score)})
    return pd.DataFrame(rows)


def odd_one_out(models: ModelSeries, tokens: list[str]) -> pd.DataFrame:
    tokens = [normalize_token(token) for token in tokens]
    return pd.DataFrame(
        {"Período": period_label(name), "Elemento destoante": model.doesnt_match(tokens)}
        for name, model in models
    )


def frequency_over_time(models: ModelSeries, tokens: list[str]) -> pd.DataFrame:
    tokens = [normalize_token(token) for token in tokens]
    rows = []
    for name, model in models:
        for token in tokens:
            try:
                count = int(model.get_vecattr(token, "count"))
            except (KeyError, TypeError):
                count = 0
            rows.append({"Período": period_label(name), "Palavra": token, "Frequência no modelo": count})
    return pd.DataFrame(rows)


def frequency_figure(data: pd.DataFrame) -> go.Figure:
    return px.line(data, x="Período", y="Frequência no modelo", color="Palavra", markers=True, title="Frequência registrada nos modelos", template="plotly_white")


def semantic_shift(models: ModelSeries, tokens: list[str], topn: int = 20, aligned: bool = True) -> pd.DataFrame:
    tokens = [normalize_token(token) for token in tokens]
    first_name, first = models[0]
    last_name, last = models[-1]
    rows = []
    for token in tokens:
        cosine = float(first.cosine_similarities(first[token], np.asarray([last[token]]))[0]) if aligned else np.nan
        first_set = {word for word, _ in first.most_similar(token, topn=topn)}
        last_set = {word for word, _ in last.most_similar(token, topn=topn)}
        union = first_set | last_set
        jaccard = len(first_set & last_set) / len(union) if union else 1.0
        rows.append({
            "Palavra": token,
            "Período inicial": period_label(first_name),
            "Período final": period_label(last_name),
            "Mudança vetorial (1 − cosseno)": 1 - cosine,
            "Mudança do campo (1 − Jaccard)": 1 - jaccard,
        })
    return pd.DataFrame(rows)


def semantic_shift_figure(data: pd.DataFrame) -> go.Figure:
    metrics = [column for column in ("Mudança vetorial (1 − cosseno)", "Mudança do campo (1 − Jaccard)") if not data[column].isna().all()]
    melted = data.melt(id_vars="Palavra", value_vars=metrics, var_name="Métrica", value_name="Mudança")
    return px.bar(melted, x="Palavra", y="Mudança", color="Métrica", barmode="group", title="Mudança semântica entre o primeiro e o último período", template="plotly_white")
