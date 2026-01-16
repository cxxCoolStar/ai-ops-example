import structlog
import time
import threading
from flask import Flask, request, jsonify

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

log = structlog.get_logger()
app = Flask(__name__)

def parse_int(s: str) -> int:
    """Parse a string to integer."""
    return int(s)

def divide(a: str, b: str) -> float:
    """Divide two numbers provided as strings."""
    return parse_int(a) / parse_int(b)

def do_work(event_id: str, request_id: str):
    """Simulate work processing with error handling."""
    log.info("work.start", event_id=event_id, request_id=request_id)
    try:
        # Simulate work
        divide("1", "0")
        log.info("work.ok", event_id=event_id, request_id=request_id)
    except ZeroDivisionError as e:
        log.error("work.failed", event_id=event_id, request_id=request_id, error=str(e))
        raise
    finally:
        log.info("work.end", event_id=event_id, request_id=request_id)

def ticker():
    """Background thread that triggers work every 5 seconds."""
    while True:
        event_id = str(uuid.uuid4())
        request_id = str(uuid.uuid4())
        try:
            do_work(event_id, request_id)
        except ZeroDivisionError:
            pass  # Error already logged
        time.sleep(5)

@app.route('/process', methods=['POST'])
def process():
    """HTTP endpoint to trigger work processing."""
    event_id = str(uuid.uuid4())
    request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
    
    try:
        do_work(event_id, request_id)
        return jsonify({"status": "ok", "event_id": event_id}), 200
    except ZeroDivisionError:
        return jsonify({"status": "error", "event_id": event_id, "error": "division by zero"}), 500

if __name__ == '__main__':
    # Start background ticker thread
    ticker_thread = threading.Thread(target=ticker, daemon=True)
    ticker_thread.start()
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000)