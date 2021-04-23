import os
from os import getenv as env


def anime_create_task(src_path, dst_path):
    params = " -acodec copy" \
        " -vcodec libx264" \
        " -crf 19" \
        " -map 0 -f segment" \
        " -segment_time 5"

    script = f"ffmpeg -i \"{env('ANIME_SRC_ROOT_DIR') + src_path}\"" \
        f"{params}" \
        f" -segment_list \"{env('ANIME_DST_ROOT_DIR') + dst_path}/playlist.m3u8\"" \
        f" -segment_list_entry_prefix \"{dst_path}/\"" \
        f" \"{dst_path}/output%04d.ts\""

    print(script)
    os.system(script)
    return dst_path + "/playlist.m3u8"
