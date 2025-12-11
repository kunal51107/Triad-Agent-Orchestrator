import os
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

def get_groq_models():
    try:
        
        client = Groq(
            api_key=os.getenv("GROQ_API_KEY"),
        )

        print("Fetching available Groq models...\n")
        models = client.models.list()

        
        print(f"{'MODEL ID':<40} {'OWNER':<15}")
        print("-" * 60)
        
        for model in models.data:
            print(f"{model.id:<40} {model.owned_by:<15}")

    except Exception as e:
        print(f"Error fetching models: {e}")

if __name__ == "__main__":
    get_groq_models()