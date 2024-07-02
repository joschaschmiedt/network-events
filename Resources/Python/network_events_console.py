import zmq


def run(hostname="localhost", port=5556):
    with zmq.Context() as ctx:
        with ctx.socket(zmq.REQ) as sock:
            sock.connect(f"tcp://{hostname}:{port}")
            # set timeouts to 1 second
            sock.setsockopt(zmq.RCVTIMEO, 1000)
            sock.setsockopt(zmq.SNDTIMEO, 1000)
            req = ""
            while req != "exit":
                try:
                    req = input("> ")

                    if req == "help":
                        print_help()
                        continue

                    sock.send_string(req)
                    rep = sock.recv_string()
                    print(rep)
                except EOFError:
                    print()  # Add final newline
                    break


def print_help():
    print("Commands:")
    print("    StartAcquisition")
    print("    StopAcquisition")
    print("    IsAcquiring")
    print(
        "    StartRecord [RecDir=<path>] [PrependText=<text>] [AppendText=<text>] [CreateNewDir=1]"
    )
    print("    StopRecord")
    print("    IsRecording")
    print("    GetRecordingPath")
    print("    TTL [Line=<line>] [State=<on/off>]")
    print("    TTL [Word=<word>]")
    print("    exit")


if __name__ == "__main__":

    print("Welcome to the Open Ephys Network Events debug console!")
    print("Type 'exit' to quit. Try 'help' for a list of commands.")
    run()
