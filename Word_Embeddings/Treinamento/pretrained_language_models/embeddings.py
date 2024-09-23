import os
from typing import List
import json
import numpy as np
import plotly.express as px
from datasets import load_dataset
from plotly.graph_objs import Figure
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances


class DatasetLoader:
    def __init__(self, dataset_name: str, split: str = 'train', filter_keyword: str = 'history'):
        self.dataset_name = dataset_name
        self.split = split
        self.filter_keyword = filter_keyword
        self.data = self.load_dataset()

    def load_dataset(self) -> List[str]:
        dataset = load_dataset(self.dataset_name, split=self.split)
        return [entry['text'] for entry in dataset if self.filter_keyword in entry['text'].lower()]

    def get_subset(self, size: int) -> List[str]:
        return self.data[:size]


class EmbeddingGenerator:
    def __init__(self, model_name: str = 'sentence-transformers/all-mpnet-base-v2'):
        self.model = SentenceTransformer(model_name)

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts, show_progress_bar=True)


class Visualizations:
    def __init__(self, embeddings: np.ndarray, texts: List[str]):
        self.embeddings = embeddings
        self.texts = texts

    def plot_2d_pca(self) -> Figure:
        pca_2d = PCA(n_components=2)
        embeddings_2d = pca_2d.fit_transform(self.embeddings)
        fig = px.scatter(x=embeddings_2d[:, 0], y=embeddings_2d[:, 1],
                         title="2D PCA Visualization",
                         labels={'x': 'PCA Dimension 1', 'y': 'PCA Dimension 2'},
                         text=self.texts)
        fig.update_traces(textposition='top center')
        # fig.show()
        return fig

    def plot_3d_pca(self) -> Figure:
        pca_3d = PCA(n_components=3)
        embeddings_3d = pca_3d.fit_transform(self.embeddings)
        fig = px.scatter_3d(x=embeddings_3d[:, 0], y=embeddings_3d[:, 1], z=embeddings_3d[:, 2],
                            title="3D PCA Visualization",
                            labels={'x': 'PCA Dimension 1', 'y': 'PCA Dimension 2', 'z': 'PCA Dimension 3'},
                            text=self.texts)
        fig.update_traces(textposition='top center')
        # fig.show()
        return fig

    def plot_2d_tsne(self) -> Figure:
        n_samples = len(self.embeddings)
        perplexity_value = min(30, n_samples // 3)
        tsne_2d = TSNE(n_components=2, perplexity=perplexity_value, random_state=42)
        embeddings_tsne_2d = tsne_2d.fit_transform(self.embeddings)
        fig = px.scatter(x=embeddings_tsne_2d[:, 0], y=embeddings_tsne_2d[:, 1],
                         title=f"2D t-SNE Visualization (Perplexity: {perplexity_value})",
                         labels={'x': 't-SNE Dimension 1', 'y': 't-SNE Dimension 2'},
                         text=self.texts)
        fig.update_traces(textposition='top center')
        # fig.show()
        return fig

    def run_and_save_all_visualizations(self, save_folder: str = 'visualizations', save_format: str = 'png'):
        os.makedirs(save_folder, exist_ok=True)
        fig_1 = self.plot_2d_pca()
        fig_2 = self.plot_3d_pca()
        fig_3 = self.plot_2d_tsne()
        if save_format == 'html':
            fig_1.write_html(os.path.join(save_folder, "2d_pca.html"))
            fig_2.write_html(os.path.join(save_folder, "3d_pca.html"))
            fig_3.write_html(os.path.join(save_folder, "2d_tsne.html"))
        else:
            fig_1.write_image(os.path.join(save_folder, "2d_pca.png"))
            fig_2.write_image(os.path.join(save_folder, "3d_pca.png"))
            fig_3.write_image(os.path.join(save_folder, "2d_tsne.png"))
        print(f"Visualizations saved in {save_folder} folder")
        return fig_1, fig_2, fig_3


class Metrics:
    @staticmethod
    def cosine_similarity(embeddings: np.ndarray) -> np.ndarray:
        return cosine_similarity(embeddings)

    @staticmethod
    def euclidean_distances(embeddings: np.ndarray) -> np.ndarray:
        return euclidean_distances(embeddings)


if __name__ == '__main__':
    dataset_loader = DatasetLoader(dataset_name='trec')
    texts = dataset_loader.get_subset(size=100)

    embedding_generator = EmbeddingGenerator()
    embeddings = embedding_generator.generate_embeddings(texts)

    visualizer = Visualizations(embeddings, texts)
    # visualizer.run_and_save_all_visualizations(save_folder='visualizations', save_format='html')

    cosine_sim = Metrics.cosine_similarity(embeddings)
    euclidean_dist = Metrics.euclidean_distances(embeddings)
    dict_scores = {'cosine_similarity': cosine_sim, 'euclidean_distances': euclidean_dist}
    print(dict_scores)
    # save to file
    with open('metrics_scores.json', 'w') as f:
        json.dump(dict_scores, f)
        f.close()