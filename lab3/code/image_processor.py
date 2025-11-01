import numpy as np
import math

class ImageProcessor:
    @staticmethod
    def process_image(image, operation, params):
        try:
            if operation == "Лінейнае кантраставаньне":
                return ImageProcessor.linear_contrast(image)
            elif operation == "Павялічыць яркасць":
                return ImageProcessor.adjust_brightness(image, 1.5)
            elif operation == "Павялічыць кантраснасць":
                return ImageProcessor.adjust_contrast(image, 1.5)
            elif operation == "Мануальная парогавая апрацоўка":
                return ImageProcessor.manual_threshold(image, 127)
            elif operation == "Адаптыўная парогавая апрацоўка (Otsu)":
                return ImageProcessor.adaptive_threshold_otsu(image)
            elif operation == "Лякальная парогавая апрацоўка (Gaussian)":
                return ImageProcessor.local_threshold_gaussian(image)
            elif operation == "Лякальная парогавая апрацоўка (Mean)":
                return ImageProcessor.local_threshold_mean(image)
            elif operation == "Інвертаваць колеры":
                return ImageProcessor.invert_colors(image)
            elif operation == "Глабальная парогавая апрацоўка (Mean)":
                return ImageProcessor.global_threshold_mean(image)
            else:
                return image.copy()
        except Exception as e:
            print(f"Памылка апрацоўкі: {e}")
            return None

    @staticmethod
    def rgb_to_grayscale(image):
        if len(image.shape) == 3:
            gray = np.dot(image[..., :3], [0.299, 0.587, 0.114])
            return gray.astype(np.uint8)
        else:
            return image

    @staticmethod
    def grayscale_to_rgb(image):
        if len(image.shape) == 2:
            rgb = np.stack([image, image, image], axis=2)
            return rgb.astype(np.uint8)
        else:
            return image

    @staticmethod
    def linear_contrast(image):
        if len(image.shape) == 3:
            gray = ImageProcessor.rgb_to_grayscale(image)
        else:
            gray = image

        min_val = np.min(gray)
        max_val = np.max(gray)

        if max_val == min_val:
            return ImageProcessor.grayscale_to_rgb(gray)

        contrasted = np.zeros_like(gray, dtype=np.float32)
        for i in range(gray.shape[0]):
            for j in range(gray.shape[1]):
                contrasted[i, j] = ((gray[i, j] - min_val) / (max_val - min_val)) * 255

        contrasted = contrasted.astype(np.uint8)
        return ImageProcessor.grayscale_to_rgb(contrasted)

    @staticmethod
    def adjust_brightness(image, factor):
        result = np.zeros_like(image, dtype=np.float32)

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if len(image.shape) == 3:
                    for k in range(3):
                        result[i, j, k] = image[i, j, k] * factor
                else:
                    result[i, j] = image[i, j] * factor

        result = np.clip(result, 0, 255).astype(np.uint8)
        return result

    @staticmethod
    def adjust_contrast(image, factor):
        if len(image.shape) == 3:
            gray = ImageProcessor.rgb_to_grayscale(image)
        else:
            gray = image

        mean_brightness = np.mean(gray)

        result = np.zeros_like(image, dtype=np.float32)

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if len(image.shape) == 3:
                    for k in range(3):
                        result[i, j, k] = mean_brightness + (image[i, j, k] - mean_brightness) * factor
                else:
                    result[i, j] = mean_brightness + (image[i, j] - mean_brightness) * factor

        result = np.clip(result, 0, 255).astype(np.uint8)
        return result

    @staticmethod
    def manual_threshold(image, threshold_value):
        if len(image.shape) == 3:
            gray = ImageProcessor.rgb_to_grayscale(image)
        else:
            gray = image

        thresholded = np.zeros_like(gray)
        for i in range(gray.shape[0]):
            for j in range(gray.shape[1]):
                if gray[i, j] > threshold_value:
                    thresholded[i, j] = 255
                else:
                    thresholded[i, j] = 0

        return ImageProcessor.grayscale_to_rgb(thresholded)

    @staticmethod
    def adaptive_threshold_otsu(image):
        """
        Адаптыўная парогавая апрацоўка паводле формул з прэзентацыі
        """
        if len(image.shape) == 3:
            gray = ImageProcessor.rgb_to_grayscale(image)
        else:
            gray = image

        height, width = gray.shape
        result = np.zeros_like(gray)

        K = 3
        alpha = 2/3

        for i in range(height):
            for j in range(width):
                f_mn = gray[i, j]

                i_min = max(0, i - K)
                i_max = min(height, i + K + 1)
                j_min = max(0, j - K)
                j_max = min(width, j + K + 1)

                region = gray[i_min:i_max, j_min:j_max]

                f_max = np.max(region)
                f_min = np.min(region)
                P_hat = np.mean(region)

                delta_f_max = f_max - P_hat
                delta_f_min = abs(f_min - P_hat)

                if delta_f_max > delta_f_min:
                    t = alpha * (2/3 * f_min + 1/3 * P_hat)
                elif delta_f_max < delta_f_min:
                    t = alpha * (1/3 * f_min + 2/3 * P_hat)
                else:
                    if f_max != f_min:
                        K_temp = K + 1
                        i_min_temp = max(0, i - K_temp)
                        i_max_temp = min(height, i + K_temp + 1)
                        j_min_temp = max(0, j - K_temp)
                        j_max_temp = min(width, j + K_temp + 1)

                        region_temp = gray[i_min_temp:i_max_temp, j_min_temp:j_max_temp]
                        f_max_temp = np.max(region_temp)
                        f_min_temp = np.min(region_temp)
                        P_hat_temp = np.mean(region_temp)

                        delta_f_max_temp = f_max_temp - P_hat_temp
                        delta_f_min_temp = abs(f_min_temp - P_hat_temp)

                        if delta_f_max_temp > delta_f_min_temp:
                            t = alpha * (2/3 * f_min_temp + 1/3 * P_hat_temp)
                        elif delta_f_max_temp < delta_f_min_temp:
                            t = alpha * (1/3 * f_min_temp + 2/3 * P_hat_temp)
                        else:
                            t = alpha * P_hat_temp
                    else:
                        t = alpha * P_hat

                if abs(P_hat - f_mn) > t:
                    result[i, j] = 255
                else:
                    result[i, j] = 0

        return ImageProcessor.grayscale_to_rgb(result)

        thresholded = np.zeros_like(gray)
        for i in range(gray.shape[0]):
            for j in range(gray.shape[1]):
                if gray[i, j] > optimal_threshold:
                    thresholded[i, j] = 255
                else:
                    thresholded[i, j] = 0

        return ImageProcessor.grayscale_to_rgb(thresholded)

    @staticmethod
    def local_threshold_gaussian(image, block_size=11, C=2):
        if len(image.shape) == 3:
            gray = ImageProcessor.rgb_to_grayscale(image)
        else:
            gray = image

        thresholded = np.zeros_like(gray)
        half_block = block_size // 2

        for i in range(gray.shape[0]):
            for j in range(gray.shape[1]):
                i_min = max(0, i - half_block)
                i_max = min(gray.shape[0], i + half_block + 1)
                j_min = max(0, j - half_block)
                j_max = min(gray.shape[1], j + half_block + 1)

                region = gray[i_min:i_max, j_min:j_max]
                weights = np.zeros_like(region, dtype=np.float32)
                center_i = i - i_min
                center_j = j - j_min

                for x in range(region.shape[0]):
                    for y in range(region.shape[1]):
                        distance = math.sqrt((x - center_i)**2 + (y - center_j)**2)
                        weights[x, y] = math.exp(-(distance**2) / (2 * (block_size/4)**2))

                weights /= np.sum(weights)
                weighted_mean = np.sum(region * weights)

                if gray[i, j] > weighted_mean - C:
                    thresholded[i, j] = 255
                else:
                    thresholded[i, j] = 0

        return ImageProcessor.grayscale_to_rgb(thresholded)

    @staticmethod
    def local_threshold_mean(image, block_size=11, C=2):
        if len(image.shape) == 3:
            gray = ImageProcessor.rgb_to_grayscale(image)
        else:
            gray = image

        thresholded = np.zeros_like(gray)
        half_block = block_size // 2

        for i in range(gray.shape[0]):
            for j in range(gray.shape[1]):
                i_min = max(0, i - half_block)
                i_max = min(gray.shape[0], i + half_block + 1)
                j_min = max(0, j - half_block)
                j_max = min(gray.shape[1], j + half_block + 1)

                region = gray[i_min:i_max, j_min:j_max]
                local_mean = np.mean(region)

                if gray[i, j] > local_mean - C:
                    thresholded[i, j] = 255
                else:
                    thresholded[i, j] = 0

        return ImageProcessor.grayscale_to_rgb(thresholded)

    @staticmethod
    def invert_colors(image):
        result = np.zeros_like(image)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if len(image.shape) == 3:
                    for k in range(3):
                        result[i, j, k] = 255 - image[i, j, k]
                else:
                    result[i, j] = 255 - image[i, j]
        return result

    @staticmethod
    def global_threshold_mean(image):
        if len(image.shape) == 3:
            gray = ImageProcessor.rgb_to_grayscale(image)
        else:
            gray = image

        mean_val = np.mean(gray)
        thresholded = np.zeros_like(gray)
        for i in range(gray.shape[0]):
            for j in range(gray.shape[1]):
                if gray[i, j] > mean_val:
                    thresholded[i, j] = 255
                else:
                    thresholded[i, j] = 0

        return ImageProcessor.grayscale_to_rgb(thresholded)
