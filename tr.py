import subprocess
import speech_recognition as sr
from pydub import AudioSegment
import os

def extract_audio_from_video(video_path, audio_path):
    command = f"ffmpeg -i {video_path} -q:a 0 -map a {audio_path} -y"
    subprocess.run(command, shell=True, check=True)

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_wav(audio_path)
    chunks = split_audio(audio)
    
    subtitles = []
    for i, chunk in enumerate(chunks):
        chunk.export(f"chunk{i}.wav", format="wav")
        with sr.AudioFile(f"chunk{i}.wav") as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                subtitles.append((i, text))
            except sr.UnknownValueError:
                subtitles.append((i, "[Inaudible]"))
            except sr.RequestError as e:
                subtitles.append((i, f"[Error: {e}]"))
        os.remove(f"chunk{i}.wav")
    
    return subtitles

def split_audio(audio, chunk_length_ms=30000):
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunks.append(audio[i:i + chunk_length_ms])
    return chunks

def label_speakers(subtitles):
    # Placeholder for speaker identification logic
    # This could be replaced with a more sophisticated model
    labeled_subtitles = []
    for i, text in subtitles:
        speaker = "Speaker 1" if i % 2 == 0 else "Speaker 2"
        labeled_subtitles.append((speaker, text))
    return labeled_subtitles

def main(video_path):
    audio_path = "extracted_audio.wav"
    extract_audio_from_video(video_path, audio_path)
    subtitles = transcribe_audio(audio_path)
    labeled_subtitles = label_speakers(subtitles)
    
    with open("subtitles.txt", "w", encoding="utf-8") as f:
        for speaker, text in labeled_subtitles:
            f.write(f"{speaker}: {text}\n")
            print(f"{speaker}: {text}")

if __name__ == "__main__":
    video_path = "videoplayback.mp4"
    main(video_path)