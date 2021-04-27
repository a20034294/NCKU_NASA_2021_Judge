def anime_create_task(src_path, dst_path, task_id):
    from tasks import ffmpeg_trans_hls, celery
    result = []
    result.append(ffmpeg_trans_hls.delay(src_path, dst_path, 1080, task_id).id)

    return result
