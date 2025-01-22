from moviepy.editor import *
import moviepy.editor as mp
import speech_recognition as sr

# Function to transcribe audio from an audio file
def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(audio_path)

    with audio_file as source:
        audio = recognizer.record(source)  # Record the audio from the file

    try:
        transcript = recognizer.recognize_google(audio)  # Perform transcription
        return transcript
    except sr.UnknownValueError:
        return "Error: Could not transcribe audio"
    except sr.RequestError as e:
        return f"Error: {e}"

# Input video file path
video_path = "/home/dan/git_clones/video-transcriber/final_video_converted.mp4"

# Load the video
video_clip = mp.VideoFileClip(video_path)

# Initialize variables
segment_duration = 5  # Maximum duration of each audio segment (in seconds)
current_time = 0
text_clips = []

# Process the video in segments
while current_time < video_clip.duration - 1:
    # Calculate the duration of the current segment
    remaining_duration = min(segment_duration, video_clip.duration - current_time)

    # Extract the audio segment from the video
    audio_segment = video_clip.subclip(current_time, current_time + remaining_duration)
    audio_path = f"temp_audio_{current_time:.2f}.wav"
    audio_segment.audio.write_audiofile(audio_path, codec='pcm_s16le')

    # Transcribe the audio segment
    transcript = transcribe_audio(audio_path)

    # Create a TextClip for the transcribed text
    text_clip = mp.TextClip(transcript, fontsize=25, color='white', bg_color='black', font='UbuntuMono-Nerd-Font-Mono')
    text_clip = text_clip.set_duration(remaining_duration)
    text_clip = text_clip.set_position(('center', 'bottom'))
    text_clips.append(text_clip)


    # Update the current time for the next segment
    current_time += remaining_duration

# Concatenate the text clips to create synchronized text
text_clip = mp.concatenate_videoclips(text_clips, method="compose")
text_clip = text_clip.set_position(('center', 'bottom')).set_duration(video_clip.duration)

# Overlay the transcribed text on the video
video_with_text = mp.CompositeVideoClip([video_clip, text_clip])

# Output video file path
output_video_path = "output_video_with_text.mp4"

# Write the modified video to a file
video_with_text.write_videofile(output_video_path, codec='libx264', audio_codec='aac')

print(f"Video with synchronized transcribed text saved to {output_video_path}")
