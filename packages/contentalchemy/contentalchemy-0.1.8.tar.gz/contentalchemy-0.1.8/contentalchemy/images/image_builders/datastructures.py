import base64
import json
import re
from re import Match
from urllib.parse import urlencode, quote

from bs4 import BeautifulSoup
from dataclasses import dataclass
import os
from io import BytesIO
from typing import Dict, Any, Callable, Optional

from pydantic import BaseModel
from PIL import Image
import requests


class SpriteData(BaseModel):
    x: Optional[int]
    y: Optional[int]
    width: Optional[int]
    height: Optional[int]

    class Config:
        allow_mutation = False
        frozen = True


# @dataclass_json
# @dataclass
class ImageSprite(BaseModel):
    link: str
    data: SpriteData

    class Config:
        allow_mutation = False
        frozen = True

    def file_extension(self):
        filename = os.path.basename(self.link)
        file_extension = filename.split('.')[-1]
        return file_extension

    def sprite_bin(self):
        filename = os.path.basename(self.link)
        file_extension = filename.split('.')[-1]
        res = requests.get(self.link, allow_redirects=True)
        if res.status_code != 200:
            return None
        full_size_content = res.content
        bin_file = BytesIO(full_size_content)
        image = Image.open(bin_file)
        left = self.data.x
        top = self.data.y
        right = self.data.x + self.data.width
        bottom = self.data.y + self.data.height
        cropped_image = image.crop((left, top, right, bottom))
        with BytesIO() as output:
            cropped_image.save(output, format=file_extension)
            cropped_data = output.getvalue()
        return cropped_data

    def relative_path(self):
        filename = os.path.basename(self.link)
        rel_path = f'image_{self.data.x}_{self.data.y}_{self.data.width}_{self.data.height}_{filename}'
        return rel_path

    def migrated_url(self, image_endpoint: str):
        relative_path = self.relative_path()
        img_url = f'{image_endpoint}/{relative_path}'
        return img_url

    def cropped_url(self, image_endpoint: str):
        if not image_endpoint:
            return ''
        if not self.link:
            return ''
        if not self.data.width or not self.data.height:
            return self.link
        if self.data.width == -1 or self.data.height == -1:
            return self.link
        params = dict(left=0, top=0, quality=100, url=self.link, areawidth=self.data.width, areaheight=self.data.height)
        if self.data.x:
            params['left'] = self.data.x
        if self.data.y:
            params['top'] = self.data.y
        encoded_params = urlencode(params)
        img_url = f'{image_endpoint}?{encoded_params}'
        return img_url


class ImageSpriteHandler(BaseModel):
    cropped_image_endpoint: Optional[str]
    migrated_image_endpoint: Optional[str]

    def build_migrated_url(self, image_sprite: ImageSprite):
        if self.migrated_image_endpoint:
            return image_sprite.migrated_url(self.migrated_image_endpoint)
        return ''

    def build_cropped_url(self, image_sprite: ImageSprite):
        if self.cropped_image_endpoint:
            return image_sprite.cropped_url(self.cropped_image_endpoint)
        return ''

    def embed_inline_cropped_img_tag(self, sprite_input: re.Match):
        sprite_content = sprite_input.group(1)
        if sprite_content:
            sprite_json = json.loads(sprite_content)
            sprite = ImageSprite.parse_obj(sprite_json)
            img_url = self.build_cropped_url(sprite)
            return f'<img class="cropped-image-sprite" src="{img_url}">' if img_url else img_url
        return sprite_input.group()

    def embed_inline_migrated_img_tag(self, sprite_input: re.Match):
        sprite_content = sprite_input.group(1)
        if sprite_content:
            sprite_json = json.loads(sprite_content)
            sprite = ImageSprite.parse_obj(sprite_json)
            img_url = self.build_migrated_url(sprite)
            return f'<img class="migrated-image-sprite" src="{img_url}">' if img_url else img_url
        return sprite_input.group()

    def embed_migrated_image_tags(self, embedded_str: str, img_sprite_regex: str):
        clean_embedded_str = embedded_str.replace('\n', '').replace('\t', '').strip()
        # img_sprite_regex = r"@\[\](.*?)@\[\]"
        content = re.sub(img_sprite_regex, self.embed_inline_migrated_img_tag, clean_embedded_str)
        return content

    def embed_cropped_image_tags(self, embedded_str: str, img_sprite_regex: str):
        clean_embedded_str = embedded_str.replace('\n', '').replace('\t', '').strip()
        # img_sprite_regex = r"@\[\](.*?)@\[\]"
        content = re.sub(img_sprite_regex, self.embed_inline_cropped_img_tag, clean_embedded_str)
        return content

