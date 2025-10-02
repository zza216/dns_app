import socket

# File to store DNS records
DNS_FILE = "dns_records.txt"
PORT = 53533

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))
print("Authoritative Server running on UDP port", PORT)

while True:
    data, addr = sock.recvfrom(1024)
    text = data.decode().strip().split("\n")

    # Registration message (has VALUE=)
    if "VALUE=" in text[1]:
        # Example: NAME=fibonacci.com VALUE=172.18.0.2 TTL=10
        parts = text[1].split()
        name = parts[0].split("=")[1]
        ip = parts[1].split("=")[1]

        with open(DNS_FILE, "w") as f:
            f.write(f"TYPE=A\nNAME={name} VALUE={ip} TTL=10\n")

        print("Registered:", name, "->", ip)

    # Query message (only NAME=)
    else:
        name = text[1].split("=")[1]
        try:
            with open(DNS_FILE, "r") as f:
                line = f.readlines()[1]  # second line has NAME, VALUE, TTL
                parts = line.strip().split()
                stored_name = parts[0].split("=")[1]
                value = parts[1].split("=")[1]
                ttl = parts[2].split("=")[1]
                if stored_name == name:
                    reply = f"TYPE=A\nNAME={name} VALUE={value} TTL={ttl}\n"
                else:
                    reply = f"NOTFOUND {name}\n"
        except:
            reply = f"NOTFOUND {name}\n"

        sock.sendto(reply.encode(), addr)