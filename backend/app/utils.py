import subprocess


def add_emoji_to_video(input_path: str, output_path: str) -> bool:
    """Накладывает эмодзи по центру видео с помощью ffmpeg."""

    emoji = "😊"

    command = [
        "ffmpeg",
        "-i", input_path,
        "-vf",
        f"drawtext=text='{emoji}':fontcolor=white:fontsize=64:"
        f"box=1:boxcolor=black@0.5:boxborderw=5:"
        f"x=(w-text_w)/2:y=(h-text_h)/2",
        "-c:a", "copy",
        "-y",
        output_path
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        print("FFmpeg output:", result.stdout)
        if result.stderr:
            print("FFmpeg errors:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg failed with error: {e}")
        print(f"Stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
