import ffmpeg
import subprocess
# def speed_up_video(input_video, output_duration):
#     # Đọc thông số video gốc
#     probe = ffmpeg.probe(input_video)
#     video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
#     fps_values = video_stream['r_frame_rate'].split('/') 
#     numerator = float(fps_values[0])
#     denominator = float(fps_values[1])
#     fps = numerator / denominator
#     duration = float(video_stream['duration'])
#     print(duration)
#     print(fps)
#     # Tính fps cần
#     new_fps = int(fps * (duration / output_duration))
#     print(new_fps)
#     # Rút ngắn video
#     ffmpeg.input(input_video).output(
#         'output.mp4', 
#         # preset='ultrafast',
#         # crf=18, 
#         vf=f'setpts=PTS * {fps / new_fps}',
#         # strict='experimental'
#     ).run()
    
#     print("Video rút ngắn thành công!")
# # Gọi hàm
# speed_up_video('data1.mp4', 60) 

test = subprocess.run(['pip3', 'uninstall', 'pillow'])
# print(test.stdout)
