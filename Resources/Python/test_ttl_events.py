import zmq
import time


def send_ttl_line(socket, number_of_lines=64):
    for line in range(1, number_of_lines + 1):
        socket.send_string(f"TTL Line={line} State=1")
        print(socket.recv_string())
        socket.send_string(f"TTL Line={line} State=0")
        print(socket.recv_string())
        time.sleep(0.002)


def reset_lines(socket):
    # reset to zero
    socket.send_string(f"TTL Word={0}")
    print(socket.recv_string())


def send_ttl_words(socket, words: list[int]):
    for word in words:
        socket.send_string(f"TTL Word={word}")
        print(socket.recv_string())
        time.sleep(0.002)


def run_client():
    # Connect network handler
    ip = "127.0.0.1"
    port = 5556
    timeout = 300.0

    url = f"tcp://{ip}:{port}"

    with zmq.Context() as context:
        with context.socket(zmq.REQ) as socket:
            socket.RCVTIMEO = int(timeout * 1000)  # timeout in milliseconds
            socket.connect(url)

            # Start data acquisition
            socket.send_string("StartAcquisition")
            print(socket.recv_string())

            reset_lines(socket)

            time.sleep(1)
            socket.send_string("StartRecord")
            print(socket.recv_string())

            send_ttl_line(socket, number_of_lines=64)

            socket.send_string("StopRecord")
            print(socket.recv_string())
            time.sleep(1)

            # send 2048 TTL words
            socket.send_string("StartRecord")
            print(socket.recv_string())

            # words = list(range(1, 2**16 + 1, 32))
            words = [97, 129]
            send_ttl_words(socket, words)

            socket.send_string("StopRecord")
            print(socket.recv_string())

            # reset to zero
            socket.send_string(f"TTL Word={0}")
            print(socket.recv_string())

            socket.send_string("StopAcquisition")
            print(socket.recv_string())


if __name__ == "__main__":
    run_client()
