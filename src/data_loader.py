import os
import pandas as pd

def load_emails(data_path: str) -> pd.DataFrame:
    file_names = []
    file_texts = []

    for file_name in os.listdir(data_path):
        if file_name.endswith('.txt'):
            with open(os.path.join(data_path, file_name), "r", encoding="utf-8") as f:
                file_names.append(file_name)
                file_texts.append(f.read())

    return pd.DataFrame({
        "file_names": file_names,
        "file_texts": file_texts
    }).sort_values(by=['file_names'])