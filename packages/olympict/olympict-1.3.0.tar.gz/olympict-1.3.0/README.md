# Olympict

![coverage](https://gitlab.com/gabraken/olympict/badges/master/coverage.svg?job=tests)![status](https://gitlab.com/gabraken/olympict/badges/master/pipeline.svg)

![Olympict](https://gitlab.com/gabraken/olympict/-/raw/master/Olympict.png)


Based on [olympipe](https://pypi.org/project/olympipe/), this project will make image processing pipelines easy to use using the basic multiprocessing module. 
This module uses type checking to ensure your data process validity from the start.

## Basic image processing pipeline

### Loading images from a folder and resize them to a new folder

```python
from olympict import ImagePipeline

p0 = ImagePipeline.load_folder("./examples") # path containing the images
p1 = p0.resize((150, 250)) # new width, new height
p2 = p1.save_to_folder("./resized_examples") # path to save the images
p2.wait_for_completion() # the code blocks here until all images are processed

print("Finished resizing")
```

### Loading images from a folder and overwrite them with a new size

```python
from olympict import ImagePipeline

p0 = ImagePipeline.load_folder("./examples") # path containing the images
p1 = p0.resize((150, 250))
p2 = p1.save() # overwrite the images
p2.wait_for_completion()
```

### Loading images from a folder and resize them keeping the aspect ratio using a padding color

```python
from olympict import ImagePipeline
blue = (255, 0, 0) # Colors are BGR to match opencv format

p0 = ImagePipeline.load_folder("./examples")
p1 = p0.resize((150, 250), pad_color=blue)
p2 = p1.save() # overwrite the images
p2.wait_for_completion()
```

### Load image to make a specific operation

```python
from olympict import ImagePipeline, Img

def operation(image: Img) -> Img:
    # set the green channel as a mean of blue and red channels
    img[:, :, 1] = (img[:, :, 0] + img[:, :, 2]) / 2
    return img

p0 = ImagePipeline.load_folder("./examples")
p1 = p0.task_img(operation)
p2 = p1.save() # overwrite the images
p2.wait_for_completion()
```


### Check ongoing operation

```python
from olympict import ImagePipeline, Img

def operation(image: Img) -> Img:
    # set the green channel as a mean of blue and red channels
    img[:, :, 1] = (img[:, :, 0] + img[:, :, 2]) / 2
    return img

p0 = ImagePipeline.load_folder("./examples").debug_window("Raw image")
p1 = p0.task_img(operation).debug_window("Processed image")
p2 = p1.save() # overwrite the images
p2.wait_for_completion()
```

### Load a video and process each individual frame

```python
from olympict import VideoPipeline

p0 = VideoPipeline.load_folder("./examples") # will load .mp4 and .mkv files

p1 = p0.to_sequence() # split each video frame into a basic image

p2 = p1.resize((100, 3), (255, 255, 255)) # resize each image with white padding

p3 = p2.save_to_folder("./sequence") # save images individually

p3.wait_for_completion()

img_paths = glob("./sequence/*.png") # count images

print("Number of images:", len(img_paths))
```


### Complex example with preview windows
```python
import os
from random import randint
import re
import time
from olympict import ImagePipeline
from olympict.files.o_image import OlympImage


def img_simple_order(path: str) -> int:
    number_pattern = r"\d+"
    res = re.findall(number_pattern, os.path.basename(path))

    return int(res[0])


if __name__ == "__main__":

    def wait(x: OlympImage):
        time.sleep(0.1)
        print(x.path)
        return x

    def generator():
        for i in range(96):
            img = np.zeros((256, 256, 3), np.uint8)
            img[i, :, :] = (255, 255, 255)

            o = OlympImage()
            o.path = f'/tmp/{i}.png'
            o.img = img
            yield o
        return

    p = (
        ImagePipeline(generator())
        .task(wait)
        .debug_window("start it")
        .task_img(lambda x: x[::-1, :, :])
        .debug_window("flip it")
        .keep_each_frame_in(1, 3)
        .debug_window("stuttered")
        .draw_bboxes(
            lambda x: [
                (
                    (
                        randint(0, 50),
                        randint(0, 50),
                        randint(100, 200),
                        randint(100, 200),
                        "change",
                        0.5,
                    ),
                    (randint(0, 255), 25, 245),
                )
            ]
        )
        .debug_window("bboxed")
    )

    p.wait_for_completion()

```

This project is still an early version, feedback is very helpful.