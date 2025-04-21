from germanetpy.germanet import Germanet
from src.config import GERMANET_PATH
import pandas as pd

class GermanetAnalyzer:
    def __init__(self):
        self.germanet = Germanet(GERMANET_PATH)

    def get_hypernym_chain(self, word: str) -> pd.DataFrame:
        synsets = self.germanet.get_synsets_by_orthform(word)
        if not synsets:
            return pd.DataFrame()

        chain_data = []
        # BFS-Queue mit Hop-Level
        for synset_index, synset in enumerate(synsets):
            queue = [(synset, 1)]
            visited = set()

            while queue:
                current_synset, hop = queue.pop(0)
                if current_synset.id in visited:
                    continue
                visited.add(current_synset.id)

                for hypernym in current_synset.direct_hypernyms:
                    chain_data.append([
                        current_synset.id,
                        ", ".join([lu.orthform for lu in current_synset.lexunits]),
                        hypernym.id,
                        ", ".join([lu.orthform for lu in hypernym.lexunits]),
                        hop,
                        synset_index
                    ])
                    if not hypernym.is_root():
                        queue.append((hypernym, hop + 1))

        return pd.DataFrame(chain_data,
                            columns=["synset_id", "hyponym", "hypernym_id", "hypernym", "hop", "synset_index"])