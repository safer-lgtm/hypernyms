from transformers import pipeline
import torch
from src.config import MODEL_NAME, HF_TOKEN, MAX_NEW_TOKENS, BATCH_SIZE


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
