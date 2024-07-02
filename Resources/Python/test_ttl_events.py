import zmq
import time


def run_client():

    # Connect network handler
    ip = "127.0.0.1"
    port = 5556
    timeout = 1.0

    url = f"tcp://{ip}:{port}"

    with zmq.Context() as context:
        with context.socket(zmq.REQ) as socket:
            socket.RCVTIMEO = int(timeout * 1000)  # timeout in milliseconds
            socket.connect(url)

            # Start data acquisition
            socket.send_string("StartAcquisition")
            print(socket.recv_string())
            time.sleep(1)

            socket.send_string("StartRecord")
            print(socket.recv_string())

            for line in range(1, 64):
                socket.send_string(f"TTL Line={line} State=1")
                print(socket.recv_string())
                socket.send_string(f"TTL Line={line} State=0")
                print(socket.recv_string())
                time.sleep(0.001)

            for word in range(0, 2**16, 16):
                socket.send_string(f"TTL Word={word}")
                print(socket.recv_string())
                time.sleep(0.001)

            time.sleep(1)
            socket.send_string("StopRecord")
            print(socket.recv_string())

            socket.send_string("StopAcquisition")
            print(socket.recv_string())


if __name__ == "__main__":
    run_client()
