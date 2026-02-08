import time
import uuid


class TraceCollector:

    def __init__(self):
        self.traces = {}

    def start_trace(self):

        trace_id = str(uuid.uuid4())

        self.traces[trace_id] = {
            "start_time": time.time(),
            "stages": {},
            "metadata": {}
        }

        return trace_id

    def record_stage(self, trace_id, stage_name, duration):

        if trace_id in self.traces:
            self.traces[trace_id]["stages"][stage_name] = duration

    def add_metadata(self, trace_id, key, value):

        if trace_id in self.traces:
            self.traces[trace_id]["metadata"][key] = value

    def end_trace(self, trace_id):

        if trace_id not in self.traces:
            return None

        trace = self.traces[trace_id]

        trace["total_latency"] = time.time() - trace["start_time"]

        return trace


trace_collector = TraceCollector()
