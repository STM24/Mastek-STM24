from moviepy.editor import VideoFileClip

# Set the path to your video file
video_path = 'path/to/video.mp4'

# Set the path where you want to save the audio file
audio_path = 'path/to/audio.wav'

# Load the video file
clip = VideoFileClip("./Input_Files/sample_video.mp4")


# Extract the audio from the video
audio = clip.audio

# Save the audio to a WAV file
audio.write_audiofile("sample_audio.wav", codec='pcm_s16le')