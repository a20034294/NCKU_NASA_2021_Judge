import os
from os import getenv as env


def anime_create_task(src_path, dst_path):
    script = 'ffmpeg -i "' + env('ANIME_SRC_ROOT_DIR') + src_path + '"'
    script += ' -acodec copy'
    script += ' -vcodec libx264'
    script += ' -crf 19'
    script += ' -map 0 -f segment'
    script += ' -segment_time 5'
    script += ' -segment_list "' + \
        env('ANIME_DST_ROOT_DIR') + dst_path + '/playlist.m3u8"'
    script += ' -segment_list_entry_prefix "' + dst_path + '/"'
    script += ' "' + dst_path + '/output%04d.ts' + '"'

    print(script)
    os.system(script)
    return dst_path + '/playlist.m3u8'
