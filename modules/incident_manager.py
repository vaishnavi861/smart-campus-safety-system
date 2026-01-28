import json
import os
import datetime
import uuid

INCIDENT_DB_PATH = 'data/incidents.json'

VALID_STATUS_TRANSITIONS = {
    'Reported': ['Inspected', 'Acknowledged'],
    'Triggered': ['Acknowledged'],
    'Acknowledged': ['Action Taken', 'Action Assigned'],
    'Action Assigned': ['Area Secured'],
    'Action Taken': ['Resolved'],
    'Area Secured': ['Resolved'],
    'Resolved': [] # Terminal state
}

class IncidentManager:
    def __init__(self):
        self._load_db()

    def _load_db(self):
        if not os.path.exists(INCIDENT_DB_PATH):
            self.incidents = []
            self._save_db()
        else:
            try:
                with open(INCIDENT_DB_PATH, 'r') as f:
                    self.incidents = json.load(f)
            except json.JSONDecodeError:
                self.incidents = []

    def _save_db(self):
        with open(INCIDENT_DB_PATH, 'w') as f:
            json.dump(self.incidents, f, indent=4)

    def trigger_emergency(self, location="Unknown Location"):
        incident_id = str(uuid.uuid4())[:8]
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        new_incident = {
            "id": incident_id,
            "type": "EMERGENCY ALERT",
            "location": location,
            "severity": "High",
            "description": "Emergency Alert Triggered by User. Immediate Attention Required.",
            "reporter": "System Alert",
            "status": "Triggered",
            "assigned_to": "All",
            "timestamp": timestamp,
            "history": [
                {
                    "status": "Triggered",
                    "timestamp": timestamp,
                    "note": "Emergency alert button pressed."
                }
            ]
        }
        
        # Prepend to ensure it appears first
        self.incidents.insert(0, new_incident)
        self._save_db()
        return incident_id

    def report_incident(self, incident_type, location, severity, description, reporter="Anonymous"):
        incident_id = str(uuid.uuid4())[:8]
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        new_incident = {
            "id": incident_id,
            "type": incident_type,
            "location": location,
            "severity": severity,
            "description": description,
            "reporter": reporter,
            "status": "Reported",
            "assigned_to": None,
            "timestamp": timestamp,
            "history": [
                {
                    "status": "Reported",
                    "timestamp": timestamp,
                    "note": "Incident reported."
                }
            ]
        }
        
        self.incidents.append(new_incident)
        self._save_db()
        return incident_id

    def get_all_incidents(self):
        return self.incidents

    def get_incident(self, incident_id):
        for inc in self.incidents:
            if inc['id'] == incident_id:
                return inc
        return None

    def update_status(self, incident_id, new_status, note="", assigned_to=None):
        incident = self.get_incident(incident_id)
        if not incident:
            return False, "Incident not found."

        current_status = incident['status']
        if new_status not in VALID_STATUS_TRANSITIONS.get(current_status, []) and new_status != current_status:
             # Admin override or force update logic could go here, but sticking to strict flow for now
             # unless it's just updating info without changing status
             if new_status != current_status:
                return False, f"Invalid transition from {current_status} to {new_status}."

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        incident['status'] = new_status
        if assigned_to:
            incident['assigned_to'] = assigned_to
            
        incident['history'].append({
            "status": new_status,
            "timestamp": timestamp,
            "note": note,
            "updated_by": assigned_to or "System"
        })
        
        self._save_db()
        return True, "Status updated successfully."

    def get_stats(self):
        stats = {
            "Total": len(self.incidents),
            "Reported": 0,
            "Resolved": 0,
            "High Severity": 0
        }
        for inc in self.incidents:
            if inc['status'] == 'Reported': stats['Reported'] += 1
            if inc['status'] == 'Resolved': stats['Resolved'] += 1
            if inc['severity'] == 'High': stats['High Severity'] += 1
            
        return stats
