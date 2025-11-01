import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from metadata_reader import MetadataReader
from datetime import datetime

class ImageAnalyzer:
    """Клас для масавага аналізу малюнкаў"""

    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.supported_formats = {'.jpg', '.jpeg', '.gif', '.tif', '.tiff', '.bmp', '.png', '.pcx'}

    def analyze_folder(self, folder_path, progress_callback=None):
        """Прааналізаваць усю папку з малюнкамі"""
        if not os.path.exists(folder_path):
            return {"error": "Папка не існуе"}

        image_files = self._find_image_files(folder_path)
        total_files = len(image_files)

        if total_files == 0:
            return {"error": "Малюнкі не знойдзены"}

        results = []
        completed = 0

        # Выкарыстанне шматпаточнасці для хуткасці
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_file = {
                executor.submit(MetadataReader.get_image_metadata, file_path): file_path
                for file_path in image_files
            }

            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    metadata = future.result()
                    metadata['file_path'] = file_path
                    results.append(metadata)

                    completed += 1
                    if progress_callback:
                        progress_callback(completed, total_files, os.path.basename(file_path))

                except Exception as e:
                    error_result = {
                        'filename': os.path.basename(file_path),
                        'error': str(e),
                        'file_path': file_path
                    }
                    results.append(error_result)

        return {
            'summary': {
                'total_files': total_files,
                'processed': len(results),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'folder_path': folder_path
            },
            'results': results
        }

    def _find_image_files(self, folder_path):
        """Знайсці ўсе падтрымоўваемыя файлы малюнкаў"""
        image_files = []

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext in self.supported_formats:
                    full_path = os.path.join(root, file)
                    image_files.append(full_path)

        return image_files

    def get_summary_stats(self, results):
        """Атрымаць статыстыку па выніках"""
        if 'results' not in results:
            return {}

        successful = [r for r in results['results'] if 'error' not in r]
        errors = [r for r in results['results'] if 'error' in r]

        formats = {}
        for result in successful:
            fmt = result.get('image_format', 'Невядома')
            formats[fmt] = formats.get(fmt, 0) + 1

        return {
            'successful': len(successful),
            'errors': len(errors),
            'formats': formats,
            'total_size': f"{sum(os.path.getsize(r['file_path']) for r in successful) / (1024*1024):.2f} MB"
        }
