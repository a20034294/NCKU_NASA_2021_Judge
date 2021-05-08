import os
from os import getenv as env
import subprocess
from celery import states
from celery.exceptions import Ignore


def ffmpeg_trans_hls_task(src_path, dst_path, resolution, paraent_task_id):
    res = str(resolution)
    params = \
        " -acodec copy" \
        " -vcodec libx264" \
        f" -filter_complex \"[0:v]uspp[a]; [a]gradfun[b]; [b]scale=-2:{res}:flags=lanczos+full_chroma_int\"" \
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

    # [:-1] bacause ends with \n
    log_file = subprocess.run(
        'mktemp', shell=True, capture_output=True, check=True).stdout[:-1]
    print(log_file.decode('utf-8'))

    result = subprocess.run(
        script, shell=True, capture_output=True)

    result_data = dict()
    if result.returncode != 0:
        print(result.stderr.decode('utf-8'))
        with open(log_file, 'w') as f:
            f.write(result.stderr.decode('utf-8'))
        result_data['status'] = 'FAILURE'
    else:
        result_data['status'] = 'SUCCESS'
    print(result.stdout.decode('utf-8'))

    result_data['playlist_path'] = output_m3u8_name
    result_data['resolution'] = str(resolution)
    result_data['patent_task_id'] = paraent_task_id
    result_data['log'] = str(result.stderr.decode('utf-8'))

    return result_data
