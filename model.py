from langchain.llms.base import LLM
from typing import Any, List, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
from transformers import pipeline
import torch
import os
from openai import OpenAI
import httpx
class deepseek(LLM):
    api_key = ''
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
    def _call(self, prompt: str, stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = True,
              **kwargs: Any) -> str:
        client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model="deepseek-coder",  
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            stream = False
        )
        return response.choices[0].message.content
    @property
    def _llm_type(self) -> str:
        return "deepseek"  
        
    @property
    def _llm_type(self) -> str:
        return "DeepSeek_LLM"

class CodeLlama13B(LLM):

    tokenizer: AutoTokenizer = None
    model: AutoModelForCausalLM = None
    def __init__(self, model_path: str):

        super().__init__()
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            trust_remote_code=True,
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )
        self.model.generation_config = GenerationConfig.from_pretrained(model_path)
        self.model.generation_config.pad_token_id = self.model.generation_config.eos_token_id
        self.model = self.model.eval()

    def _call(self, prompt : str, stop: Optional[List[str]] = None,
                run_manager: Optional[CallbackManagerForLLMRun] = True,
                **kwargs: Any) -> str:
        messages = [
            {"role": "user", "content": prompt}
        ]    
        input_tensor = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt"
        )
        outputs = self.model.generate(input_tensor.to(self.model.device), max_new_tokens=5000)
        response = self.tokenizer.decode(outputs[0][input_tensor.shape[1]:], skip_special_tokens=True)
        return response
    @property
    def _llm_type(self) -> str:
        return "CodeLlama13B"
 
class GPT(LLM):
    api_key = ''
    mymodel = ''
    def __init__(self, api_key: str,model):
        super().__init__()
        self.api_key = api_key
        self.mymodel = model
    def _call(self, prompt: str,stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = True,
              **kwargs: Any) -> str:
        client = OpenAI(
            api_key=self.api_key,
        )
        response = client.chat.completions.create(
            model = self.mymodel,  
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    @property
    def _llm_type(self) -> str:
        return "gpt"  
    
class StarChat(LLM):

    mypipe = ''
    def __init__(self, model_path: str):

        super().__init__()
        self.mypipe = pipeline("text-generation", model=model_path, torch_dtype=torch.bfloat16, device_map="auto")

    def _call(self, prompt : str, stop: Optional[List[str]] = None,
                run_manager: Optional[CallbackManagerForLLMRun] = True,
                **kwargs: Any) -> str:

        prompt_template = "<|system|>\n<|end|>\n<|user|>\n{query}<|end|>\n<|assistant|>"
        myprompt = prompt_template.format(query=prompt)
        outputs = self.mypipe(myprompt, max_new_tokens=2560, do_sample=True, temperature=0.2, top_k=50, top_p=0.95, eos_token_id=49155)
                   
        response = outputs[0]['generated_text'].split('<|assistant|>')[1]
        return response
    @property
    def _llm_type(self) -> str:
        return "StarChat"

if __name__ == "__main__":
    print("ok")
    llm = StarChat("")
    prompt = "hello"
    response = llm._call(prompt)
    print(response)