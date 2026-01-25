## rag (using cleaned data.csv after processing -> data_fixed.csv)
# if there is no very similar q&a in dataset, generate using distilgpt2 fine-tuned
# ^^ responses would be better with something like microsfot/phi2 or tinyllama
# but not powerful enough computing resources locally for something like that 

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
# Import `sentence_transformers` lazily in `__init__` to avoid
# import-time failures when `huggingface_hub` versions are incompatible
# with the installed `sentence-transformers` package.
import numpy as np
import pandas as pd
from typing import List, Dict
import csv
import os

class WomensHealthRAG:
    def __init__(self, knowledge_base_path: str, 
                 generation_model_path: str = "./chat/fine-tune-attempts/distilgpt2-finetuned" ):
        """
        Initialize RAG system with dual models:
        - SentenceTransformer for embeddings
        - Fine-tuned DistilGPT2 for fast generation
        """
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # load knowledge for rag & parse csv
        print("load data")
        try:
            self.kb = pd.read_csv(
                knowledge_base_path,
                quoting=csv.QUOTE_ALL,
                escapechar='\\',
                encoding='utf-8',
                engine='python'
            )
        except Exception as e:
            print(f"Error with parsing -> trying again: {e}")
            self.kb = pd.read_csv(
                knowledge_base_path,
                on_bad_lines='skip',
                engine='python',
                encoding='utf-8'
            )
        
        self.kb.columns = [c.strip().lower().replace("\ufeff", "") for c in self.kb.columns]
        self.kb = self.kb.dropna(subset=['instruction', 'output'])
        print(f"   Loaded {len(self.kb)} Q&A pairs")
        
        # Load embedding model (lightweight for similarity search)
        # Import lazily because some environments have incompatible
        # `huggingface_hub` versions that break `sentence-transformers`.
        print("Embedding model (all-MiniLM-L6) loading")
        try:
            from sentence_transformers import SentenceTransformer
        except Exception as e:
            raise ImportError(
                "sentence_transformers import failed. "
                "Install a compatible version (or pin huggingface-hub) "
                "to use the RAG features. Original error: " + str(e)
            )

        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # embeddings
        print("Making embeddings for csv dataset")
        self.kb_embeddings = self.embedder.encode(
            self.kb['instruction'].tolist(),
            show_progress_bar=True,
            batch_size=32
        )
        
        # load fine-tuned DistilGPT2 
        print(f"Loading fine-tuned DistilGPT2 from {generation_model_path}")
        
        # local path??
        if os.path.exists(generation_model_path):
            try:
                self.gen_tokenizer = AutoTokenizer.from_pretrained(
                    generation_model_path,
                    local_files_only=True
                )
                if self.gen_tokenizer.pad_token is None:
                    self.gen_tokenizer.pad_token = self.gen_tokenizer.eos_token
                
                self.gen_model = AutoModelForCausalLM.from_pretrained(
                    generation_model_path,
                    torch_dtype=torch.float32,
                    local_files_only=True
                )
                """Lightweight, defensive RAG/LLM helper.

                This module performs lazy imports and supports loading a local model path
                specified by the `LOCAL_LLM_PATH` environment variable or passed directly.
                If heavy libraries (torch/transformers/sentence-transformers) are missing,
                the wrapper exposes stable methods that return fallbacks instead of crashing
                the Flask app.
                """

                from typing import Optional
                import os
                import traceback


                class RagWrapper:
                    """Wrapper that lazily loads embedding + generation models.

                    Usage:
                      R = RagWrapper()
                      R.load(model_path='path/to/model')  # optional
                      R.generate('prompt')
                    """

                    def __init__(self):
                        self.model_path = os.environ.get('LOCAL_LLM_PATH')
                        self._ready = False
                        self._has_transformers = False
                        self._has_sentence_transformers = False
                        self._device = 'cpu'
                        self._embedder = None
                        self._generator = None
                        self._tokenizer = None

                    def load(self, model_path: Optional[str] = None, force: bool = False) -> bool:
                        """Attempt to load transformer and embedding models. Returns True if successful."""
                        if model_path:
                            self.model_path = model_path
                        if self._ready and not force:
                            return True

                        # Attempt imports lazily
                        try:
                            import torch
                            from transformers import AutoTokenizer, AutoModelForCausalLM
                            self._has_transformers = True
                        except Exception:
                            self._has_transformers = False

                        try:
                            from sentence_transformers import SentenceTransformer
                            self._has_sentence_transformers = True
                        except Exception:
                            self._has_sentence_transformers = False

                        # set device if torch present
                        if self._has_transformers:
                            try:
                                import torch
                                self._device = 'mps' if torch.backends.mps.is_available() else ('cuda' if torch.cuda.is_available() else 'cpu')
                            except Exception:
                                self._device = 'cpu'

                        # Load embedder if available
                        if self._has_sentence_transformers:
                            try:
                                from sentence_transformers import SentenceTransformer
                                self._embedder = SentenceTransformer('all-MiniLM-L6-v2')
                            except Exception:
                                self._embedder = None

                        # Load generator model if available and path specified or fallback to small public model
                        if self._has_transformers:
                            try:
                                from transformers import AutoTokenizer, AutoModelForCausalLM
                                model_source = self.model_path or 'distilgpt2'
                                # prefer local files if a path is given
                                local_only = bool(self.model_path)
                                self._tokenizer = AutoTokenizer.from_pretrained(model_source, local_files_only=local_only)
                                if getattr(self._tokenizer, 'pad_token', None) is None:
                                    self._tokenizer.pad_token = self._tokenizer.eos_token
                                self._generator = AutoModelForCausalLM.from_pretrained(model_source, local_files_only=local_only)
                                try:
                                    self._generator.to(self._device)
                                except Exception:
                                    pass
                            except Exception:
                                traceback.print_exc()
                                self._generator = None

                        self._ready = bool(self._generator or self._embedder)
                        return self._ready

                    def is_ready(self) -> bool:
                        return self._ready

                    def generate(self, prompt: str, max_new_tokens: int = 128) -> str:
                        """Generate text using loaded generator or return a safe fallback message."""
                        if self._generator and self._tokenizer:
                            try:
                                import torch
                                inputs = self._tokenizer(prompt, return_tensors='pt', truncation=True, max_length=512)
                                # move to device if possible
                                if hasattr(inputs, 'to'):
                                    try:
                                        inputs = {k: v.to(self._device) for k, v in inputs.items()}
                                    except Exception:
                                        pass
                                with torch.no_grad():
                                    out = self._generator.generate(**inputs, max_new_tokens=max_new_tokens, pad_token_id=self._tokenizer.pad_token_id)
                                text = self._tokenizer.decode(out[0], skip_special_tokens=True)
                                # trim prompt prefix
                                if prompt and text.startswith(prompt):
                                    return text[len(prompt):].strip()
                                return text.strip()
                            except Exception:
                                traceback.print_exc()
                                return "[model error] Unable to generate response — check server logs."

                        # fallback: if embedder present, return nearest KB answer not implemented here
                        if self._embedder:
                            return "[limited] Model backend not available; embedding support exists but generation is disabled."

                        return "[unavailable] No local model or required libraries (transformers, torch) are installed."


                # module-level singleton
                _rag = RagWrapper()

                def get_rag() -> RagWrapper:
                    return _rag
