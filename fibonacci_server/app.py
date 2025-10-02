from flask import Flask, request, jsonify
import socket

app = Flask(__name__)


def fib(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for i in range(2, n + 1):
        a, b = b, a + b
    return b

@app.route("/register", methods=["PUT"])
def register():
    data = request.get_json()
    hostname = data["hostname"]
    ip = data["ip"]
    as_ip = data["as_ip"]
    as_port = int(data["as_port"])

    message = f"TYPE=A\nNAME={hostname} VALUE={ip} TTL=10\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (as_ip, as_port))
    sock.close()

    return jsonify({"status": "registered", "hostname": hostname, "ip": ip}), 201

@app.route("/fibonacci")
def fibonacci():
    number = request.args.get("number")
    if number is None:
        return jsonify({"error": "missing number"}), 400
    try:
        n = int(number)
    except:
        return jsonify({"error": "not an integer"}), 400
    return jsonify({"n": n, "value": fib(n)}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)