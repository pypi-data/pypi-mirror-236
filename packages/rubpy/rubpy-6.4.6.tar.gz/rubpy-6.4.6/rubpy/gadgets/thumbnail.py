import base64
import tempfile

try:
    import cv2
    import numpy
except ImportError:
    cv2 = None
    numpy = None

class Thumbnail:
    def __init__(self, image: bytes, width: int = 200, height: int = 200, seconds: int = 1, *args, **kwargs) -> None:
        self.image = image
        self.width = width
        self.height = height
        self.seconds = seconds

        # اگر image به عنوان یک مسیر فایل داده شده است، آن را بخوانید
        if isinstance(self.image, str):
            with open(image, 'rb') as file:
                self.image = file.read()

    def to_base64(self, *args, **kwargs) -> str:
        if self.image is not None:
            return base64.b64encode(self.image).decode('utf-8')

class MakeThumbnail(Thumbnail):
    def __init__(self, image, width: int = 200, height: int = 200, seconds: int = 1, *args, **kwargs) -> None:
        self.image = None
        self.width = width
        self.height = height
        self.seconds = seconds

        if hasattr(cv2, 'imdecode'):
            # اگر image یک آرایه numpy نبود، آن را به آرایه تبدیل کنید و سپس تصویر را بسازید
            if not isinstance(image, numpy.ndarray):
                image = numpy.frombuffer(image, dtype=numpy.uint8)
                image = cv2.imdecode(image, flags=1)

            self.image = self.ndarray_to_bytes(image)

    def ndarray_to_bytes(self, image, *args, **kwargs) -> bytes:
        if hasattr(cv2, 'resize'):
            # تغییر اندازه تصویر به ابعاد مورد نظر
            self.width = image.shape[1]
            self.height = image.shape[0]
            image = cv2.resize(image,
                               (round(self.width / 10), round(self.height / 10)),
                               interpolation=cv2.INTER_CUBIC)

            _, buffer = cv2.imencode('.png', image)
            if _:
                return buffer.tobytes()

    @classmethod
    def from_video(cls, video: bytes, *args, **kwargs):
        if hasattr(cv2, 'VideoCapture'):
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as file:
                file.write(video)
                file_path = file.name
                capture = cv2.VideoCapture(file_path)
                fps = int(capture.get(cv2.CAP_PROP_FPS))
                frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
                duration_in_seconds = frames / fps
                _, image = capture.read()
                if image is not None:
                    return MakeThumbnail(image=image, seconds=int(duration_in_seconds) * 1000, *args, **kwargs)