from typing import List, Dict
import pandas as pd
from tqdm import tqdm
from src.model import LLMHypernymExtractor


class HypernymProcessor:
    def __init__(self, max_depth: int = 5):
        self.max_depth = max_depth

    def build_hypernym_chain(self, word: str, resgroup: pd.DataFrame) -> str:
        """
        Builds a hypernym chain for a given word
        """
        chain = [word]
        if word != "UNBEKANNT":
            current_word = word
            for _ in range(self.max_depth):
                hypernym_data = LLMHypernymExtractor.extract_hypernyms([current_word])
                hypernym_data = hypernym_data[hypernym_data['subword'] == current_word]

                if not hypernym_data.empty:
                    most_common_parent = hypernym_data.iloc[0]['parent']
                    if most_common_parent not in chain:
                        chain.append(most_common_parent)
                        current_word = most_common_parent
                    else:
                        break  # Cycle detected
                else:
                    break  # No hypernyms found
        return " , ".join(chain)

    def process_hypernym_chains(self, words: List[str]) -> pd.DataFrame:
        """
        Processes multiple words to build hypernym chains
        """
        resgroup = LLMHypernymExtractor.extract_hypernyms(words)
        chains = []

        for word in tqdm(words):
            chain = self.build_hypernym_chain(word, resgroup)
            chains.append({"Word": word, "Hypernym_Chain": chain})

        return self._postprocess_chains(chains)

    def _postprocess_chains(self, chains: List[Dict]) -> pd.DataFrame:
        """
        Post-processes the hypernym chains
        """
        df_chains = pd.DataFrame(chains)
        df_chains['Hypernym_Chain'] = df_chains['Hypernym_Chain'].str.split(' , ')

        # Filter out original words from chains
        filtered_chains = []
        for _, row in df_chains.iterrows():
            filtered = [h for h in row['Hypernym_Chain'] if h != row['Word']]
            filtered_chains.append({"Word": row["Word"], "Hypernym_Chain": filtered})

        return pd.DataFrame(filtered_chains)