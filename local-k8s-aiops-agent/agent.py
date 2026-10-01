import argparse,json
from config import K8S_NAMESPACE
import kubernetes_tools as k
import prometheus_tools as p
from runbook_tools import load_runbooks
from llm import analyze

def safe(name,fn):
    try: return fn()
    except Exception as e: return {"collection_error":name,"message":str(e)}

def collect(ns):
    return {"namespace":ns,
      "kubernetes":{"pods":safe("pods",lambda:k.get_pods(ns)),
                    "services":safe("services",lambda:k.get_services(ns)),
                    "endpoints":safe("endpoints",lambda:k.get_endpoints(ns)),
                    "events":safe("events",lambda:k.get_events(ns)),
                    "logs":safe("logs",lambda:k.get_logs(ns))},
      "prometheus":{"cpu":safe("cpu",lambda:p.cpu(ns)),
                    "memory":safe("memory",lambda:p.memory(ns)),
                    "restarts":safe("restarts",lambda:p.restarts(ns)),
                    "not_ready":safe("not_ready",lambda:p.not_ready(ns))},
      "runbooks":load_runbooks()}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--namespace",default=K8S_NAMESPACE)
    ap.add_argument("--show-context",action="store_true")
    a=ap.parse_args()
    print("LOCAL KUBERNETES AIOPS AGENT | Namespace:",a.namespace)
    ctx=json.dumps(collect(a.namespace),indent=2,default=str)
    if a.show_context: print(ctx)
    print("\nAI INCIDENT ANALYSIS\n"+"="*60)
    print(analyze(ctx))
if __name__=="__main__": main()
