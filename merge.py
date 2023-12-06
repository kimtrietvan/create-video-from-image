from PIL import Image
import glob
import requests
import numpy as np
from subprocess import Popen, PIPE
from lib.Image import StaticImage, DynamicImage
import argparse
import os
import io
import ffmpeg
import uuid

def get_paths(directory):
    # Lấy danh sách tất cả các files trong thư mục
    files = os.listdir(directory)

    # Sắp xếp danh sách files theo thứ tự số
    sorted_files = sorted(files, key=lambda x: int(x.split('.')[0]))

    # Tạo đường dẫn tuyệt đối cho từng file
    paths = [os.path.join(directory, file) for file in sorted_files]
    return paths

def speed_up_video(input_video, output_duration, output):
    # Đọc thông số video gốc
    probe = ffmpeg.probe(input_video)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    fps_values = video_stream['r_frame_rate'].split('/') 
    numerator = float(fps_values[0])
    denominator = float(fps_values[1])
    fps = numerator / denominator
    duration = float(video_stream['duration'])
    print(duration)
    print(fps)
    # Tính fps cần
    new_fps = int(fps * (duration / output_duration))
    print(new_fps)
    # Rút ngắn video
    ffmpeg.input(input_video).output(
        output, 
        # preset='ultrafast',
        # crf=18, 
        vf=f'setpts=PTS * {fps / new_fps}',
        # strict='experimental'
    ).run()
    os.remove(input_video)
    
# Gọi hàm

argParser = argparse.ArgumentParser()
argParser.add_argument("-i", "--images", help="Your images url list")
argParser.add_argument("-f", "--front", help="Your front layer")
argParser.add_argument("-b", "--back", help="Your back layer")
argParser.add_argument('-o', '--output', help="Video output")
argParser.add_argument('-s', '--sound', help="Sound data", required=False, default=None)
argParser.add_argument('-sl', '--soundLoop', help="Sound loop or not", required=False, default=False, type=bool)
args = argParser.parse_args()

# image_url = []
# with open(args.images) as f:
#     for line in f:
#         image_url.append(line.split("\n")[0])

# images = [Image.open(io.BytesIO(requests.get(path).content)).convert("RGBA") for path in image_url]
images_path = get_paths(args.images)
images = [Image.open(path).convert('RGBA') for path in images_path]
# print(os.environ['average_height'])
max_width = sum(np.array(image).shape[1] for image in images)
max_height = max(np.array(image).shape[0] for image in images)
average_width = int(max_width / len(images))
result_image = Image.new("RGBA", (max_width, max_height))

x_offset = 0
for img in images:
    temp_image = Image.new("RGBA", (max_width, max_height), color=(0,0,0,0))
    temp_image.paste(img, (x_offset, max_height - img.height), mask=img)

    result_image = Image.alpha_composite(result_image, temp_image)
    x_offset += img.width



result_image = result_image.convert("RGBA")


for img in images:
    img.close()

result_numpy = np.array(result_image)
img = result_numpy
  
height, width, c = img.shape
  
i = 0
if args.back.split(".")[-1].lower() == 'mp4':
    backLayerImage = DynamicImage(args.back)
else:
    backLayerImage = StaticImage(args.back)

if args.front.split(".")[-1].lower() == 'mp4':
    frontLayerImage = DynamicImage(args.front)
else:
    frontLayerImage = StaticImage(args.front)
temp_name = uuid.uuid1()
p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-i', '-', '-qscale', '5', '-r', '30','-pix_fmt', 'yuv420p', f'{temp_name}.mp4'], stdin=PIPE)
average_width =  average_width if average_width % 2 == 0 else average_width - 1
frames = []
for i in range(width - average_width):
    bImage = backLayerImage.take_frame_by_frame()
    fImage = frontLayerImage.take_frame_by_frame()
    
    bImage = bImage.convert("RGBA")

    l = img[:, :(i % width)]
    r = img[:, (i % width):]
    
    img1 = np.hstack((r, l))
    temp_img = Image.fromarray(img1[:, :average_width, :])
    bImage = bImage.resize(temp_img.size)
    temp_img = Image.alpha_composite(bImage, temp_img)
    fImage = fImage.convert("RGBA").resize(temp_img.size)
    temp_img = Image.alpha_composite(temp_img, fImage)
    temp_img.save(p.stdin, 'PNG')
    



p.stdin.close()
p.wait()

output_time = len(images_path) * 5

speed_up_video(f'{temp_name}.mp4', output_time, args.output)