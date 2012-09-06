import Image
import ImageDraw
import ImageEnhance
from django.conf import settings


def expand_canvas(image, size, expand=False, expand_colour="white", **kwargs):
    """
    Expand canvas of the image to the full requested size

    Centers the scaled image within the new canvas.
    Useful when using image sliders.
    """
    if expand:
        source_x, source_y = image.size
        target_x, target_y = size

        new_image = Image.new("RGB", size, expand_colour)

        if source_x < target_x:
            x1, y1 = ((target_x - source_x) / 2, 0)
        else:
            x1, y1 = (0, (target_y - source_y) / 2)

        new_image.paste(image, (x1, y1))
        return new_image
    else:
        return image


def watermark_overlay(image, watermark_image=None, wm_margin=15, **kwargs):
    # import ipdb; ipdb.set_trace()
    if watermark_image is None:
        return image
    overlay_path = settings.STATICFILES_DIRS[0] + '/' + watermark_image
    # import ipdb; ipdb.set_trace()
    overlay = Image.open(overlay_path)

    upperLeft = [(image.size[i] - overlay.size[i]) / 2 for i in [0, 1]]
    upperLeft = (image.size[0] - overlay.size[0] - wm_margin, image.size[1] - overlay.size[1] - wm_margin)
    image.paste(overlay, tuple(upperLeft), overlay)  # use overlay as image and mask
    return image


def watermark_processor(image, watermark=None, **kwargs):
    """
    Add a watermark to the image
    """
    if watermark is not None:
        image = watermark_image(image, watermark)
    return image


def watermark_image(im, text, font=None, color=None, opacity=0.6,
        margin=(30, 30)):
    """
    Adds an overlay of text to the image
    """
    textlayer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    textdraw = ImageDraw.Draw(textlayer)
    textsize = textdraw.textsize(text, font)
    textpos = [im.size[i] - textsize[i] - margin[i] for i in [0, 1]]
    textdraw.text(textpos, text, font=font, fill=color)
    if opacity != 1:
        textlayer = reduce_opacity(textlayer, opacity)
    return Image.composite(textlayer, im, textlayer)


def reduce_opacity(im, opacity):
    """
    Returns an image with reduced opacity.
    """
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im
