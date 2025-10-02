from flask import Flask, request, jsonify
import socket, requests

app = Flask(__name__)

@app.route("/fibonacci")
def fibonacci_handler():

    hostname = request.args.get("hostname")
    fs_port = request.args.get("fs_port")
    number = request.args.get("number")
    as_ip = request.args.get("as_ip")
    as_port = request.args.get("as_port")


    if not all([hostname, fs_port, number, as_ip, as_port]):
        return jsonify({"error": "missing params"}), 400


    try:
        n = int(number)
    except:
        return jsonify({"error": "number not int"}), 400


    msg = f"TYPE=A\nNAME={hostname}\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)
    sock.sendto(msg.encode(), (as_ip, int(as_port)))
    try:
        data, _ = sock.recvfrom(1024)
        text = data.decode()
        if "VALUE=" in text:
            ip = text.split("VALUE=")[1].split()[0]
        else:
            return jsonify({"error": "hostname not found"}), 404
    except:
        return jsonify({"error": "AS timeout"}), 502
    finally:
        sock.close()


    try:
        url = f"http://{ip}:{fs_port}/fibonacci?number={n}"
        r = requests.get(url, timeout=5)
        return r.json(), 200
    except:
        return jsonify({"error": "FS unreachable"}), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)