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

# Website Monitoring Generators
def gen_website_config(i):
    return {
        "website_id": f"web-{random.randint(100000,999999)}",
        "url": random.choice([
            "https://example.com",
            "https://api.example.com/health",
            "https://checkout.example.com",
            "https://search.example.com"
        ]),
        "check_interval_seconds": random.choice([30, 60, 120, 300]),
        "timeout_ms": random.randint(5000, 15000),
        "expected_status_codes": [200, 201, 202],
        "alert_on_failure": random.choice([True, False]),
        "tags": random.sample(["env:prod", "env:staging", "region:us", "region:eu"], k=2)
    }

def gen_website_catalog():
    websites = [
        {
            "website_id": f"web-{random.randint(100000,999999)}",
            "name": "Example Homepage",
            "url": "https://example.com",
            "description": "Main website homepage",
            "tags": ["env:prod", "type:homepage"]
        },
        {
            "website_id": f"web-{random.randint(100000,999999)}",
            "name": "API Health Check",
            "url": "https://api.example.com/health",
            "description": "API health endpoint",
            "tags": ["env:prod", "type:api"]
        }
    ]
    return {"websites": websites}

def gen_website_metrics(website_id, minutes=60):
    to = now_ms()
    frm = to - minutes * 60_000
    points = []
    val = random.randint(200, 500)  # response time ms
    for t in range(frm, to, 60_000):  # every minute
        val += random.randint(-50, 100)
        if random.random() < 0.1:  # occasional spikes
            val += random.randint(500, 2000)
        points.append({"timestamp": t, "value": max(100, val)})
    return {
        "website_id": website_id,
        "metric_name": "response_time_ms",
        "aggregation": "avg",
        "timeframe": {"from": frm, "to": to, "step_ms": 60000},
        "points": points
    }

def gen_website_analyze(website_id):
    return {
        "website_id": website_id,
        "snapshot_id": f"snap-{random.randint(10**12, 10**13-1)}",
        "timestamp": now_ms(),
        "response_time_ms": random.randint(150, 2000),
        "status_code": random.choice([200, 201, 404, 500]),
        "error_message": None if random.random() < 0.8 else "Connection timeout",
        "page_views": random.randint(1000, 10000),
        "unique_visitors": random.randint(500, 5000),
        "availability": round(random.uniform(0.95, 1.0), 3),
        "issues": [gen_issue(website_id) for _ in range(random.randint(0, 2))]
    }

# Logging Generators
def gen_log_entry(entity_ids=None):
    entity_id = random.choice(entity_ids) if entity_ids else f"srv-{random.randint(10000000,99999999)}"
    severity_levels = ["DEBUG", "INFO", "WARN", "ERROR", "FATAL"]
    severity = random.choices(severity_levels, weights=[40, 30, 20, 8, 2])[0]
    return {
        "timestamp": now_ms() - random.randint(0, 86400000),  # up to 1 day ago
        "severity": severity,
        "message": random.choice([
            "Request processed successfully",
            "Database connection established",
            "High memory usage detected",
            "Failed to connect to external service",
            "User authentication failed"
        ]),
        "entity_id": entity_id,
        "correlation_id": f"corr-{random.randint(100000,999999)}",
        "tags": random.sample(["env:prod", "env:staging", "team:core", "team:payments"], k=2),
        "source": random.choice(["application", "infrastructure", "web"])
    }

# Synthetic Checks Generators
def gen_synthetic_check(endpoint_ids=None):
    endpoint_id = random.choice(endpoint_ids) if endpoint_ids else f"ep-{random.randint(100000,999999)}"
    return {
        "check_id": f"chk-{random.randint(100000,999999)}",
        "name": f"Synthetic Check for {endpoint_id}",
        "type": random.choice(["api", "browser"]),
        "endpoint_id": endpoint_id,
        "url": random.choice([
            "https://api.example.com/checkout",
            "https://api.example.com/search",
            "https://api.example.com/user"
        ]),
        "method": random.choice(["GET", "POST"]),
        "headers": {"Authorization": "Bearer token", "Content-Type": "application/json"},
        "body": None if random.random() < 0.7 else '{"test": "data"}',
        "expected_status": 200,
        "timeout_ms": random.randint(5000, 10000),
        "frequency_seconds": random.choice([60, 300, 600]),
        "locations": random.sample(["us-east", "us-west", "eu-central", "ap-southeast"], k=2)
    }

def gen_synthetic_run(check_id):
    success = random.random() < 0.9  # 90% success rate
    return {
        "run_id": f"run-{random.randint(100000,999999)}",
        "check_id": check_id,
        "timestamp": now_ms() - random.randint(0, 3600000),  # up to 1 hour ago
        "duration_ms": random.randint(100, 5000),
        "status": "success" if success else "failure",
        "status_code": 200 if success else random.choice([404, 500, 502]),
        "error_message": None if success else "Connection refused",
        "location": random.choice(["us-east", "us-west", "eu-central", "ap-southeast"]),
        "response_size_bytes": random.randint(100, 10000) if success else 0
    }

# Mobile Monitoring Generators
def gen_mobile_config(i):
    platforms = ["iOS", "Android"]
    platform = random.choice(platforms)
    config = {
        "mobile_app_id": f"mobile-{random.randint(100000,999999)}",
        "platform": platform,
        "version": f"{random.randint(1,5)}.{random.randint(0,9)}.{random.randint(0,9)}",
        "check_interval_seconds": random.choice([300, 600, 900]),
        "crash_threshold": round(random.uniform(0.01, 0.1), 3),
        "response_time_threshold_ms": random.randint(1000, 5000),
        "alert_on_crash": random.choice([True, False]),
        "tags": random.sample(["env:prod", "env:staging", "platform:" + platform.lower(), "region:us", "region:eu"], k=2)
    }
    if platform == "iOS":
        config["bundle_id"] = f"com.example.app{random.randint(1,100)}"
    else:
        config["package_name"] = f"com.example.app{random.randint(1,100)}"
    return config

def gen_mobile_catalog():
    apps = [
        {
            "mobile_app_id": f"mobile-{random.randint(100000,999999)}",
            "name": "E-commerce Mobile App",
            "platform": "iOS",
            "description": "Main mobile app for e-commerce",
            "tags": ["env:prod", "platform:ios"]
        },
        {
            "mobile_app_id": f"mobile-{random.randint(100000,999999)}",
            "name": "E-commerce Android App",
            "platform": "Android",
            "description": "Android version of e-commerce app",
            "tags": ["env:prod", "platform:android"]
        }
    ]
    return {"mobile_apps": apps}

def gen_mobile_metrics(mobile_app_id, minutes=60):
    to = now_ms()
    frm = to - minutes * 60_000
    points = []
    crash_rate = random.uniform(0.001, 0.05)  # crash rate
    response_time = random.randint(500, 3000)  # ms
    for t in range(frm, to, 60_000):  # every minute
        crash_rate += random.uniform(-0.005, 0.01)
        crash_rate = max(0.0001, min(0.1, crash_rate))
        response_time += random.randint(-200, 400)
        response_time = max(100, response_time)
        points.append({"timestamp": t, "crash_rate": round(crash_rate, 4), "response_time_ms": response_time})
    return {
        "mobile_app_id": mobile_app_id,
        "metric_name": "mobile_performance",
        "aggregation": "avg",
        "timeframe": {"from": frm, "to": to, "step_ms": 60000},
        "points": points
    }

def gen_mobile_analyze(mobile_app_id):
    return {
        "mobile_app_id": mobile_app_id,
        "snapshot_id": f"snap-{random.randint(10**12, 10**13-1)}",
        "timestamp": now_ms(),
        "platform": random.choice(["iOS", "Android"]),
        "version": f"{random.randint(1,5)}.{random.randint(0,9)}.{random.randint(0,9)}",
        "crash_count": random.randint(0, 50),
        "crash_rate": round(random.uniform(0.001, 0.05), 4),
        "avg_response_time_ms": random.randint(500, 3000),
        "user_sessions": random.randint(1000, 10000),
        "active_users": random.randint(500, 5000),
        "battery_drain_percent": round(random.uniform(1.0, 10.0), 2),
        "memory_usage_mb": random.randint(50, 500),
        "issues": [gen_issue(mobile_app_id) for _ in range(random.randint(0, 2))]
    }

# Infrastructure Monitoring Generators (v1.4.0)
def gen_infrastructure_entity(entity_type):
    entity_id = f"{entity_type}-{random.randint(100000,999999)}"
    base_entity = {
        "entity_id": entity_id,
        "entity_type": entity_type,
        "label": f"{entity_type.capitalize()}-{random.randint(1000,9999)}",
        "tags": random.sample(["env:prod", "env:staging", "region:us-east", "region:eu-west", "team:infra", "team:platform"], k=2),
        "snapshot_id": f"snap-{random.randint(10**12, 10**13-1)}",
        "time": now_ms()
    }

    if entity_type == "host":
        base_entity.update({
            "cpu_cores": random.randint(2, 64),
            "memory_gb": random.randint(4, 256),
            "disk_gb": random.randint(50, 2000),
            "os": random.choice(["Linux", "Windows", "macOS"]),
            "hostname": f"host-{random.randint(1000,9999)}.example.com",
            "ip_address": f"192.168.{random.randint(1,255)}.{random.randint(1,255)}"
        })
    elif entity_type == "container":
        base_entity.update({
            "image": f"nginx:{random.randint(1,2)}.{random.randint(0,20)}",
            "cpu_limit": round(random.uniform(0.1, 4.0), 1),
            "memory_limit_mb": random.randint(128, 4096),
            "host_id": f"host-{random.randint(100000,999999)}",
            "namespace": random.choice(["default", "kube-system", "production", "staging"])
        })
    elif entity_type == "process":
        base_entity.update({
            "pid": random.randint(1, 65535),
            "command": random.choice(["nginx", "java -jar app.jar", "python app.py", "node server.js"]),
            "user": random.choice(["root", "www-data", "appuser"]),
            "host_id": f"host-{random.randint(100000,999999)}",
            "container_id": f"container-{random.randint(100000,999999)}" if random.random() < 0.7 else None
        })

    return base_entity

def gen_infrastructure_metrics(entity_id, metric_name, minutes=60):
    to = now_ms()
    frm = to - minutes * 60_000
    points = []
    val = 0

    if "cpu" in metric_name:
        val = random.uniform(5, 30)  # CPU usage %
    elif "memory" in metric_name:
        val = random.uniform(40, 80)  # Memory usage %
    elif "network" in metric_name:
        val = random.uniform(1, 100)  # Network Mbps
    elif "disk" in metric_name:
        val = random.uniform(20, 90)  # Disk usage %

    for t in range(frm, to, 60_000):  # every minute
        val += random.uniform(-5, 5)
        val = max(0, min(100, val))  # clamp to 0-100
        points.append({"timestamp": t, "value": round(val, 2)})

    return {
        "entity_id": entity_id,
        "metric_name": metric_name,
        "aggregation": "avg",
        "timeframe": {"from": frm, "to": to, "step_ms": 60000},
        "points": points
    }

def gen_infra_topology(entity_ids=None):
    if not entity_ids:
        entity_ids = [f"host-{random.randint(100000,999999)}" for _ in range(10)] + \
                     [f"container-{random.randint(100000,999999)}" for _ in range(20)] + \
                     [f"process-{random.randint(100000,999999)}" for _ in range(30)]

    nodes = []
    edges = []

    # Create nodes
    for eid in entity_ids:
        entity_type = eid.split('-')[0]
        nodes.append({
            "id": eid,
            "label": f"{entity_type}-{random.randint(1000,9999)}",
            "type": entity_type,
            "group": "infrastructure"
        })

    # Create edges (host -> container -> process relationships)
    hosts = [n for n in nodes if n["type"] == "host"]
    containers = [n for n in nodes if n["type"] == "container"]
    processes = [n for n in nodes if n["type"] == "process"]

    for container in containers:
        host = random.choice(hosts)
        edges.append({
            "from": host["id"],
            "to": container["id"],
            "type": "hosts",
            "weight": random.randint(1, 10)
        })

    for process in processes:
        if random.random() < 0.7:  # 70% of processes run in containers
            container = random.choice(containers)
            edges.append({
                "from": container["id"],
                "to": process["id"],
                "type": "contains",
                "weight": random.randint(1, 5)
            })
        else:  # direct on host
            host = random.choice(hosts)
            edges.append({
                "from": host["id"],
                "to": process["id"],
                "type": "runs",
                "weight": random.randint(1, 5)
            })

    return {
        "nodes": nodes,
        "edges": edges,
        "timestamp": now_ms(),
        "type": "infrastructure"
    }

# Application Monitoring Generators (v1.4.0)
def gen_application_metrics(app_id, metric_name, minutes=60):
    to = now_ms()
    frm = to - minutes * 60_000
    points = []
    val = 0

    if metric_name == "latency_p95_ms":
        val = random.randint(100, 300)
    elif metric_name == "throughput_rpm":
        val = random.randint(1000, 10000)
    elif metric_name == "apdex_score":
        val = random.uniform(0.7, 0.95)
    elif metric_name == "error_rate_percent":
        val = random.uniform(0.1, 2.0)

    for t in range(frm, to, 60_000):  # every minute
        if metric_name == "latency_p95_ms":
            val += random.randint(-20, 30)
            val = max(50, val)
        elif metric_name == "throughput_rpm":
            val += random.randint(-500, 500)
            val = max(100, val)
        elif metric_name == "apdex_score":
            val += random.uniform(-0.05, 0.05)
            val = max(0.5, min(1.0, val))
        elif metric_name == "error_rate_percent":
            val += random.uniform(-0.5, 0.5)
            val = max(0.0, min(5.0, val))

        points.append({"timestamp": t, "value": round(val, 2) if isinstance(val, float) else val})

    return {
        "application_id": app_id,
        "metric_name": metric_name,
        "aggregation": "p95" if "latency" in metric_name else "avg",
        "timeframe": {"from": frm, "to": to, "step_ms": 60000},
        "points": points
    }

def gen_application_traces(app_id, span_count=5):
    trace_id = f"trace-{random.randint(10**15, 10**16-1)}"
    spans = []

    start_time = now_ms() - random.randint(0, 3600000)  # up to 1 hour ago

    for i in range(span_count):
        span_id = f"span-{random.randint(10**15, 10**16-1)}"
        parent_span_id = spans[-1]["span_id"] if spans else None
        duration = random.randint(10, 500)  # ms

        spans.append({
            "trace_id": trace_id,
            "span_id": span_id,
            "parent_span_id": parent_span_id,
            "name": random.choice(["GET /api/user", "POST /api/order", "GET /api/product", "PUT /api/cart"]),
            "service_name": f"service-{random.randint(1,10)}",
            "start_time": start_time + i * 50,  # sequential
            "duration_ms": duration,
            "tags": {
                "http.method": random.choice(["GET", "POST", "PUT", "DELETE"]),
                "http.status_code": random.choice([200, 201, 400, 404, 500]),
                "error": random.choice([True, False]) if random.random() < 0.1 else False
            }
        })

    return {
        "trace_id": trace_id,
        "application_id": app_id,
        "spans": spans,
        "total_spans": len(spans),
        "duration_ms": sum(s["duration_ms"] for s in spans),
        "start_time": start_time,
        "end_time": start_time + sum(s["duration_ms"] for s in spans)
    }

def gen_app_topology():
    services = [f"service-{i}" for i in range(1, 11)]
    nodes = []
    edges = []

    # Create service nodes
    for svc in services:
        nodes.append({
            "id": svc,
            "label": svc,
            "type": "service",
            "group": "application"
        })

    # Create call relationships
    for i, svc in enumerate(services):
        # Each service calls 1-3 other services
        targets = random.sample([s for s in services if s != svc], k=random.randint(1, 3))
        for target in targets:
            edges.append({
                "from": svc,
                "to": target,
                "type": "calls",
                "weight": random.randint(1, 10),
                "protocol": random.choice(["http", "grpc", "kafka"])
            })

    return {
        "nodes": nodes,
        "edges": edges,
        "timestamp": now_ms(),
        "type": "application"
    }

def gen_app_settings(app_id):
    return {
        "application_id": app_id,
        "rules": [
            {
                "rule_id": f"rule-{random.randint(100000,999999)}",
                "name": "High Latency Rule",
                "condition": "latency_p95_ms > 500",
                "action": "alert",
                "enabled": True
            },
            {
                "rule_id": f"rule-{random.randint(100000,999999)}",
                "name": "Error Rate Rule",
                "condition": "error_rate > 0.05",
                "action": "alert",
                "enabled": True
            }
        ],
        "tags": random.sample(["env:prod", "team:backend", "region:us", "version:v2.1"], k=3),
        "configs": {
            "tracing_enabled": True,
            "metrics_interval_seconds": 60,
            "log_level": random.choice(["INFO", "DEBUG", "WARN"])
        }
    }

# Global & Infra Alert Configurations (v1.4.0)
def gen_global_alert_config():
    return {
        "alert_config_id": f"global-alert-{random.randint(100000,999999)}",
        "name": random.choice(["Global Latency Alert", "Global Error Rate Alert", "Global Throughput Alert"]),
        "scope": "global",
        "rule": {
            "metric": random.choice(["latency_p95_ms", "error_rate", "throughput_rpm"]),
            "operator": random.choice([">", "<", ">=", "<="]),
            "threshold": random.randint(100, 1000),
            "duration_minutes": random.choice([5, 10, 15, 30])
        },
        "severity": random.choice([1, 2, 3, 4, 5]),
        "notification_channels": random.sample(["email", "slack", "webhook", "pagerduty"], k=2),
        "enabled": True,
        "tags": random.sample(["env:prod", "global", "critical"], k=2)
    }

def gen_infra_alert_config():
    return {
        "alert_config_id": f"infra-alert-{random.randint(100000,999999)}",
        "name": random.choice(["High CPU Alert", "Memory Usage Alert", "Disk Space Alert", "Network Alert"]),
        "scope": "infrastructure",
        "entity_type": random.choice(["host", "container", "process"]),
        "rule": {
            "metric": random.choice(["cpu_usage_percent", "memory_usage_percent", "disk_usage_percent", "network_rx_mbps"]),
            "operator": ">",
            "threshold": random.randint(70, 95),
            "duration_minutes": random.choice([5, 10, 15])
        },
        "severity": random.choice([2, 3, 4]),
        "notification_channels": ["email"],
        "enabled": True,
        "tags": random.sample(["infra", "system", "capacity"], k=2)
    }

# Event Settings & Host Agent (v1.4.0)
def gen_event_settings():
    return {
        "event_settings_id": f"event-settings-{random.randint(100000,999999)}",
        "name": "Default Event Ingestion",
        "enabled": True,
        "filters": [
            {
                "filter_id": f"filter-{random.randint(100000,999999)}",
                "type": random.choice(["include", "exclude"]),
                "pattern": random.choice(["*.error", "*.warn", "system.*"]),
                "source": random.choice(["application", "infrastructure", "custom"])
            }
        ],
        "retention_days": random.choice([7, 30, 90]),
        "max_events_per_minute": random.randint(1000, 10000),
        "tags": ["event", "ingestion"]
    }

def gen_host_agent_status():
    return {
        "host_id": f"host-{random.randint(100000,999999)}",
        "agent_version": f"{random.randint(1,2)}.{random.randint(0,9)}.{random.randint(0,9)}",
        "status": random.choice(["connected", "disconnected", "updating"]),
        "last_seen": now_ms() - random.randint(0, 300000),  # up to 5 minutes ago
        "uptime_seconds": random.randint(3600, 604800),  # 1 hour to 1 week
        "cpu_usage_percent": round(random.uniform(1, 10), 2),
        "memory_usage_mb": random.randint(50, 200),
        "config": {
            "tracing_enabled": True,
            "metrics_interval_seconds": 60,
            "log_level": "INFO"
        },
        "plugins": random.sample(["java", "nodejs", "python", "kubernetes", "docker"], k=3)
    }

def gen_events(entity_ids=None, count=10):
    events = []
    for _ in range(count):
        entity_id = random.choice(entity_ids) if entity_ids else f"entity-{random.randint(100000,999999)}"
        events.append({
            "event_id": f"event-{random.randint(100000,999999)}",
            "entity_id": entity_id,
            "timestamp": now_ms() - random.randint(0, 86400000),  # up to 1 day ago
            "type": random.choice(["metric_anomaly", "error_spike", "performance_degradation", "system_alert"]),
            "severity": random.choice([1, 2, 3, 4, 5]),
            "message": random.choice([
                "CPU usage exceeded threshold",
                "Memory leak detected",
                "Response time increased",
                "Error rate spike observed"
            ]),
            "source": random.choice(["agent", "sensor", "rule_engine"]),
            "tags": random.sample(["auto", "critical", "system"], k=2),
            "metadata": {
                "threshold": random.randint(70, 95),
                "current_value": random.randint(80, 100),
                "duration_minutes": random.randint(5, 30)
            }
        })
    return events

# User Management (v1.4.0)
def gen_user_roles():
    roles = ["admin", "viewer", "editor", "operator"]
    users = []

    for _ in range(random.randint(5, 15)):
        role = random.choice(roles)
        users.append({
            "user_id": f"user-{random.randint(100000,999999)}",
            "username": f"user{random.randint(1000,9999)}",
            "email": f"user{random.randint(1000,9999)}@example.com",
            "role": role,
            "permissions": {
                "read": True,
                "write": role in ["admin", "editor", "operator"],
                "delete": role == "admin",
                "admin": role == "admin"
            },
            "last_login": now_ms() - random.randint(0, 604800000),  # up to 1 week ago
            "enabled": True,
            "tags": [role, "active"]
        })

    return {"users": users}

def gen_api_tokens():
    return {
        "token_id": f"token-{random.randint(100000,999999)}",
        "name": f"API Token {random.randint(1,100)}",
        "token": f"instana-{random.randint(10**20, 10**21-1)}",  # fake token
        "created_by": f"user-{random.randint(100000,999999)}",
        "created_at": now_ms() - random.randint(0, 2592000000),  # up to 30 days ago
        "expires_at": now_ms() + random.randint(86400000, 31536000000),  # 1 day to 1 year
        "permissions": random.sample([
            "read:metrics", "read:traces", "read:logs", "write:configs",
            "read:alerts", "write:alerts", "admin"
        ], k=random.randint(2, 5)),
        "enabled": True,
        "last_used": now_ms() - random.randint(0, 86400000)  # up to 1 day ago
    }

def gen_access_catalogs():
    catalogs = []

    for _ in range(random.randint(3, 8)):
        catalogs.append({
            "catalog_id": f"catalog-{random.randint(100000,999999)}",
            "name": random.choice(["Production Access", "Development Access", "Read-Only Access"]),
            "description": "Access control catalog for monitoring entities",
            "rules": [
                {
                    "rule_id": f"rule-{random.randint(100000,999999)}",
                    "resource_type": random.choice(["application", "infrastructure", "website", "mobile"]),
                    "resource_pattern": "*",
                    "permissions": random.sample(["read", "write", "admin"], k=2),
                    "conditions": {
                        "tags": random.sample(["env:prod", "team:backend"], k=1)
                    }
                }
            ],
            "created_at": now_ms() - random.randint(0, 2592000000),
            "updated_at": now_ms() - random.randint(0, 86400000)
        })

    return {"access_catalogs": catalogs}

# Kubernetes Monitoring Generators (v1.6.0)
def gen_kubernetes_pod(i, cluster_id, deployment_id):
    """Generate a synthetic Kubernetes Pod record."""
    status_choices = ["Running", "Pending", "Succeeded", "Failed", "CrashLoopBackOff"]
    status = random.choices(status_choices, weights=[80, 5, 5, 5, 5])[0]
    return {
        "pod_id": f"pod-{random.randint(100000, 999999)}",
        "name": f"app-pod-{i}-{random.randint(1000, 9999)}",
        "cluster_id": cluster_id,
        "deployment_id": deployment_id,
        "namespace": random.choice(["default", "production", "staging", "kube-system"]),
        "status": status,
        "restarts": 0 if status == "Running" else random.randint(1, 10),
        "created_at": now_ms() - random.randint(3600_000, 86400_000), # 1 hour to 1 day ago
        "metrics": {
            "cpu_usage_cores": round(random.uniform(0.1, 2.5), 2),
            "memory_usage_mb": random.randint(128, 2048)
        },
        "labels": {
            "app": "my-app",
            "version": f"v{random.randint(1,3)}.{random.randint(0,9)}"
        }
    }

def gen_kubernetes_cluster(i):
    """Generate a synthetic Kubernetes Cluster record."""
    status_choices = ["Healthy", "Warning", "Critical"]
    return {
        "cluster_id": f"k8s-cluster-{i}",
        "name": f"prod-cluster-{random.choice(['us-east-1', 'eu-west-1', 'ap-southeast-2'])}",
        "region": random.choice(["us-east-1", "eu-west-1", "ap-southeast-2"]),
        "status": random.choices(status_choices, weights=[90, 8, 2])[0],
        "node_count": random.randint(3, 50),
        "metrics": {
            "total_cpu_cores": random.randint(12, 200),
            "total_memory_gb": random.randint(48, 800),
            "cpu_utilization_percent": round(random.uniform(40, 90), 2),
            "memory_utilization_percent": round(random.uniform(50, 85), 2)
        }
    }

def gen_kubernetes_deployment(i, cluster_id):
    """Generate a synthetic Kubernetes Deployment record."""
    replicas = random.randint(2, 10)
    available_replicas = replicas if random.random() > 0.1 else replicas - 1
    return {
        "deployment_id": f"deploy-{random.randint(100000, 999999)}",
        "name": f"app-deployment-{i}",
        "cluster_id": cluster_id,
        "namespace": random.choice(["production", "staging"]),
        "replicas": {
            "desired": replicas,
            "available": available_replicas,
            "unavailable": replicas - available_replicas
        },
        "rollout_status": "Completed" if available_replicas == replicas else "InProgress",
        "image": f"my-app-image:v{random.randint(1,3)}.{random.randint(0,9)}.{random.randint(0,9)}",
        "created_at": now_ms() - random.randint(86400_000, 604800_000), # 1 to 7 days ago
        "labels": {
            "app": "my-app",
            "env": "production"
        }
    }
