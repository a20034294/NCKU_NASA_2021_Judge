def anime_create_task(src_path, dst_path, task_id):
    from tasks import ffmpeg_trans_hls, celery
    result_data = dict()
    result_data['1080p'] = ffmpeg_trans_hls.delay(src_path, dst_path, 1080, task_id).id
    result_data['480p'] = ffmpeg_trans_hls.delay(src_path, dst_path, 480, task_id).id

    return result_data
