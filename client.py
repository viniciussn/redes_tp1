import socket
import sys
import time

BUFFER = ''


def get_address_family(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
        return socket.AF_INET
    except:
        pass

    try:
        socket.inet_pton(socket.AF_INET6, address)
        return socket.AF_INET6
    except:
        pass

    sys.exit(1)


def create_socket(address, port):
    address_family = get_address_family(address)
    attempts = 0
    client_socket = None
    while attempts < 5:
        try:
            client_socket = socket.socket(address_family, socket.SOCK_STREAM)
            client_socket.connect((address, port))
            break
        except socket.error:
            client_socket = None
            time.sleep(0.05)
        attempts += 1
    if not client_socket:
        sys.exit(2)
    return client_socket


# send one message
def send(client_socket, msg):
    msg = msg.encode('ascii')
    total_sent = 0
    while total_sent != len(msg):
        sent = client_socket.send(msg[total_sent:])
        if sent == 0:
            sys.exit(3)
        total_sent += sent


# receive one complete message
def receive(client_socket):
    global BUFFER
    while True:
        if '\n' in BUFFER:
            msg = BUFFER[:BUFFER.index('\n')]
            BUFFER = BUFFER[BUFFER.index('\n') + 1:]
            return msg
        try:
            data = client_socket.recv(500 - len(BUFFER)).decode()
        except socket.timeout:
            sys.exit(7)
        
        if not data:
            sys.exit(4)

        BUFFER += data
        if len(BUFFER) >= 500:
            sys.exit(5)


def run_multiple_msg_single_pkg(client_socket):
    msg_buffer = []
    for msg in sys.stdin:
        msg_buffer.append(msg)

    for i in range(0, len(msg_buffer), 2):
        if i == len(msg_buffer) - 1:
            send(client_socket, msg_buffer[i])
            if msg_buffer[i] == 'kill\n':
                client_socket.close()
                sys.exit(0)
            ret = receive(client_socket)
            print(ret)
        else:
            msg = msg_buffer[i] + msg_buffer[i + 1]
            send(client_socket, msg)
            if msg_buffer[i] == 'kill\n':
                client_socket.close()
                sys.exit(0)
            ret = receive(client_socket)
            print(ret)
            if msg_buffer[i + 1] == 'kill\n':
                client_socket.close()
                sys.exit(0)
            ret = receive(client_socket)
            print(ret)


def run_single_msg_multiple_pkg(client_socket):
    for msg in sys.stdin:
        send(client_socket, msg[:3])
        time.sleep(0.1)
        send(client_socket, msg[3:])
        if msg == 'kill\n':
            client_socket.close()
            sys.exit(0)
        ret = receive(client_socket)
        print(ret)


def run_single_msg_single_pkg(client_socket):
    for msg in sys.stdin:
        send(client_socket, msg)
        if msg == 'kill\n':
            client_socket.close()
            sys.exit(0)
        ret = receive(client_socket)
        print(ret)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(
            f'Usage: python3 {sys.argv[0]} <address> <port> [single_msg_single_pkg | single_msg_multiple_pkg | multiple_msg_single_pkg]')
        sys.exit(6)
    client_socket = create_socket(sys.argv[1], int(sys.argv[2]))
    client_socket.settimeout(5)

    if sys.argv[3] == 'single_msg_single_pkg':
        run_single_msg_single_pkg(client_socket)
    elif sys.argv[3] == 'single_msg_multiple_pkg':
        run_single_msg_multiple_pkg(client_socket)
    elif sys.argv[3] == 'multiple_msg_single_pkg':
        run_multiple_msg_single_pkg(client_socket)

    client_socket.close()
    sys.exit(0)
