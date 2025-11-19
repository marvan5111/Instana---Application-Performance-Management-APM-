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
