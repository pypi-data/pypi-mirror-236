import socket
import json
import struct

class FCAST_Client:
    def __init__(self, host, port=46899):
        """Initializes the client.
            host: String, //The host to connect to
            port: number = 46899 //The port to connect to
        """
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send_message(self, opcode, body=None):
        if body:
            body = json.dumps(body).encode('utf-8')
            header = struct.pack('<IB', len(body) + 1, opcode)
        else:
            header = struct.pack('<IB', 1, opcode)
            body = b''
        self.sock.sendall(header + body)

    def play(self, container, url=None, content=None, time=None):
        """Plays a video.
            container: String, //The MIME type (video/mp4)
            url: String = null, //The URL to load (optional)
            content: String = null, //The content to load (i.e. a DASH manifest, optional)
            time: number = null //The time to start playing in seconds
        """
        body = {
            "container": container,
            "url": url,
            "content": content,
            "time": time
        }
        self.send_message(1, body)

    def pause(self):
        """Pauses the video."""
        self.send_message(2)

    def resume(self):
        """Resumes the video."""
        self.send_message(3)

    def stop(self):
        """Stops the video."""
        self.send_message(4)

    def seek(self, time):
        """Seeks to a time in the video.
            time: number //The time to seek to in seconds
        """
        body = {"time": time}
        self.send_message(5, body)

    def set_volume(self, volume):
        """Sets the volume of the video.
            volume: number //The volume to set (0.0 - 1.0)
        """
        body = {"volume": volume}
        self.send_message(8, body)

    def close(self):
        self.sock.close()