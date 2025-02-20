import os
import whisper
import srt
import ffmpeg
from datetime import timedelta

def extract_audio(video_path, audio_path="audio.wav"):
    """提取视频中的音频"""
    ffmpeg.input(video_path).output(audio_path, format="wav", acodec="pcm_s16le", ac=1, ar="16000").run(overwrite_output=True)
    return audio_path

def transcribe_audio(audio_path):
    """使用 Whisper 进行语音识别"""
    model = whisper.load_model("medium")  # 可选 "tiny", "base", "small", "medium", "large"
    result = model.transcribe(audio_path, language="en")
    return result["segments"]

def convert_to_srt(segments, srt_path="output.srt"):
    """将识别结果转换为 SRT 格式"""
    subtitles = []
    for seg in segments:
        start = timedelta(seconds=seg["start"])
        end = timedelta(seconds=seg["end"])
        subtitles.append(srt.Subtitle(index=seg["id"], start=start, end=end, content=seg["text"]))

    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt.compose(subtitles))

    print(f"SRT 字幕已保存: {srt_path}")

def main(file_path):
    """主函数"""
    if file_path.lower().endswith(".m4a"):
        print("检测到 M4A 文件，直接进行语音识别...")
        audio_path = file_path
    else:
        print("检测到视频文件，正在提取音频...")
        audio_path = extract_audio(file_path)

    print("正在进行语音识别...")
    segments = transcribe_audio(audio_path)

    print("正在生成 SRT 字幕...")
    convert_to_srt(segments)

if __name__ == "__main__":
    file_path = "videoplayback.m4a"  # 这里改成你的音频/视频文件路径
    main(file_path)
