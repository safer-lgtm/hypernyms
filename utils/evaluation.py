from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from wordcloud import WordCloud

class Evaluator:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    def cosine_similarity(self, text1: str, text2: str) -> float:
        emb1 = self.model.encode(text1)
        emb2 = self.model.encode(text2)
        return cosine_similarity([emb1], [emb2])[0][0]

    def plot_similarity_distribution(self, similarities):
        plt.figure(figsize=(8, 5))
        plt.hist(similarities, bins=20, color="skyblue", edgecolor="black")
        avg = np.mean(similarities)
        plt.axvline(avg, color='red', linestyle='--', label=f"Durchschnitt: {avg:.2f}")
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()
        return avg

    def generate_wordcloud(self, words: list, title: str):
        text = " ".join(words)
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.title(title, fontsize=16)
        plt.show()