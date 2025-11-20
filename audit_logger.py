import json
import time
from datetime import datetime
from typing import Dict, List, Optional

class AuditLogger:
    """Audit logging system for tracking user actions and configuration changes."""

    def __init__(self, log_file: str = "data/audit_log.jsonl"):
        self.log_file = log_file

    def log_action(self, user_id: str, action: str, resource_type: str,
                   resource_id: str, details: Optional[Dict] = None,
                   tenant_id: Optional[str] = None) -> None:
        """Log a user action for audit purposes."""
        audit_entry = {
            "timestamp": int(time.time() * 1000),
            "user_id": user_id,
            "tenant_id": tenant_id,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "details": details or {},
            "ip_address": "127.0.0.1",  # Would be populated from request in real implementation
            "user_agent": "Dashboard/1.7.0"
        }

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(audit_entry) + '\n')
        except Exception as e:
            print(f"Failed to write audit log: {e}")

    def get_audit_trail(self, user_id: Optional[str] = None,
                       tenant_id: Optional[str] = None,
                       limit: int = 100) -> List[Dict]:
        """Retrieve audit trail with optional filtering."""
        audit_trail = []
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    entry = json.loads(line.strip())
                    if user_id and entry['user_id'] != user_id:
                        continue
                    if tenant_id and entry.get('tenant_id') != tenant_id:
                        continue
                    audit_trail.append(entry)
                    if len(audit_trail) >= limit:
                        break
        except FileNotFoundError:
            pass
        return audit_trail

# Global audit logger instance
audit_logger = AuditLogger()
