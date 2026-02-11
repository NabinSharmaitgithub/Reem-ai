import os
from llama_cpp import Llama

# Default path to the GGUF model
DEFAULT_MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "model.gguf")

class ReemBrain:
    def __init__(self, model_path=DEFAULT_MODEL_PATH):
        self.model_path = model_path
        self.llm = None
        self.load_model()

    def load_model(self):
        if os.path.exists(self.model_path):
            try:
                # Initializing the local LLM
                self.llm = Llama(
                    model_path=self.model_path,
                    n_ctx=2048,
                    n_threads=4  # Adjust based on CPU cores
                )
                print(f"Model loaded successfully from {self.model_path}")
            except Exception as e:
                print(f"Failed to load model: {e}")
        else:
            print(f"Model file NOT found at {self.model_path}")
            print("Please download a GGUF model and place it there.")

    def think(self, prompt):
        if not self.llm:
            return '{"error": "Model not loaded"}'

        try:
            # Generate response
            response = self.llm(
                prompt,
                max_tokens=512,
                temperature=0.1,
                top_p=0.95,
                echo=False
            )
            return response["choices"][0]["text"].strip()
        except Exception as e:
            return f'{"error": "{str(e)}"}'

# Singleton instance for easy access
brain = ReemBrain()

def think(prompt):
    """
    Standard function to get a response from the local LLM.
    """
    return brain.think(prompt)

if __name__ == "__main__":
    print("LLM module ready.")
