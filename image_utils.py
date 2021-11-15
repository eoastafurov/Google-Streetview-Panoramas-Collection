import numpy as np


class ImageUtils:
    @staticmethod
    def remove_google_label_from_image(image: np.ndarray) -> np.ndarray:
        """
        height: int = 410,
        width: int = 640
        """
        height, width = image.shape[0], image.shape[1]
        return image[:int(height * 0.88), :]
