import json
from config import K8S_NAMESPACE as n
import kubernetes_tools as k
print(json.dumps({"pods":k.get_pods(n),"services":k.get_services(n),"endpoints":k.get_endpoints(n),"events":k.get_events(n)},indent=2))
