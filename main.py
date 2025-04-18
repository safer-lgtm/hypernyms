from src.model import LLMHypernymExtractor, HypernymProcessor
from src.data_loader import load_emails, process_llama_output
from src.preprocessing import TextPreprocessor
from src.config import DATA_PATH

def main():
    # Initialisierung
    llm = LLMHypernymExtractor()
    preprocessor = TextPreprocessor()
    hypernym_processor = HypernymProcessor(max_depth=5)

    # Daten laden
    df = load_emails(DATA_PATH)
    print(df.shape)

    # Aktionen extrahieren
    df["json"] = llm.extract_actions(df["file_texts"].tolist())
    df = process_llama_output(df)

    # Lemmatisierung
    df = preprocessor.lemmatize_column(df, "Action")
    df = preprocessor.lemmatize_column(df, "Object")

    # Hypernym-Analyse
    unique_objects = df["objectlemma"].dropna().unique()
    hypernym_results = hypernym_processor.process_hypernym_chains(unique_objects)

    # Save results
    hypernym_results.to_csv("hypernym_chains.csv", index=False)
    print("Sample results:")
    print(hypernym_results.head())

if __name__ == "__main__":
    main()