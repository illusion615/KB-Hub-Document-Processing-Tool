import logging

def setup_logging(status_label=None):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    if status_label:
        handler = StatusBarHandler(status_label)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(handler)

class StatusBarHandler(logging.Handler):
    def __init__(self, status_label):
        super().__init__()
        self.status_label = status_label

    def emit(self, record):
        msg = self.format(record)
        self.status_label.setText(msg)