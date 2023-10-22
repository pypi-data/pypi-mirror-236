import os.path

import ffmpy
from kit.file_utils import Files
import os
from pydub import AudioSegment
from pydub.utils import make_chunks
from pathlib import Path
from moviepy.editor import VideoFileClip, concatenate_videoclips
import subprocess


class VideoHandler:
    @classmethod
    def video_format_converter(cls, source_file, dest=None):
        if dest is None:
            name = "converted_" + Files.get_file_name(source_file)
            format = Files.get_file_format(source_file)
            dest = os.path.join(Files.get_file_parent(source_file), '{}.{}'.format(name, format))
        video = ffmpy.FFmpeg(
            inputs={source_file: None},
            outputs={dest: None})
        video.run()

    @classmethod
    def merge_videos(cls, source_file, dest=None):
        if dest is None:
            name = "merged_" + Files.get_file_name(source_file)
            format = Files.get_file_format(source_file)
            dest = os.path.join(Files.get_file_parent(source_file), '{}.{}'.format(name, format))
        all = []
        for i in source_file:
            all.append(VideoFileClip(i))
        final_video = concatenate_videoclips(all)
        final_video.write_videofile(dest)

    @classmethod
    def audio_format_converter(cls, source_file, dest=None):
        if dest is None:
            name = "converted_" + Files.get_file_name(source_file)
            format = Files.get_file_format(source_file)
            dest = os.path.join(Files.get_file_parent(source_file), '{}.{}'.format(name, format))
        cmd = 'ffmpeg -y -i ' + source_file + ' -acodec pcm_s16le -f s16le -ac 1 -ar 16000 ' + dest
        os.system(cmd)

    @classmethod
    def cut_video_by_second(cls, source_file, start_s, end_s, dest=None):
        if dest is None:
            name = "cut_" + Files.get_file_name(source_file)
            format = Files.get_file_format(source_file)
            dest = os.path.join(Files.get_file_parent(source_file), '{}.{}'.format(name, format))
        clipOri = VideoFileClip(source_file).subclip(start_s, end_s)
        clipOri.write_videofile(dest)

    @classmethod
    def extract_gif_from_video(cls, source_file, start_s, end_s, size, dest=None):
        if dest is None:
            name = "extracted_gif_" + Files.get_file_name(source_file)
            format = Files.get_file_format(source_file)
            dest = os.path.join(Files.get_file_parent(source_file), '{}.{}'.format(name, format))
        clipOri = VideoFileClip(source_file).subclip(start_s, end_s)
        clipOri.write_gif(dest, size)

    @classmethod
    def extract_audio_from_video(cls, source_file, dest=None):
        if dest is None:
            name = "extracted_" + Files.get_file_name(source_file)
            format = Files.get_file_format(source_file)
            dest = os.path.join(Files.get_file_parent(source_file), '{}.{}'.format(name, format))
        audio = AudioSegment.from_file(dest)
        audio.export(dest, format=Files.get_file_format(dest))

    @classmethod
    def alter_video_size(cls, video, dest=None, aspect='16:9', scale='1280:720'):
        print('altering: ' + video)
        if dest is None:
            dest = os.path.join(Files.get_file_dir_path(video),
                                'altered_' + Files.get_file_name(video) + '.' + Files.get_file_format(video))
        resize = 'ffmpeg -i {} -aspect {} -vf scale={} {}'.format(video, aspect, scale, dest)
        subprocess.call(resize, shell=True)

    @classmethod
    def embed_subtitle_to_video(cls, video, subtitle, dest_file=None):
        print('embedding: ' + video)
        sub = '\'' + subtitle.replace('\\', '\\\\').replace(':', '\:') + '\''
        if dest_file is None:
            dest_file = os.path.join(Files.get_file_dir_path(video),
                                     'embed_' + Files.get_file_name(video) + '.' + Files.get_file_format(video))
        cmd_line = '''ffmpeg -i {} -vf subtitles="{}" {}'''.format(video, sub, dest_file)
        subprocess.call(cmd_line, shell=True)


class AudioHandler:

    @classmethod
    def split_audio_by_ms(cls, source_file, duration_ms, dest=None):
        if dest is None:
            name = "split_" + Files.get_file_name(source_file)
            format = Files.get_file_format(source_file)
            dest = os.path.join(Files.get_file_parent(source_file), '{}.{}'.format(name, format))
        f = Files.get_file_format(source_file)
        d = Files.get_file_name(source_file).replace(' ', '')
        audio = AudioSegment.from_file(source_file, format=f)

        chunks = make_chunks(audio, duration_ms)
        for i, chunk in enumerate(chunks):
            path = os.path.join(dest, d)
            Path(path).mkdir(parents=True, exist_ok=True)
            chunk_name = os.path.join(dest, d, '{}.{}'.format(i, f))
            chunk.export(chunk_name, format=f)

    @classmethod
    def split_audio_by_second(cls, source_file, duration_s, dest=None):
        if dest is None:
            name = "split_" + Files.get_file_name(source_file)
            format = Files.get_file_format(source_file)
            dest = os.path.join(Files.get_file_parent(source_file), '{}.{}'.format(name, format))
        AudioHandler.split_audio_by_ms(source_file, dest, duration_s * 1000)

    @classmethod
    def cut_audio_by_ms(cls, source_file, start_ms, end_ms, dest=None):
        if dest is None:
            name = "cut_" + Files.get_file_name(source_file)
            format = Files.get_file_format(source_file)
            dest = os.path.join(Files.get_file_parent(source_file), '{}.{}'.format(name, format))
        f = Files.get_file_format(source_file)
        audio = AudioSegment.from_file(source_file, format=f)
        slice = audio[start_ms:end_ms]
        slice.export(dest, format=f)

    @classmethod
    def cut_audio_by_second(cls, source_file, start_s, end_s, dest=None):
        if dest is None:
            name = "cut_" + Files.get_file_name(source_file)
            format = Files.get_file_format(source_file)
            dest = os.path.join(Files.get_file_parent(source_file), '{}.{}'.format(name, format))
        AudioHandler.cut_audio_by_ms(source_file, dest, start_s * 1000, end_s * 1000)

    @classmethod
    def merge_audios(cls, audios, target_file):
        all_files = []
        for file in audios:
            all_files.append(AudioSegment.from_file(file))

        audio_merged = all_files[0]
        del all_files[0]
        for i in all_files:
            audio_merged += i
        audio_merged.export(target_file, format=Files.get_file_format(target_file))
