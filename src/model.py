from transformers import pipeline
import torch
from src.config import MODEL_NAME, HF_TOKEN, MAX_NEW_TOKENS, BATCH_SIZE
from typing import List, Dict
import pandas as pd

class LLMHypernymExtractor:
    def __init__(self):
        self.pipeline = pipeline(
            "text-generation",
            model=MODEL_NAME,
            torch_dtype=torch.float16,
            device_map="auto",
            token=HF_TOKEN
        )
        self.pipeline.tokenizer.pad_token_id = self.pipeline.model.config.eos_token_id[0]
        self.pipeline.tokenizer.padding_side = "left"
        self.pipeline.model.generation_config.pad_token_id = self.pipeline.tokenizer.pad_token_id

    def extract_actions(self, texts):
        messages = []
        for text in texts:
            messages.append([{
                "role": "system",
                "content":
                    """
                    Extrahiere aus der neuesten E-Mail an den Empfänger die Aktion (Verb im Infinitiv) und das Objekt (Substantiv).
            
                    Format: [AKTION, OBJEKT]
                    Keine Erklärungen oder Zusatzinfos.
            
                    Regeln:
                    - Die Antwort muss auf Deutsch sein und das Objekt ein Substantiv sein.
                    - Falls keine klare Aufgabe bzw. passende [AKTION, OBJEKT] erkennbar ist, bitte: [UNBEKANNT, UNBEKANNT] zurückgeben.
            
                    Beispiele:
                    [antworten, E-Mail]
                    [halten, Votrag]
                    [senden, Dokument]
                    [anmelden, Projekt]
                    [weiterleiten, Info]
                    """
            }, {
                "role": "user",
                "content": f"\"{text}\""
            }])

        outputs = self.pipeline(
            messages,
            max_new_tokens=MAX_NEW_TOKENS,
            batch_size=BATCH_SIZE
        )
        return [output[0]["generated_text"][-1]["content"].strip() for output in outputs]

    def extract_hypernyms(self, words):
        messages = []
        for word in words:
            messages.append([{
                "role": "system",
                "content":
                    """
                    Du bist ein Linguistik-Experte mit tiefgehendem Wissen über Semantik und Wortbedeutungen.
                    Bestimme die übergeordneten Hypernyme für das gegebene deutsche Wort.
                    
                    Anforderungen:
                    - Gib mehrere Hypernyme an, getrennt durch ein Komma.
                    - Die Antwort muss auf Deutsch sein.
                    - Keine zusätzlichen Erklärungen, Formatierungen oder Beispiele.
                    
                    Beispiele:
                    - Eingabe: Information
                    - Ausgabe: Kommunikationseinheit, Einheit, Entität
                    
                    - Eingabe: Klausur
                    - Ausgabe: Examen, Prüfung, Leistung
                    
                    - Eingabe: Mitarbeiter
                    - Ausgabe: Berufstätiger, Person, Lebewesen
                    
                    - Eingabe: Mail
                    - Ausgabe: Nachricht, Mitteilung, Senden
                    """
            }, {
                "role": "user",
                "content": f"\"{word}\""
            }])

        outputs = self.pipeline(
            messages,
            max_new_tokens=MAX_NEW_TOKENS,
            batch_size=BATCH_SIZE
        )
        return outputs


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
