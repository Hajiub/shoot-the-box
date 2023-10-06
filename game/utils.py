import pygame as pg
import os

main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(file, scale=1):
    file = os.path.join(main_dir, 'imgs', file)
    try:
        image = pg.image.load(file)
    except pg.error as e:
        raise ValueError(f"Couldn't load {file} due to {str(e)}")
    
    # Scale the image
    size = image.get_size()
    size = (int(size[0] * scale), int(size[1] * scale))
    image = pg.transform.scale(image, size)
    
    return image, image.get_rect()


def load_sound(file):
    if not pg.mixer:
        return None
    file = os.path.join(main_dir, "audio", file)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error as e:
        print(f"Warning, unable to load, {file}")
    return None
    