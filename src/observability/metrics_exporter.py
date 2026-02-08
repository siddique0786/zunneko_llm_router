import json
from datetime import datetime
from src.metrics.store import metrics_data


def export_metrics_snapshot():
    """
    Exports current in-memory metrics into snapshot JSON file
    """

    snapshot = {
        "timestamp": datetime.utcnow().isoformat(),
        "metrics": metrics_data
    }

    with open("metrics_snapshot.json", "w") as f:
        json.dump(snapshot, f, indent=4)

    return snapshot
