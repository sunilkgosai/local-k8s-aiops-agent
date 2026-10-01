from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from config import LOG_TAIL_LINES

def core():
    config.load_kube_config()
    return client.CoreV1Api()

def get_pods(ns):
    v=core(); out=[]
    for p in v.list_namespaced_pod(ns).items:
        cs=[]
        for s in p.status.container_statuses or []:
            last=s.last_state.terminated.reason if s.last_state and s.last_state.terminated else None
            waiting=s.state.waiting.reason if s.state and s.state.waiting else None
            cs.append({"name":s.name,"ready":s.ready,"restarts":s.restart_count,
                       "waiting_reason":waiting,"last_termination_reason":last})
        out.append({"name":p.metadata.name,"phase":p.status.phase,"pod_ip":p.status.pod_ip,
                    "node":p.spec.node_name,"containers":cs})
    return out

def get_events(ns):
    v=core()
    return [{"type":e.type,"reason":e.reason,"message":e.message,
             "object":e.involved_object.name} for e in v.list_namespaced_event(ns).items]

def get_services(ns):
    v=core()
    return [{"name":s.metadata.name,"type":s.spec.type,"cluster_ip":s.spec.cluster_ip,
             "selector":s.spec.selector} for s in v.list_namespaced_service(ns).items]

def get_endpoints(ns):
    v=core(); out=[]
    for e in v.list_namespaced_endpoints(ns).items:
        ready=[]; not_ready=[]
        for sub in e.subsets or []:
            ready += [a.ip for a in (sub.addresses or [])]
            not_ready += [a.ip for a in (sub.not_ready_addresses or [])]
        out.append({"name":e.metadata.name,"ready":ready,"not_ready":not_ready})
    return out

def get_logs(ns):
    v=core(); out=[]
    for p in v.list_namespaced_pod(ns).items:
        for c in p.spec.containers:
            item={"pod":p.metadata.name,"container":c.name}
            try:
                item["current"]=v.read_namespaced_pod_log(p.metadata.name,ns,container=c.name,
                    tail_lines=LOG_TAIL_LINES,timestamps=True)
            except ApiException as x: item["current"]="Unavailable: "+x.reason
            try:
                item["previous"]=v.read_namespaced_pod_log(p.metadata.name,ns,container=c.name,
                    previous=True,tail_lines=LOG_TAIL_LINES,timestamps=True)
            except ApiException: item["previous"]=None
            out.append(item)
    return out
