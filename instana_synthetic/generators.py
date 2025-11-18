import json
import random
import time
from datetime import datetime, timedelta

def now_ms():
    return int(time.time() * 1000)

def rand_timeframe(minutes=15):
    to = now_ms()
    window = minutes * 60 * 1000
    return {"to": to, "window_size": window}

def gen_issue(entity_id, severity_dist=(0,1,2,3,4)):
    sev = random.choices(severity_dist, weights=[50,25,15,7,3])[0]
    return {
        "id": f"ISS-{random.randint(100000,999999)}",
        "entity_id": entity_id,
        "severity": sev,
        "start": now_ms() - random.randint(1, 30) * 60_000,
        "end": None if random.random() < 0.7 else now_ms(),
        "problem_text": random.choice([
            "Elevated latency", "Error rate spike", "CPU saturation",
            "GC pauses", "Network jitter"
        ])
    }

def gen_entity(i):
    eid = f"srv-{15284626 + i}"
    return {
        "entity_health_info": {
            "max_severity": round(random.random(), 2),
            "open_issues": [gen_issue(eid) for _ in range(random.randint(0,2))]
        },
        "label": random.choice(["checkout-service","search-service","user-service","payment-service"]),
        "entity_id": eid,
        "entity_type": random.choice(["Service","Host","Container","MobileApp"]),
        "plugin": random.choice(["java","nodejs","python","go","kubernetes"]),
        "snapshot_id": f"snap-{random.randint(10**12, 10**13-1)}",
        "tags": random.sample(["env:prod","env:staging","team:core","team:payments","region:apac","region:us"], k=2),
        "metrics": {
            "p95_latency_ms": random.randint(80, 1200),
            "error_rate": round(random.uniform(0.0, 0.05), 3),
            "req_per_min": random.randint(50, 2000)
        },
        "time": now_ms()
    }

def gen_timeseries(entity_id, metric="latency_p95_ms", minutes=60, step=60_000):
    to = now_ms()
    frm = to - minutes * 60_000
    points = []
    val = random.randint(200, 400)
    for t in range(frm, to, step):
        # random walk + spikes
        val += random.randint(-20, 25)
        if random.random() < 0.05:
            val += random.randint(150, 600)
        points.append({"timestamp": t, "value": max(50, val)})
    return {
        "entity_id": entity_id,
        "metric_name": metric,
        "aggregation": "p95",
        "timeframe": {"from": frm, "to": to, "step_ms": step},
        "points": points
    }

def gen_application(i):
    aid = f"app-{random.randint(100000,999999)}"
    return {
        "application_id": aid,
        "name": random.choice(["E-commerce App","Search Engine","User Portal","Payment Gateway"]),
        "services": [f"srv-{random.randint(10000000,99999999)}" for _ in range(random.randint(2,5))],
        "health": random.choice(["healthy","warning","critical"]),
        "tags": random.sample(["env:prod","env:staging","team:core","team:payments"], k=2),
        "metrics": {
            "total_requests": random.randint(1000, 10000),
            "error_rate": round(random.uniform(0.0, 0.1), 3),
            "avg_response_time_ms": random.randint(100, 500)
        }
    }

def gen_endpoint(i):
    eid = f"ep-{random.randint(100000,999999)}"
    return {
        "endpoint_id": eid,
        "path": random.choice(["/api/checkout","/api/search","/api/user","/api/payment"]),
        "method": random.choice(["GET","POST","PUT","DELETE"]),
        "service_id": f"srv-{random.randint(10000000,99999999)}",
        "metrics": {
            "calls_per_min": random.randint(10, 500),
            "avg_latency_ms": random.randint(50, 1000),
            "error_rate": round(random.uniform(0.0, 0.05), 3)
        }
    }

def gen_issue_record(i, entity_ids=None):
    iid = f"ISS-{random.randint(100000,999999)}"
    entity_id = random.choice(entity_ids) if entity_ids else f"srv-{random.randint(10000000,99999999)}"
    return {
        "issue_id": iid,
        "entity_id": entity_id,
        "severity": random.choice([1,2,3,4,5]),
        "state": random.choice(["open","resolved","acknowledged"]),
        "start_time": now_ms() - random.randint(0, 86400000),  # up to 1 day ago
        "end_time": None if random.random() < 0.5 else now_ms(),
        "problem": random.choice(["High CPU","Memory Leak","Slow Queries","Network Timeout"]),
        "tags": random.sample(["env:prod","env:staging","team:core","team:payments"], k=2)
    }

def gen_topology(entity_ids, is_infra=True):
    nodes = [{"id": eid, "label": f"Node-{eid}", "type": random.choice(["Service","Host","Container"]) if is_infra else "Application"} for eid in random.sample(entity_ids, k=min(20, len(entity_ids)))]
    edges = []
    for i in range(len(nodes)-1):
        edges.append({"from": nodes[i]["id"], "to": nodes[i+1]["id"], "weight": random.randint(1,10), "timestamp": now_ms()})
    return {
        "nodes": nodes,
        "edges": edges,
        "timestamp": now_ms()
    }

def gen_alert_config(entity_ids, config_type="app"):
    if config_type == "app":
        return {
            "alert_id": f"ALERT-{random.randint(100000,999999)}",
            "name": "Application Latency Alert",
            "entity_id": random.choice(entity_ids),
            "rule": {"metric": "latency_p95_ms", "operator": ">", "threshold": 500},
            "severity": random.choice([1,2,3,4,5]),
            "enabled": True,
            "notification_channels": ["email", "slack"]
        }
    elif config_type == "infra":
        return {
            "alert_id": f"ALERT-{random.randint(100000,999999)}",
            "name": "Infrastructure CPU Alert",
            "entity_id": random.choice(entity_ids),
            "rule": {"metric": "cpu_usage", "operator": ">", "threshold": 80},
            "severity": random.choice([1,2,3,4,5]),
            "enabled": True,
            "notification_channels": ["email"]
        }
    else:  # synthetic
        return {
            "alert_id": f"ALERT-{random.randint(100000,999999)}",
            "name": "Synthetic Check Failure",
            "check_id": f"CHK-{random.randint(100000,999999)}",
            "rule": {"failure_count": 3, "window_minutes": 5},
            "severity": random.choice([1,2,3,4,5]),
            "enabled": True,
            "notification_channels": ["webhook"]
        }

def gen_metrics_catalog():
    metrics = [
        {"name": "latency_p95_ms", "unit": "ms", "aggregation": "p95", "description": "95th percentile latency"},
        {"name": "error_rate", "unit": "%", "aggregation": "avg", "description": "Error rate percentage"},
        {"name": "cpu_usage", "unit": "%", "aggregation": "avg", "description": "CPU usage"},
        {"name": "memory_usage", "unit": "%", "aggregation": "avg", "description": "Memory usage"},
        {"name": "req_per_min", "unit": "req/min", "aggregation": "sum", "description": "Requests per minute"}
    ]
    return {"metrics": metrics}

def gen_entity_types():
    types = [
        {"type": "Service", "description": "Application service entity"},
        {"type": "Host", "description": "Infrastructure host"},
        {"type": "Container", "description": "Containerized entity"},
        {"type": "MobileApp", "description": "Mobile application"},
        {"type": "Website", "description": "Website monitoring"}
    ]
    return {"entity_types": types}

def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
