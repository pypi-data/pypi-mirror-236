import logging
import queue
import threading
import time
from datetime import datetime

from elasticsearch import Elasticsearch


class ElasticsearchHandler(logging.Handler):
    def __init__(self, es: Elasticsearch, application_name: str, index_prefix: str):
        super().__init__()
        self.index_prefix = index_prefix
        self.application_name = application_name
        self.es = es
        self._logs_queue = queue.Queue()
        threading.Thread(target=self._start_send_events).start()

    def emit(self, record):
        try:
            date = datetime.utcnow()
            index = f"{self.index_prefix}-{date.strftime('%Y.%m.%d')}"
            level = self.log_levels[record.levelname]
            log_data = {
                "@timestamp": date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                "level": level,
                "ApplicationName": self.application_name,
                "message": record.getMessage(),
            }
            self._logs_queue.put((index, log_data))
        except Exception as ex:
            print(f"Can' t send elastic log.  Ex: {ex}")

    log_levels = {
        "DEBUG": "Debug",
        "INFO": "Information",
        "WARNING": "Warning",
        "ERROR": "Error",
        "CRITICAL": "Fatal"
    }

    def _start_send_events(self):
        while True:
            try:
                if self._logs_queue.empty():
                    time.sleep(2)
                    continue
                try:
                    log = self._logs_queue.get()
                    self.es.index(index=log[0], body=log[1])
                except Exception as ex:
                    print(f"Can' t send elastic log.  Ex: {ex}")
                    self._logs_queue.put(log)
            except Exception as ex:
                print(ex)
