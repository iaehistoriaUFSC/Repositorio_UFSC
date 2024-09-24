import streamlit as st
from Word_Embeddings.Treinamento.pretrained_language_models import embeddings
import json
import numpy as np

def main():
    st.title("Text Embeddings and Visualization")

    dataset_name = st.text_input("Enter dataset name:", "trec")
    # filter_keyword = st.text_input("Enter filter keyword:", "history")
    # subset_size = st.number_input("Enter subset size:", min_value=1, max_value=1000, value=100)


    def get_dataset():
        dataset_loader = embeddings.DatasetLoader(dataset_name=dataset_name)
        texts = dataset_loader.get_subset(size=100)
        st.write(f"Loaded {len(texts)} texts from the dataset.")
        return texts

    def get_embeddings(texts):
        embedding_generator = embeddings.EmbeddingGenerator()
        embeddings_data = embedding_generator.generate_embeddings(texts)
        st.write("Generated embeddings for the texts.")
        return embeddings_data

    texts = get_dataset()
    embeddings_data = get_embeddings(texts)


    visualizer = embeddings.Visualizations(embeddings_data, texts)
    fig_2d_pca = visualizer.plot_2d_pca()
    fig_3d_pca = visualizer.plot_3d_pca()
    fig_2d_tsne = visualizer.plot_2d_tsne()
    st.plotly_chart(fig_2d_pca, use_container_width=True)
    st.plotly_chart(fig_3d_pca, use_container_width=True)
    st.plotly_chart(fig_2d_tsne, use_container_width=True)

    cosine_sim = embeddings.Metrics.cosine_similarity(embeddings_data)
    euclidean_dist = embeddings.Metrics.euclidean_distances(embeddings_data)


    avg_cosine_sim = np.mean(cosine_sim)
    avg_euclidean_dist = np.mean(euclidean_dist)


    summary_scores = {
        "Average Cosine Similarity": avg_cosine_sim,
        "Average Euclidean Distance": avg_euclidean_dist
    }


    st.write("Summary of Similarity and Distance Metrics:")
    st.json(summary_scores)


    if st.checkbox('Show full Cosine Similarity Matrix'):
        st.write("Cosine Similarity Matrix:")
        st.write(cosine_sim)

    if st.checkbox('Show full Euclidean Distance Matrix'):
        st.write("Euclidean Distance Matrix:")
        st.write(euclidean_dist)

    dict_scores = {'cosine_similarity': cosine_sim.tolist(), 'euclidean_distances': euclidean_dist.tolist()}

    btn_save_metrics = st.button("Save Metrics")
    if btn_save_metrics:
        with open('metrics_scores.json', 'w') as f:
            json.dump(dict_scores, f)
        st.write("Metrics saved to 'metrics_scores.json'.")