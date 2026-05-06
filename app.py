from flask import Flask, render_template, jsonify
import psutil
import datetime
import os

app = Flask(__name__)

def get_system_stats():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot_time

    return {
        "cpu_percent": cpu,
        "cpu_cores": psutil.cpu_count(),
        "memory_total": round(memory.total / (1024**3), 2),
        "memory_used": round(memory.used / (1024**3), 2),
        "memory_percent": memory.percent,
        "disk_total": round(disk.total / (1024**3), 2),
        "disk_used": round(disk.used / (1024**3), 2),
        "disk_percent": disk.percent,
        "net_sent": round(net.bytes_sent / (1024**2), 2),
        "net_recv": round(net.bytes_recv / (1024**2), 2),
        "uptime": str(uptime).split('.')[0],
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
    }

@app.route('/')
def index():
    stats = get_system_stats()
    return render_template('index.html', stats=stats)

@app.route('/api/stats')
def api_stats():
    return jsonify(get_system_stats())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
