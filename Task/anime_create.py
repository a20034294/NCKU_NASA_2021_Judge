import os
from os import getenv as env


def anime_create_task(src_path, dst_path):
    ffmpeg_trans_hls(src_path, dst_path, 1080)
    return dst_path + "/playlist.m3u8"


def ffmpeg_trans_hls(src_path, dst_path, resolution=1080):
    res = str(resolution)
    params = \
        " -acodec copy" \
        " -vcodec libx264" \
        f" -filter_complex \"[0:v]uspp[a]; [a]gradfun[b]; [b]scale=-1:{res}:flags=lanczos+full_chroma_int\"" \
        " -crf 20" \
        " -preset:v slow" \
        " -map 0 -f segment" \
        " -segment_time 5"

    input_file_name = os.path.join(env('ANIME_SRC_ROOT_DIR'), src_path)
    output_m3u8_name = os.path.join(env('ANIME_DST_ROOT_DIR'), dst_path,
                                    f"playlist_h264_{res}p_uspp.m3u8")
    output_ts_name = os.path.join(env('ANIME_DST_ROOT_DIR'), dst_path,
                                  f"output%04d_h264_{res}p_uspp.ts")
    script = \
        f"ffmpeg -i \"{input_file_name}\"" \
        f"{params}" \
        f" -segment_list \"{output_m3u8_name}\"" \
        f" -segment_list_entry_prefix \"/{dst_path}/\"" \
        f" \"{output_ts_name}\""

    print(script)
    os.system(script)
