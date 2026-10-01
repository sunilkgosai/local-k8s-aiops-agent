import json
from config import K8S_NAMESPACE as n
import prometheus_tools as p
print(json.dumps({"cpu":p.cpu(n),"memory":p.memory(n),"restarts":p.restarts(n),"not_ready":p.not_ready(n)},indent=2))
