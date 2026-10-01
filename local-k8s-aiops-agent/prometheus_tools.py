import requests
from config import PROMETHEUS_URL
def query(q):
    r=requests.get(PROMETHEUS_URL+"/api/v1/query",params={"query":q},timeout=15)
    r.raise_for_status(); p=r.json()
    if p.get("status")!="success": raise RuntimeError(p)
    return p["data"]["result"]
def cpu(ns):
    return query(f'sum by (namespace,pod) (rate(container_cpu_usage_seconds_total{{namespace="{ns}",container!="",container!="POD"}}[5m]))')
def memory(ns):
    return query(f'sum by (namespace,pod) (container_memory_working_set_bytes{{namespace="{ns}",container!="",container!="POD"}})')
def restarts(ns):
    return query(f'kube_pod_container_status_restarts_total{{namespace="{ns}"}}')
def not_ready(ns):
    return query(f'kube_pod_status_ready{{namespace="{ns}",condition="false"}} == 1')
