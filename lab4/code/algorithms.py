import math
import time

class RasterAlgorithms:
    @staticmethod
    def step_by_step(x1, y1, x2, y2):
        """Пошаговы алгарытм"""
        points = []
        if x1 == x2:  # Вертыкальная лінія
            for y in range(min(y1, y2), max(y1, y2) + 1):
                points.append((x1, y))
            return points

        # Каэфіцыент нахілу
        k = (y2 - y1) / (x2 - x1)
        b = y1 - k * x1

        if abs(k) <= 1:
            # Пакроква па x
            for x in range(min(x1, x2), max(x1, x2) + 1):
                y = k * x + b
                points.append((x, round(y)))
        else:
            # Пакроква па y
            for y in range(min(y1, y2), max(y1, y2) + 1):
                x = (y - b) / k
                points.append((round(x), y))

        return points

    @staticmethod
    def dda(x1, y1, x2, y2):
        """Алгарытм ЦДА (Digital Differential Analyzer)"""
        points = []
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))

        if steps == 0:
            return [(x1, y1)]

        x_inc = dx / steps
        y_inc = dy / steps

        x, y = x1, y1
        for i in range(steps + 1):
            points.append((round(x), round(y)))
            x += x_inc
            y += y_inc

        return points

    @staticmethod
    def bresenham_line(x1, y1, x2, y2):
        """Алгарытм Брезенхема для адрэзка"""
        points = []
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        x, y = x1, y1
        x_step = 1 if x2 > x1 else -1
        y_step = 1 if y2 > y1 else -1

        if dx > dy:
            error = 2 * dy - dx
            for i in range(dx + 1):
                points.append((x, y))
                if error >= 0:
                    y += y_step
                    error -= 2 * dx
                error += 2 * dy
                x += x_step
        else:
            error = 2 * dx - dy
            for i in range(dy + 1):
                points.append((x, y))
                if error >= 0:
                    x += x_step
                    error -= 2 * dy
                error += 2 * dx
                y += y_step

        return points

    @staticmethod
    def castle_pitway(x1, y1, x2, y2):
        """Алгарытм Кастла-Пітвея для адрэзка"""
        points = []

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        # Вызначаем крокі для кожнай восі
        if x2 > x1:
            x_step = 1
        else:
            x_step = -1

        if y2 > y1:
            y_step = 1
        else:
            y_step = -1

        x, y = x1, y1

        # Асноўны выпадак: |k| < 1
        if dx > dy:
            error = 2 * dy - dx

            for i in range(dx + 1):
                points.append((x, y))

                if error >= 0:
                    y += y_step
                    error -= 2 * dx

                error += 2 * dy
                x += x_step
        else:
            # Асобны выпадак: |k| >= 1
            error = 2 * dx - dy

            for i in range(dy + 1):
                points.append((x, y))

                if error >= 0:
                    x += x_step
                    error -= 2 * dy

                error += 2 * dx
                y += y_step

        return points

    @staticmethod
    def bresenham_circle(xc, yc, r):
        """Алгарытм Брезенхема для акружнасці"""
        points = []
        x = 0
        y = r
        d = 3 - 2 * r

        # Дабаўляем 8 сіметрычных пунктаў
        def add_points(xc, yc, x, y):
            return [
                (xc + x, yc + y), (xc - x, yc + y),
                (xc + x, yc - y), (xc - x, yc - y),
                (xc + y, yc + x), (xc - y, yc + x),
                (xc + y, yc - x), (xc - y, yc - x)
            ]

        points.extend(add_points(xc, yc, x, y))

        while y >= x:
            x += 1
            if d > 0:
                y -= 1
                d = d + 4 * (x - y) + 10
            else:
                d = d + 4 * x + 6
            points.extend(add_points(xc, yc, x, y))

        return points

    # НОВЫЯ АЛГАРЫТМЫ ЗГЛАЖЖВАННЯ

    @staticmethod
    def wu_line(x1, y1, x2, y2):
        """Алгарытм Ву для зглажвання лініі"""
        points = []

        def plot_point(x, y, intensity):
            points.append((x, y, intensity))

        dx = x2 - x1
        dy = y2 - y1

        if abs(dx) > abs(dy):
            # Гарызантальны выпадак
            if x2 < x1:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
                dx = -dx
                dy = -dy

            gradient = dy / dx if dx != 0 else 1
            y = y1

            for x in range(x1, x2 + 1):
                y_floor = math.floor(y)
                y_frac = y - y_floor

                plot_point(x, y_floor, 1 - y_frac)
                plot_point(x, y_floor + 1, y_frac)

                y += gradient
        else:
            # Вертыкальны выпадак
            if y2 < y1:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
                dx = -dx
                dy = -dy

            gradient = dx / dy if dy != 0 else 1
            x = x1

            for y in range(y1, y2 + 1):
                x_floor = math.floor(x)
                x_frac = x - x_floor

                plot_point(x_floor, y, 1 - x_frac)
                plot_point(x_floor + 1, y, x_frac)

                x += gradient

        return points

    @staticmethod
    def smooth_step_by_step(x1, y1, x2, y2):
        """Згладжаны пакрокавы алгарытм"""
        points = []

        if x1 == x2:  # Вертыкальная лінія
            for y in range(min(y1, y2), max(y1, y2) + 1):
                points.append((x1, y, 1.0))
            return points

        k = (y2 - y1) / (x2 - x1)
        b = y1 - k * x1

        if abs(k) <= 1:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                y_exact = k * x + b
                y_floor = math.floor(y_exact)
                y_frac = y_exact - y_floor

                points.append((x, y_floor, 1 - y_frac))
                points.append((x, y_floor + 1, y_frac))
        else:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                x_exact = (y - b) / k
                x_floor = math.floor(x_exact)
                x_frac = x_exact - x_floor

                points.append((x_floor, y, 1 - x_frac))
                points.append((x_floor + 1, y, x_frac))

        return points

    @staticmethod
    def gaussian_smooth_line(x1, y1, x2, y2, sigma=0.7):
        """Зглажванне з выкарыстаннем Гаусавага ядра"""
        points = []

        # Спачатку атрымліваем звычайную лінію
        base_points = RasterAlgorithms.bresenham_line(x1, y1, x2, y2)

        # Гаусава ядро для зглажвання
        kernel_size = 3
        kernel = []
        for i in range(-kernel_size, kernel_size + 1):
            weight = math.exp(-(i**2) / (2 * sigma**2))
            kernel.append((i, weight))

        # Нармалізуем ядро
        total_weight = sum(weight for _, weight in kernel)
        kernel = [(offset, weight/total_weight) for offset, weight in kernel]

        # Дабаўляем згладжаныя пункты
        for x, y in base_points:
            for x_offset, weight in kernel:
                for y_offset, weight2 in kernel:
                    combined_weight = weight * weight2
                    if combined_weight > 0.1:  # Ігнаруем вельмі малыя значэнні
                        points.append((x + x_offset, y + y_offset, combined_weight))

        return points

    @staticmethod
    def super_sampling_line(x1, y1, x2, y2, samples=2):
        """Супер-семплінг для зглажвання"""
        points = []

        # Маштабуем каардынаты
        scale = samples
        xx1, yy1 = x1 * scale, y1 * scale
        xx2, yy2 = x2 * scale, y2 * scale

        # Будуем лінію ў маштабаванай прасторы
        scaled_points = RasterAlgorithms.bresenham_line(xx1, yy1, xx2, yy2)

        # Зліваем семплы назад у зыходную прастору
        sample_grid = {}
        for sx, sy in scaled_points:
            orig_x, orig_y = sx // scale, sy // scale
            sample_x, sample_y = sx % scale, sy % scale

            key = (orig_x, orig_y)
            if key not in sample_grid:
                sample_grid[key] = []
            sample_grid[key].append((sample_x, sample_y))

        # Разлічваем інтэнсіўнасць для кожнага пікселя
        total_samples = scale * scale
        for (x, y), samples_list in sample_grid.items():
            intensity = len(samples_list) / total_samples
            points.append((x, y, intensity))

        return points

    # ДАПАМОЖНЫЯ МЕТАДЫ ДЛЯ ЗГЛАЖЖВАННЯ

    @staticmethod
    def normalize_intensity(points, max_intensity=1.0):
        """Нармалізацыя інтэнсіўнасці пунктаў"""
        if not points:
            return points

        # Знаходзім максімальную інтэнсіўнасць
        current_max = max(point[2] for point in points if len(point) > 2)

        if current_max == 0:
            return points

        # Нармалізуем
        scale_factor = max_intensity / current_max
        normalized_points = []
        for point in points:
            if len(point) == 3:
                x, y, intensity = point
                normalized_points.append((x, y, intensity * scale_factor))
            else:
                normalized_points.append(point)

        return normalized_points

    @staticmethod
    def apply_threshold(points, threshold=0.1):
        """Прымяняе парог да інтэнсіўнасці"""
        filtered_points = []
        for point in points:
            if len(point) == 3:
                x, y, intensity = point
                if intensity >= threshold:
                    filtered_points.append((x, y, intensity))
            else:
                filtered_points.append(point)
        return filtered_points

    @staticmethod
    def measure_time(algorithm, *args):
        """Вымярэнне часу выканання"""
        start_time = time.time()
        result = algorithm(*args)
        end_time = time.time()
        return result, (end_time - start_time) * 1000  # у мілісекундах
