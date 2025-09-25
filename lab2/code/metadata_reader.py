from PIL import Image, ExifTags, TiffTags
from PIL.ExifTags import TAGS
import os
from datetime import datetime
from formats_info import infer_color_depth, get_dpi, get_compression_info, get_additional_info

class MetadataReader:
    """Клас для чытання метаданых з малюнкаў"""

    @staticmethod
    def get_image_metadata(file_path):
        """Атрымаць усю метаінфармацыю з малюнка"""
        try:
            with Image.open(file_path) as img:
                # Базавая інфармацыя
                basic_info = MetadataReader._get_basic_info(img, file_path)

                # EXIF даныя
                exif_data = MetadataReader._get_exif_data(img)

                # Даныя пэўныя для фармату з formats_info.py
                format_specific = MetadataReader._get_format_specific_data(img, file_path)

                # Дадатковая інфармацыя з formats_info.py
                additional_info = MetadataReader._get_additional_info(img)

                # Інфармацыя пра квантаванне
                quantization_info = MetadataReader._get_quantization_info(img)

                # Аб'яднанне ўсіх даных
                all_metadata = {**basic_info, **exif_data, **format_specific, **additional_info, **quantization_info}

                return all_metadata

        except Exception as e:
            return {"error": f"Памылка чытання: {str(e)}"}

    @staticmethod
    def _get_basic_info(img, file_path):
        """Атрымаць базавую інфармацыю пра малюнак"""
        file_stats = os.stat(file_path)

        return {
            "filename": os.path.basename(file_path),
            "file_path": file_path,  # Поўны шлях
            "file_size": f"{file_stats.st_size / 1024:.2f} KB",
            "file_size_bytes": file_stats.st_size,
            "file_modified": datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            "image_format": img.format,
            "image_mode": img.mode,
            "image_size": f"{img.width} × {img.height} px",
            "width": img.width,
            "height": img.height,
            "has_alpha": "Так" if img.mode in ('RGBA', 'LA', 'P') else "Не"
        }

    @staticmethod
    def _get_format_specific_data(img, file_path):
        """Атрымаць даныя спецыфічныя для фармату з formats_info.py"""
        specific_data = {}

        try:
            # Выкарыстоўваем функцыі з formats_info.py
            # Глыбіня колеру
            color_depth = infer_color_depth(img)
            specific_data['color_depth'] = f"{color_depth} біт"
            specific_data['color_depth_value'] = color_depth

            # Дазвол (DPI)
            dpi_x, dpi_y = get_dpi(img)
            if dpi_x and dpi_y:
                specific_data['dpi'] = f"{dpi_x:.1f} × {dpi_y:.1f} DPI"
                specific_data['dpi_x'] = dpi_x
                specific_data['dpi_y'] = dpi_y
            else:
                specific_data['dpi'] = "Не вызначана"

            # Інфармацыя пра сціск
            compression = get_compression_info(img)
            if compression:
                specific_data['compression'] = compression
            else:
                specific_data['compression'] = "Не вызначана"

        except Exception as e:
            specific_data["format_specific_error"] = str(e)

        return specific_data

    @staticmethod
    def _get_additional_info(img):
        """Атрымаць дадатковую інфармацыю з formats_info.py"""
        additional_data = {}

        try:
            additional_info = get_additional_info(img)

            # EXIF даныя
            if 'exif_keys_count' in additional_info:
                additional_data['exif_keys_count'] = additional_info['exif_keys_count']

            if 'exif_sample' in additional_info:
                additional_data['exif_sample'] = additional_info['exif_sample']

            # JPEG quantization tables
            if 'jpeg_quant_tables' in additional_info:
                additional_data['jpeg_quantization_tables'] = additional_info['jpeg_quant_tables']

            # GIF palette
            if 'gif_palette_colors' in additional_info:
                additional_data['gif_palette_colors'] = additional_info['gif_palette_colors']

            if 'gif_frames' in additional_info:
                additional_data['gif_frames_count'] = additional_info['gif_frames']

        except Exception as e:
            additional_data["additional_info_error"] = str(e)

        return additional_data

    @staticmethod
    def _get_exif_data(img):
        """Атрымаць EXIF метаданыя (захавана для сумяшчальнасці)"""
        exif_data = {}

        try:
            if hasattr(img, '_getexif') and img._getexif():
                for tag_id, value in img._getexif().items():
                    tag_name = TAGS.get(tag_id, tag_id)

                    # Канвертаваць нестандартныя тыпы даных
                    if isinstance(value, bytes):
                        try:
                            value = value.decode('utf-8', errors='ignore')
                        except:
                            value = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)

                    exif_data[f"EXIF_{tag_name}"] = value

        except Exception as e:
            exif_data["exif_error"] = f"EXIF памылка: {str(e)}"

        return exif_data

    # Старыя метады захаваны для сумяшчальнасці
    @staticmethod
    def _get_jpeg_info(img):
        """JPEG-спецыфічная інфармацыя (захавана для сумяшчальнасці)"""
        jpeg_info = {}

        try:
            # Спрабуем атрымаць якасць сціску
            if hasattr(img, 'quality'):
                jpeg_info['compression_quality'] = f"{getattr(img, 'quality', 'Невядома')}%"

            # Інфармацыя пра JFIF
            if hasattr(img, 'info'):
                info = img.info
                jpeg_info['jfif_version'] = info.get('jfif_version', 'Не JFIF')

        except Exception as e:
            jpeg_info['jpeg_error'] = str(e)

        return jpeg_info

    @staticmethod
    def _get_gif_info(img):
        """GIF-спецыфічная інфармацыя (захавана для сумяшчальнасці)"""
        gif_info = {}

        try:
            if hasattr(img, 'info'):
                info = img.info
                gif_info['version'] = info.get('version', 'GIF89a')
                gif_info['background'] = info.get('background', 'Невядома')
                gif_info['duration'] = f"{info.get('duration', 0)} ms"
                gif_info['loop'] = info.get('loop', 0)

        except Exception as e:
            gif_info['gif_error'] = str(e)

        return gif_info

    @staticmethod
    def _get_png_info(img):
        """PNG-спецыфічная інфармацыя (захавана для сумяшчальнасці)"""
        png_info = {}

        try:
            if hasattr(img, 'info'):
                info = img.info
                png_info['gamma'] = info.get('gamma', 'Невядома')

        except Exception as e:
            png_info['png_error'] = str(e)

        return png_info

    @staticmethod
    def _get_tiff_info(img):
        """TIFF-спецыфічная інфармацыя (захавана для сумяшчальнасці)"""
        return {"format_note": "TIFF формат"}

    @staticmethod
    def _get_bmp_info(img):
        """BMP-спецыфічная інфармацыя (захавана для сумяшчальнасці)"""
        return {"format_note": "Windows Bitmap"}

    @staticmethod
    def _get_pcx_info(img):
        """PCX-спецыфічная інфармацыя (захавана для сумяшчальнасці)"""
        return {"format_note": "PC Paintbrush"}

    @staticmethod
    def _get_quantization_info(img):
        """Атрымаць інфармацыю пра квантаванне"""
        quantization_info = {}

        try:
            # Для JPEG файлаў
            if img.format == "JPEG" and hasattr(img, 'quantization') and img.quantization:
                tables = img.quantization
                if tables:
                    # Колькасць табліц квантавання
                    quantization_info['quantization_tables_count'] = len(tables)

                    # Памер табліц (звычайна 64 для 8x8 блокаў)
                    table_sizes = []
                    for table_id, table_data in tables.items():
                        if table_data:
                            table_sizes.append(len(table_data))

                    if table_sizes:
                        quantization_info['quantization_table_size'] = f"{table_sizes[0]} coefficients"

                    # Кароткая інфармацыя для табліцы
                    quantization_info['quantization_short'] = f"JPEG {len(tables)} табліц"
                else:
                    quantization_info['quantization_short'] = "Без квантавання"
            else:
                quantization_info['quantization_short'] = "Не ўжываецца"

        except Exception as e:
            quantization_info['quantization_short'] = "Памылка чытання"
            quantization_info['quantization_error'] = str(e)

        return quantization_info
