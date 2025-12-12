# clipping_algorithms.py
class LiangBarskyClipper:
    @staticmethod
    def clip_segment(segment, window):
        x1, y1, x2, y2 = segment
        xmin, ymin, xmax, ymax = window

        dx = x2 - x1
        dy = y2 - y1

        p = [-dx, dx, -dy, dy]
        q = [x1 - xmin, xmax - x1, y1 - ymin, ymax - y1]

        t1 = 0.0
        t2 = 1.0

        for i in range(4):
            if p[i] == 0:
                if q[i] < 0:
                    return None
                continue

            t = q[i] / p[i]

            if p[i] < 0:
                if t > t1:
                    t1 = t
            else:
                if t < t2:
                    t2 = t

            if t1 > t2:
                return None

        if t1 < t2:
            new_x1 = x1 + t1 * dx
            new_y1 = y1 + t1 * dy
            new_x2 = x1 + t2 * dx
            new_y2 = y1 + t2 * dy
            return [new_x1, new_y1, new_x2, new_y2]

        return None

class PolygonClipper:
    @staticmethod
    def clip_polygon(subject_polygon, clip_polygon):
        """Алгарытм Сазерленда-Ходжмана для адсячэння выпуклага мнагавугольніка"""
        if len(subject_polygon) < 3 or len(clip_polygon) < 3:
            return []

        # Пачынаем з суб'ект-мнагавугольніка
        output_polygon = subject_polygon.copy()

        # Адсякаем кожным бокам clip-мнагавугольніка
        for i in range(len(clip_polygon)):
            clip_edge_start = clip_polygon[i]
            clip_edge_end = clip_polygon[(i + 1) % len(clip_polygon)]

            input_list = output_polygon
            output_polygon = []

            if not input_list:
                break

            # Бяром апошнюю кропку
            s = input_list[-1]

            for e in input_list:
                # Правяраем ці знаходзіцца кропка e ўнутры clip-боку
                if PolygonClipper.is_inside(e, clip_edge_start, clip_edge_end):
                    if not PolygonClipper.is_inside(s, clip_edge_start, clip_edge_end):
                        # Дадаем кропку перасячэння
                        intersection = PolygonClipper.line_intersection(s, e, clip_edge_start, clip_edge_end)
                        if intersection:
                            output_polygon.append(intersection)
                    output_polygon.append(e)
                elif PolygonClipper.is_inside(s, clip_edge_start, clip_edge_end):
                    # Дадаем кропку перасячэння
                    intersection = PolygonClipper.line_intersection(s, e, clip_edge_start, clip_edge_end)
                    if intersection:
                        output_polygon.append(intersection)
                s = e

        return output_polygon

    @staticmethod
    def is_inside(point, edge_start, edge_end):
        """Правярае ці знаходзіцца кропка злева ад боку (для выпуклага мнагавугольніка)"""
        x, y = point
        x1, y1 = edge_start
        x2, y2 = edge_end

        # Вектарны здабытак для вызначэння становішча кропкі
        return (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1) >= 0

    @staticmethod
    def line_intersection(p1, p2, p3, p4):
        """Знаходзім кропку перасячэння двух адрэзкаў"""
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4

        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(denom) < 1e-10:
            return None

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom

        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)

        return (x, y)

class PolygonLineClipper:
    @staticmethod
    def clip_segment_by_polygon(segment, polygon):
        """Алгарытм адсячэння адрэзка выпуклым мнагавугольнікам"""
        if len(polygon) < 3:
            return None

        x1, y1, x2, y2 = segment

        # Калі абодва канцы ўнутры - вяртаем увесь адрэзак
        start_inside = PolygonLineClipper.is_point_inside_polygon((x1, y1), polygon)
        end_inside = PolygonLineClipper.is_point_inside_polygon((x2, y2), polygon)

        if start_inside and end_inside:
            return [x1, y1, x2, y2]

        return None

    @staticmethod
    def is_point_inside_polygon(point, polygon):
        """Правярае ці знаходзіцца кропка ўнутры мнагавугольніка"""
        x, y = point
        n = len(polygon)
        inside = False

        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            if ((p1y <= y and y < p2y) or (p2y <= y and y < p1y)) and \
               (x < (p2x - p1x) * (y - p1y) / (p2y - p1y) + p1x):
                inside = not inside
            p1x, p1y = p2x, p2y

        return inside
