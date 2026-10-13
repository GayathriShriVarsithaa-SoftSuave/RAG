"""
Week 9 - captures the RAW JSON-RPC exchange with a server, bypassing the mcp SDK's parsed
objects entirely (writes/reads the wire format directly) so what lands in wire.json is exactly
what was sent over stdio, not the SDK's Python representation of it.

    python wire_capture.py
"""
import json
import subprocess

SERVER = ["python3", "mcp_servers/claims_server.py"]   # the NEW server (server two)


def send(proc, msg):
    proc.stdin.write(json.dumps(msg) + "\n")
    proc.stdin.flush()
    return msg


def recv(proc):
    return json.loads(proc.stdout.readline())


def main():
    proc = subprocess.Popen(SERVER, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, bufsize=1)
    wire = []

    req = send(proc, {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                      "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                                 "clientInfo": {"name": "wire-capture-client", "version": "0.1"}}})
    wire.append({"direction": "client -> server", "raw": req})
    wire.append({"direction": "server -> client", "raw": recv(proc)})

    notif = send(proc, {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})
    wire.append({"direction": "client -> server (notification, no response expected)", "raw": notif})

    req2 = send(proc, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    wire.append({"direction": "client -> server", "raw": req2})
    wire.append({"direction": "server -> client", "raw": recv(proc)})

    req3 = send(proc, {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                       "params": {"name": "get_claim", "arguments": {"claim_id": "CLM-2026-00004"}}})
    wire.append({"direction": "client -> server", "raw": req3})
    wire.append({"direction": "server -> client", "raw": recv(proc)})

    proc.terminate()
    with open("wire.json", "w") as f:
        json.dump(wire, f, indent=2)
    print(json.dumps(wire, indent=2))
    print("\nSaved wire.json")


if __name__ == "__main__":
    main()
