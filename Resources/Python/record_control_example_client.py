"""
    A zmq client to test remote control of open-ephys GUI via Network Events plugin
"""

import zmq
import os
import time
import enum


class Commands(enum.Enum):
    StartAcquisition = "StartAcquisition"
    StopAcquisition = "StopAcquisition"
    StartRecord = "StartRecord"
    StopRecord = "StopRecord"
    IsAcquiring = "IsAcquiring"
    IsRecording = "IsRecording"
    GetRecordingPath = "GetRecordingPath"


def run_client():

    # Example settings
    rec_dir = os.path.join(os.getcwd(), "Output_RecordControl")
    print("Saving data to:", rec_dir)

    # Some commands with arguments
    record_commands_with_args = [
        Commands.StartRecord.value + f" RecDir={rec_dir}",
        Commands.StartRecord.value + " PrependText=Session01 AppendText=Condition01",
        Commands.StartRecord.value + " PrependText=Session01 AppendText=Condition02",
        Commands.StartRecord.value + " PrependText=Session02 AppendText=Condition01",
        Commands.StartRecord.value,
        Commands.StartRecord.value + " CreateNewDir=1",
    ]

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
            socket.send_string(Commands.StartAcquisition.value)
            print(socket.recv_string())
            time.sleep(5)

            socket.send_string(Commands.IsAcquiring.value)
            print("IsAcquiring:", socket.recv_string())
            print("")

            for command_with_args in record_commands_with_args:

                socket.send_string(command_with_args)
                print(socket.recv_string())

                # Record data for 5 seconds
                socket.send_string(Commands.IsRecording.value)
                print("IsRecording:", socket.recv_string())

                socket.send_string(Commands.GetRecordingPath.value)
                print("Recording path:", socket.recv_string())

                time.sleep(5)

                # Stop for 1 second
                socket.send_string(Commands.StopRecord.value)
                print("IsRecording:", socket.recv_string())
                time.sleep(1)

            # Finally, stop data acquisition; it might be a good idea to
            # wait a little bit until all data have been written to hard drive
            time.sleep(0.5)
            socket.send_string(Commands.StopAcquisition.value)
            print(socket.recv_string())


if __name__ == "__main__":
    run_client()
