# FCAST_Client Wrapper Documentation

This is a Python client wrapper for the video streaming receiver found at [fcast on GitLab](https://gitlab.futo.org/videostreaming/fcast/-/tree/master). The `FCAST_Client` class provides an easy-to-use interface to communicate with the reciever and control video playback.

## Installation

Ensure you have Python installed and the required libraries. This wrapper uses the `socket`, `json`, and `struct` libraries which are part of the Python standard library.

## Usage

First, create an instance of the `FCAST_Client`:

```python
client = FCAST_Client(host="your_host_here", port=46899)
```

### Methods

#### play

Plays a video.

```python
client.play(container="video/mp4", url="http://example.com/video.mp4")
```

Parameters:
- `container`: The MIME type (e.g., "video/mp4").
- `url`: The URL to load (optional).
- `content`: The content to load (e.g., a DASH manifest, optional).
- `time`: The time to start playing in seconds (optional).

#### pause

Pauses the video.

```python
client.pause()
```

#### resume

Resumes the video.

```python
client.resume()
```

#### stop

Stops the video.

```python
client.stop()
```

#### seek

Seeks to a specific time in the video.

```python
client.seek(time=120)  # Seeks to 2 minutes into the video.
```

Parameters:
- `time`: The time to seek to in seconds.

#### set_volume

Sets the volume of the video.

```python
client.set_volume(volume=0.5)  # Sets the volume to 50%.
```

Parameters:
- `volume`: The volume level (0.0 - 1.0).

#### close

Closes the connection to the reciever.

```python
client.close()
```

## Example of Usage with `fcast`

To use the `FCAST_Client` wrapper with the `fcast` reciever, follow the steps below:

1. Ensure the `fcast` reciever is running and listening on the desired host and port.

2. Create an instance of the `FCAST_Client` and connect to the `fcast` reciever:

```python
from fcast import FCAST_Client

# Replace with the appropriate host and port of your fcast reciever
client = FCAST_Client(host="your_host_here", port=46899)
```

3. Play a video:

```python
# Play a video from a URL
client.play(container="video/mp4", url="http://example.com/video.mp4")
```

4. Control the video playback:

```python
import time

# Pause the video after 5 seconds
time.sleep(5)
client.pause()

# Resume playback after another 5 seconds
time.sleep(5)
client.resume()

# Seek to 2 minutes into the video after 5 seconds
time.sleep(5)
client.seek(time=120)

# Adjust the volume to 50%
client.set_volume(volume=0.5)
```

5. Once done, close the connection:

```python
client.close()
```