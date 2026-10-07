import json, os, socket

PORT = 53533
DB = os.environ.get("AS_DB", "/data/dns_records.json")


def parse(msg):
    rec = {}
    for tok in msg.split():
        if "=" in tok:
            k, v = tok.split("=", 1)
            rec[k.strip().upper()] = v.strip()
    return rec


def load():
    try:
        with open(DB) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save(db):
    os.makedirs(os.path.dirname(DB) or ".", exist_ok=True)
    with open(DB, "w") as f:
        json.dump(db, f)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", PORT))
    while True:
        data, addr = sock.recvfrom(2048)
        rec = parse(data.decode())
        rtype, name = rec.get("TYPE", "A"), rec.get("NAME")
        if not name:
            continue
        db = load()
        if "VALUE" in rec:
            db[f"{name}|{rtype}"] = {"value": rec["VALUE"], "ttl": rec.get("TTL", "10")}
            save(db)
            reply = f"TYPE={rtype}\nNAME={name} VALUE={rec['VALUE']} TTL={rec.get('TTL', '10')}\n"
        else:
            entry = db.get(f"{name}|{rtype}")
            if not entry:
                reply = f"TYPE={rtype}\nNAME={name} VALUE= TTL=0\n"
            else:
                reply = f"TYPE={rtype}\nNAME={name} VALUE={entry['value']} TTL={entry['ttl']}\n"
        sock.sendto(reply.encode(), addr)


if __name__ == "__main__":
    main()
