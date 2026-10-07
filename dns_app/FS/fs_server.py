import socket
from flask import Flask, request, jsonify

app = Flask(__name__)


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


@app.route("/register", methods=["PUT"])
def register():
    body = request.get_json(silent=True) or {}
    hostname, ip = body.get("hostname"), body.get("ip")
    as_ip, as_port = body.get("as_ip"), body.get("as_port")
    if not all([hostname, ip, as_ip, as_port]):
        return "missing fields", 400
    msg = f"TYPE=A\nNAME={hostname} VALUE={ip} TTL=10\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)
    try:
        sock.sendto(msg.encode(), (as_ip, int(as_port)))
        sock.recvfrom(2048)
    except (socket.timeout, OSError, ValueError):
        return "registration with AS failed", 500
    finally:
        sock.close()
    return "registered", 201


@app.route("/fibonacci", methods=["GET"])
def fibonacci():
    try:
        x = int(request.args.get("number", ""))
        if x < 0:
            raise ValueError
    except ValueError:
        return "bad format", 400
    return jsonify(number=x, fibonacci=fib(x)), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)
