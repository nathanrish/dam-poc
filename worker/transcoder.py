import subprocess
import os

def transcode_to_hls(input_file, output_dir):
    """
    Transcodes the input video file to HLS format using FFmpeg.
    Generates 'playlist.m3u8' and .ts segments in the output_dir.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_playlist = os.path.join(output_dir, "playlist.m3u8")

    # Basic HLS transcoding command
    command = [
        "ffmpeg",
        "-i", input_file,
        "-profile:v", "baseline",  # Baseline profile for compatibility
        "-level", "3.0",
        "-start_number", "0",
        "-hls_time", "10",         # Segment duration in seconds
        "-hls_list_size", "0",     # Include all segments in the playlist
        "-f", "hls",
        output_playlist
    ]

    try:
        # Run FFmpeg command
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Transcoding complete. HLS playlist saved to: {output_playlist}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during transcoding: {e.stderr.decode()}")
        raise e
