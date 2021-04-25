import os
from os import getenv as env


def anime_create_task(src_path, dst_path):
    anime_create_task_h264_1080(src_path, dst_path)
    return dst_path + "/playlist.m3u8"


def anime_create_task_h264_1080(src_path, dst_path):
    params = \
        " -acodec copy" \
        " -vcodec libx264" \
        " -filter_complex \"[0:v]uspp[a]; [a]gradfun[b]; [b]scale=-1:1080:flags=lanczos+full_chroma_int\"" \
        " -crf 20" \
        " -preset:v veryslow" \
        " -map 0 -f segment" \
        " -segment_time 5"

    script = \
        f"ffmpeg -i \"{os.path.join(env('ANIME_SRC_ROOT_DIR'), src_path)}\"" \
        f"{params}" \
        f" -segment_list \"{os.path.join(env('ANIME_DST_ROOT_DIR'), dst_path, 'playlist_h264_1080p_uspp.m3u8')}\"" \
        f" -segment_list_entry_prefix \"/{dst_path}/\"" \
        f" \"{os.path.join(env('ANIME_DST_ROOT_DIR'), dst_path, 'output%04d_h264_1080p_uspp.ts')}\""

    print(script)
    os.system(script)
