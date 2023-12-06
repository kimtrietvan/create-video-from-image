from fastapi import FastAPI, UploadFile, File
from typing import List
import uvicorn
import uuid
import os
import subprocess
from fastapi.responses import FileResponse
import shutil

app = FastAPI()

@app.post('/image_to_video')
async def tranfer_image_to_video(file: List[UploadFile], frontend: UploadFile, backend: UploadFile):
    id = str(uuid.uuid4())
    folder_dir = os.path.join(os.getcwd(),'images', id)
    frontLayer = os.path.join(os.getcwd(), 'frontLayer', f'{id}.{frontend.filename.split(".")[-1]}')
    backLayer = os.path.join(os.getcwd(), 'backLayer', f'{id}.{backend.filename.split(".")[-1]}')
    output_dir = os.path.join(os.getcwd(), 'videos', id)
    os.mkdir(folder_dir)

    for index, data in enumerate(file):
        with open(os.path.join(folder_dir, f'{index}.png'), 'wb') as f:
            content = await data.read()
            f.write(content)
    with open(frontLayer, 'wb') as f:
        content = await frontend.read()
        f.write(content)
    with open(backLayer, 'wb') as f:
        content = await backend.read()
        f.write(content)
    subprocess.run(f'python3 {os.path.join(os.getcwd(), "merge.py")} -i {folder_dir} -o {output_dir}.mp4 -f {frontLayer} -b {backLayer}'.split(' '))
    # shutil.rmtree(folder_dir)

    return FileResponse(f'{output_dir}.mp4')




    # os.rmdir(folder_dir)
    # return folder_dir
    # for f in file:
        
    # return file

# uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)

