import os

def get_model_path():
    """
    Finds the model.gguf in common locations for both Desktop and Android.
    """
    base_dir = os.path.dirname(__file__)
    path1 = os.path.join(base_dir, "model", "model.gguf")
    if os.path.exists(path1):
        return path1

    path2 = os.path.join(os.getcwd(), "model", "model.gguf")
    if os.path.exists(path2):
        return path2

    path3 = "/sdcard/ReemAI/model/model.gguf"
    if os.path.exists(path3):
        return path3

    return path1

class ReemBrain:
    def __init__(self, model_path=None):
        self.model_path = model_path or get_model_path()
        self.llm = None
        self.load_model()

    def load_model(self):
        try:
            from llama_cpp import Llama
        except ImportError:
            print("llama-cpp-python not installed.")
            return

        if os.path.exists(self.model_path):
            try:
                self.llm = Llama(
                    model_path=self.model_path,
                    n_ctx=2048,
                    n_threads=4
                )
                print(f"Model loaded successfully from {self.model_path}")
            except Exception as e:
                print(f"Failed to load model: {e}")
        else:
            print(f"Model file NOT found at {self.model_path}")

    def think(self, prompt):
        if not self.llm:
            return '{"error": "Model not loaded"}'

        try:
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

brain = ReemBrain()

def think(prompt):
    return brain.think(prompt)

if __name__ == "__main__":
    print("LLM module ready.")
