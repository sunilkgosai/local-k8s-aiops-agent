import requests
from config import OLLAMA_URL, OLLAMA_MODEL
SYSTEM="""You are a Kubernetes SRE incident-analysis assistant.
Use only supplied evidence. Separate facts from hypotheses. Do not invent data.
Use supplied runbooks when relevant. Never claim remediation was executed.
A human SRE must approve remediation.
Return: INCIDENT SUMMARY, EVIDENCE, LIKELY CAUSE, POTENTIAL IMPACT,
RECOMMENDED INVESTIGATION, RECOMMENDED REMEDIATION, CONFIDENCE."""
def analyze(context):
    r=requests.post(OLLAMA_URL+"/api/chat",json={"model":OLLAMA_MODEL,"stream":False,
      "messages":[{"role":"system","content":SYSTEM},{"role":"user","content":"Analyze:\n"+context}]},timeout=300)
    r.raise_for_status()
    return r.json()["message"]["content"]
