import Image
import ImageDraw
import ImageEnhance


def watermark_processor(image, watermark=False, **kwargs):
    """
    Add a watermark to the image
    """
    if watermark:
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
