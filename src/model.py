from transformers import pipeline
import torch
from src.config import MODEL_NAME, HF_TOKEN


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