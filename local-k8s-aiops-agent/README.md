# Local Kubernetes AIOps Agent

Read-only training prototype for **Windows + Minikube + Prometheus + Ollama**.

## Architecture
```text
Minikube/Kubernetes ----+
                        +--> Python AIOps Agent --> Ollama --> RCA/recommendations
Prometheus -------------+          |
                                   +--> local Markdown runbooks
```

The LLM recommends actions; it does not mutate the cluster.

## Setup
```powershell
minikube status
kubectl config current-context
kubectl get pods -n demo-app
kubectl get svc -n monitoring
```

Start Prometheus access (adjust Service name if your Helm release differs):
```powershell
kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090
```

Verify Ollama and pull the configured model:
```powershell
ollama --version
ollama pull qwen3
ollama run qwen3
```

Create Python environment:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

## Test each integration
```powershell
python test_kubernetes.py
python test_prometheus.py
python test_ollama.py
```

## Run
```powershell
python agent.py --namespace demo-app --show-context
```

## Safe incident lab
Inject an invalid backend image:
```powershell
kubectl set image deployment/backend backend=nginx:does-not-exist -n demo-app
kubectl get pods -n demo-app
python agent.py
```

Restore:
```powershell
kubectl set image deployment/backend backend=hashicorp/http-echo:1.0 -n demo-app
kubectl rollout status deployment/backend -n demo-app
```

## Prometheus rules
```powershell
kubectl apply -f .\k8s\sample-prometheus-rules.yaml
kubectl get prometheusrule -n monitoring
```

## Push to GitHub
Create an empty GitHub repository, then:
```powershell
git init
git add .
git commit -m "Initial local Kubernetes AIOps agent"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/local-k8s-aiops-agent.git
git push -u origin main
```

`.env`, virtual environments, logs and kubeconfig files are ignored. Never commit credentials or tokens.

## Next evolution
Add Ollama tool calling, Alertmanager webhook ingestion, RAG over runbooks, a chat UI, approval-gated remediation, and an AWS/Bedrock variant.
