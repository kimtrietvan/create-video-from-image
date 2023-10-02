from PIL import Image
import glob
import numpy as np
from subprocess import Popen, PIPE
from lib.Image import StaticImage, DynamicImage
import argparse
import os
argParser = argparse.ArgumentParser()
argParser.add_argument("-i", "--images", help="Your images folder")
argParser.add_argument("-f", "--front", help="Your front layer")
argParser.add_argument("-b", "--back", help="Your back layer")
argParser.add_argument('-o', '--output', help="Video output")
argParser.add_argument('-s', '--sound', help="Sound data", required=False, default=None)
argParser.add_argument('-sl', '--soundLoop', help="Sound loop or not", required=False, default=False, type=bool)



args = argParser.parse_args()


images = [Image.open(path).convert("RGBA") for path in sorted(glob.glob(os.path.join(args.images,'*')))]
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
if args.sound == None:
    p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-i', '-', '-vcodec', 'libx264', '-qscale', '5','-b','1000k', '-r', '30','-pix_fmt', 'yuv420p', args.output], stdin=PIPE)
elif args.soundLoop:
    p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-i', '-','-stream_loop', '-1', '-i', args.sound, '-shortest', '-acodec', 'aac', '-vcodec', 'libx264', '-qscale', '5','-b','1000k', '-r', '30','-pix_fmt', 'yuv420p', args.output], stdin=PIPE)
else:
    p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-i', '-','-stream_loop', '-1', '-i', args.sound,'-map', '0', '-map', '1', '-shortest','-acodec', 'aac', '-vcodec', 'libx264', '-qscale', '5','-b','1000k', '-r', '30','-pix_fmt', 'yuv420p', args.output], stdin=PIPE)
average_width =  average_width if average_width % 2 == 0 else average_width - 1
for i in range(width - average_width):
    bImage = backLayerImage.take_frame_by_frame()
    bImage = bImage.convert("RGBA")

    l = img[:, :(i % width)]
    r = img[:, (i % width):]
    
    img1 = np.hstack((r, l))
      
    temp_img = Image.fromarray(img1[:, :average_width, :])
    # temp_img.show()
    bImage = bImage.resize(temp_img.size)
    temp_img = Image.alpha_composite(bImage, temp_img)
    fImage = frontLayerImage.take_frame_by_frame().convert("RGBA").resize(temp_img.size)
    temp_img = Image.alpha_composite(temp_img, fImage)
    temp_img.save(p.stdin, 'PNG')


p.stdin.close()
p.wait()