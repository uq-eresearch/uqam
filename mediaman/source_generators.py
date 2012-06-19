try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from PIL import Image as PilImage
from pgmagick import Image, Blob
import logging

logger = logging.getLogger(__name__)


def pgmagick_image(source, **options):
    """
    Try to open the source file using pgmagick, ignoring any errors.

    """
    # Use a StringIO wrapper because if the source is an incomplete file like
    # object, PIL may have problems with it. For example, some image types
    # require tell and seek methods that are not present on all storage
    # File objects.
#    import ipdb; ipdb.set_trace()
    if not source:
        return
    source.open()  # If tried by a previous source_generator, will be closed
    source = StringIO(source.read())
    try:
        blob = Blob(source.read())
        image = Image(blob)
    except Exception:
        logger.exception("unable to read image to create thumbnail")
        return

    if not image.isValid():
        return

    return convertGMtoPIL(image)


def convertGMtoPIL(gmimage):
    """
    Convert GraphicsMagick image to PIL

    work with grayscale and colour
    """
    img = Image(gmimage)  # make copy
    gmimage.depth(8)
    img.magick("RGB")
    w, h = img.columns(), img.rows()
    blob = Blob()
    img.write(blob)
    data = blob.data

    # convert string array to an RGB PIL image
    pilimage = PilImage.fromstring('RGB', (w, h), data)
    return pilimage
