## rag (using cleaned data.csv after processing -> data_fixed.csv)
# if there is no very similar q&a in dataset, generate using distilgpt2 fine-tuned
# ^^ responses would be better with something like microsfot/phi2 or tinyllama
# but not powerful enough computing resources locally for something like that 

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
from typing import List, Dict
import csv
import os

class WomensHealthRAG:
    def __init__(self, knowledge_base_path: str, 
                 generation_model_path: str = "./chat/distilgpt2-finetuned"):
        """Initialize RAG system with feedback capabilities"""
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        self.knowledge_base_path = knowledge_base_path
        print(f"Using device: {self.device}")
        
        # Load knowledge base with robust CSV parsing
        print("Loading knowledge base...")
        try:
            self.kb = pd.read_csv(
                knowledge_base_path,
                quoting=csv.QUOTE_ALL,
                escapechar='\\',
                encoding='utf-8',
                engine='python'
            )
        except Exception as e:
            print(f"⚠️ Error with strict parsing, trying lenient mode: {e}")
            self.kb = pd.read_csv(
                knowledge_base_path,
                on_bad_lines='skip',
                engine='python',
                encoding='utf-8'
            )
        
        self.kb.columns = [c.strip().lower().replace("\ufeff", "") for c in self.kb.columns]
        self.kb = self.kb.dropna(subset=['instruction', 'output'])
        print(f"   Loaded {len(self.kb)} Q&A pairs")
        
        # Load embedding model
        print("Loading embedding model...")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Create embeddings
        print("Creating knowledge base embeddings...")
        self.kb_embeddings = self.embedder.encode(
            self.kb['instruction'].tolist(),
            show_progress_bar=True,
            batch_size=32
        )
        
        # Load fine-tuned DistilGPT2
        print(f"⚡ Loading fine-tuned DistilGPT2 from {generation_model_path}...")
        
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
                self.gen_model.to(self.device)
                self.gen_model.eval()
                print("Fine-tuned DistilGPT2 loaded successfully!")
                self.using_finetuned = True
            except Exception as e:
                print(f"⚠️ Could not load fine-tuned model: {e}")
                print("   Falling back to base DistilGPT2...")
                self._load_base_model()
        else:
            print(f"⚠️ Path {generation_model_path} not found")
            print("   Falling back to base DistilGPT2...")
            self._load_base_model()
        
        print("RAG system ready!\n")
    
    def _load_base_model(self):
        """Load base DistilGPT2 as fallback"""
        self.gen_tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
        self.gen_tokenizer.pad_token = self.gen_tokenizer.eos_token
        self.gen_model = AutoModelForCausalLM.from_pretrained(
            "distilgpt2",
            torch_dtype=torch.float32
        )
        self.gen_model.to(self.device)
        self.gen_model.eval()
        self.using_finetuned = False
    
    def retrieve_context(self, query: str, top_k: int = 3) -> List[Dict]:
        """Retrieve most relevant Q&A pairs from knowledge base"""
        query_embedding = self.embedder.encode([query])[0]
        
        similarities = np.dot(self.kb_embeddings, query_embedding) / (
            np.linalg.norm(self.kb_embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        relevant_context = []
        for idx in top_indices:
            relevant_context.append({
                'question': self.kb.iloc[idx]['instruction'],
                'answer': self.kb.iloc[idx]['output'],
                'similarity': float(similarities[idx])
            })
        
        return relevant_context
    
    def generate_response_simple(self, user_query: str, top_k: int = 3, verbose: bool = False, 
                                similarity_threshold: float = 0.5, regenerate: bool = False) -> Dict:
        """
        Generate response and return metadata for feedback system
        Returns: {
            'reply': str,
            'needs_feedback': bool,
            'similarity': float,
            'response_type': str  # 'direct', 'generated', or 'fallback'
        }
        """
        context = self.retrieve_context(user_query, top_k=top_k)
        max_similarity = context[0]['similarity']
        
        if verbose:
            print(f"Retrieved {len(context)} relevant examples:")
            for i, ctx in enumerate(context, 1):
                print(f"   {i}. {ctx['question'][:50]}... (similarity: {ctx['similarity']:.3f})")
            print(f"Max similarity: {max_similarity:.3f}")
        
        # Strategy 1: High similarity - use direct answer
        if max_similarity > 0.75:
            if verbose:
                print("✨ High similarity - using direct answer with context")
            
            base_answer = context[0]['answer']
            additional_info = []
            for ctx in context[1:]:
                if ctx['similarity'] > 0.7 and ctx['answer'] != context[0]['answer']:
                    additional_info.append(ctx['answer'])
            
            reply = f"{base_answer}\n\nAdditionally, {additional_info[0]}" if additional_info else base_answer
            
            return {
                'reply': reply,
                'needs_feedback': False,
                'similarity': max_similarity,
                'response_type': 'direct'
            }
        
        # Strategy 2: Medium similarity - use model generation with feedback
        elif max_similarity > similarity_threshold:
            if verbose:
                model_type = "fine-tuned DistilGPT2" if self.using_finetuned else "base DistilGPT2"
                print(f"⚡ Medium similarity - using {model_type} for generation")
            
            context_str = ""
            for ctx in context[:2]:
                context_str += f"Q: {ctx['question']}\nA: {ctx['answer']}\n\n"
            
            if self.using_finetuned:
                prompt = f"<|user|>\n{user_query}\n<|assistant|>\n"
            else:
                prompt = f"Based on this information:\n\n{context_str}\nQuestion: {user_query}\nAnswer:"
            
            inputs = self.gen_tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=512
            ).to(self.device)
            
            # Adjust temperature for regeneration
            temperature = 0.9 if regenerate else 0.7
            
            with torch.no_grad():
                output_ids = self.gen_model.generate(
                    **inputs,
                    max_new_tokens=100,
                    do_sample=True,
                    top_k=50,
                    top_p=0.9,
                    temperature=temperature,
                    repetition_penalty=1.15,
                    pad_token_id=self.gen_tokenizer.pad_token_id,
                    eos_token_id=self.gen_tokenizer.eos_token_id
                )
            
            full_output = self.gen_tokenizer.decode(output_ids[0], skip_special_tokens=True)
            
            if self.using_finetuned and "<|assistant|>" in full_output:
                reply = full_output.split("<|assistant|>")[-1].strip()
                reply = reply.split("<|user|>")[0].strip()
                reply = reply.split("<|endoftext|>")[0].strip()
            elif "Answer:" in full_output:
                reply = full_output.split("Answer:")[-1].strip()
            else:
                reply = full_output[len(prompt):].strip()
            
            reply = reply.split("\n\n")[0].strip()
            
            if verbose:
                print(f"Generated: {reply[:100]}...")
            
            if reply and len(reply) > 20:
                return {
                    'reply': reply,
                    'needs_feedback': True,  # Requires user validation
                    'similarity': max_similarity,
                    'response_type': 'generated'
                }
            else:
                if verbose:
                    print("⚠️ Generation produced poor output - falling back")
                if max_similarity > 0.6:
                    return {
                        'reply': context[0]['answer'],
                        'needs_feedback': False,
                        'similarity': max_similarity,
                        'response_type': 'direct'
                    }
        
        # Strategy 3: Low similarity - resources message
        if verbose:
            print("Low similarity - providing Resources tab message")
        
        return {
            'reply': "I'm sorry, I can't provide an answer to that. Please see the resources tab for more information!",
            'needs_feedback': False,
            'similarity': max_similarity,
            'response_type': 'fallback'
        }
    
    def add_to_dataset(self, question: str, answer: str) -> bool:
        """Add a validated Q&A pair to the dataset"""
        try:
            # Add to in-memory dataframe
            new_row = pd.DataFrame({
                'instruction': [question.strip()],
                'output': [answer.strip()]
            })
            self.kb = pd.concat([self.kb, new_row], ignore_index=True)
            
            # Save to CSV
            self.kb.to_csv(self.knowledge_base_path, index=False, quoting=csv.QUOTE_ALL)
            
            # Update embeddings for the new entry
            new_embedding = self.embedder.encode([question.strip()])
            self.kb_embeddings = np.vstack([self.kb_embeddings, new_embedding])
            
            print(f"Added to dataset: {question[:50]}...")
            return True
        except Exception as e:
            print(f"Error adding to dataset: {e}")
            return False
    
    def reload_dataset(self):
        """Reload dataset and embeddings after external updates"""
        try:
            self.kb = pd.read_csv(self.knowledge_base_path, on_bad_lines='skip', engine='python')
            self.kb.columns = [c.strip().lower().replace("\ufeff", "") for c in self.kb.columns]
            self.kb = self.kb.dropna(subset=['instruction', 'output'])
            self.kb_embeddings = self.embedder.encode(self.kb['instruction'].tolist(), batch_size=32)
            print(f"Dataset reloaded: {len(self.kb)} Q&A pairs")
            return True
        except Exception as e:
            print(f"Error reloading dataset: {e}")
            return False