import os
from dotenv import load_dotenv
load_dotenv()
K8S_NAMESPACE=os.getenv("K8S_NAMESPACE","demo-app")
PROMETHEUS_URL=os.getenv("PROMETHEUS_URL","http://localhost:9090").rstrip("/")
OLLAMA_URL=os.getenv("OLLAMA_URL","http://localhost:11434").rstrip("/")
OLLAMA_MODEL=os.getenv("OLLAMA_MODEL","qwen3")
LOG_TAIL_LINES=int(os.getenv("LOG_TAIL_LINES","100"))
