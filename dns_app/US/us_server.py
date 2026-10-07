import socket
import urllib.request, urllib.error
from flask import Flask, request, Response

app = Flask(__name__)
PARAMS = ["hostname", "fs_port", "number", "as_ip", "as_port"]


def dns_query(name, as_ip, as_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)
    try:
        sock.sendto(f"TYPE=A\nNAME={name}\n".encode(), (as_ip, int(as_port)))
        data, _ = sock.recvfrom(2048)
    finally:
        sock.close()
    for tok in data.decode().split():
        if tok.startswith("VALUE="):
            return tok.split("=", 1)[1] or None
    return None


@app.route("/fibonacci", methods=["GET"])
def fibonacci():
    args = {p: request.args.get(p) for p in PARAMS}
    if any(not v for v in args.values()):
        return "bad request", 400
    try:
        ip = dns_query(args["hostname"], args["as_ip"], args["as_port"])
    except (socket.timeout, OSError, ValueError):
        return "DNS lookup failed", 502
    if not ip:
        return "hostname not found", 404
    url = f"http://{ip}:{args['fs_port']}/fibonacci?number={args['number']}"
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            return Response(r.read(), status=200, mimetype=r.headers.get_content_type())
    except urllib.error.HTTPError as e:
        return Response(e.read(), status=e.code)
    except (urllib.error.URLError, OSError):
        return "Fibonacci server unreachable", 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
