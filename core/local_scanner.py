import os
import re

class LocalScanner:
    BASE_DIR = "/storage/emulated/0/Download/Animes"

    @staticmethod
    def ensure_directory_exists():
        try:
            if not os.path.exists(LocalScanner.BASE_DIR):
                os.makedirs(LocalScanner.BASE_DIR, exist_ok=True)
        except Exception as e:
            print(f"Erro ao verificar/criar diretório: {e}")

    @staticmethod
    def _clean_base_title(folder_name: str) -> str:
        patterns = [
            r'(?i)\s+season\s+\d+.*',
            r'(?i)\s+\d+nd\s+season.*',
            r'(?i)\s+\d+rd\s+season.*',
            r'(?i)\s+\d+th\s+season.*',
            r'(?i)\s+part\s+\d+.*',
            r'(?i)\s+dublado.*',
            r'(?i)\s+legendado.*',
            r'(?i)\s+ova.*'
        ]
        clean_name = folder_name
        for pattern in patterns:
            clean_name = re.sub(pattern, '', clean_name)
        return clean_name.strip()

    @staticmethod
    def get_local_animes_grouped():
        LocalScanner.ensure_directory_exists()

        if not os.path.exists(LocalScanner.BASE_DIR):
            return []

        grouped_animes = {}
        video_extensions = ('.mp4', '.mkv', '.avi', '.webm')

        try:
            folders = [f for f in os.listdir(LocalScanner.BASE_DIR) if os.path.isdir(os.path.join(LocalScanner.BASE_DIR, f))]

            for folder_name in folders:
                folder_path = os.path.join(LocalScanner.BASE_DIR, folder_name)
                episodes = []

                for root, _, files in os.walk(folder_path):
                    for file in sorted(files):
                        if file.lower().endswith(video_extensions):
                            episodes.append({
                                'title': os.path.splitext(file)[0],
                                'path': os.path.join(root, file)
                            })

                if not episodes:
                    continue

                main_title = LocalScanner._clean_base_title(folder_name)
                
                # Identificador único baseado no caminho real do diretório
                # Isso garante que pastas com mesmo nome ou conteúdos distintos não se misturem nem alterem os conteúdos de outras
                group_key = f"{main_title}_{folder_path}"

                season_label = folder_name.replace(main_title, '').strip()
                if not season_label:
                    season_label = "Temporada 1"

                season_data = {
                    'season_name': season_label,
                    'folder_path': folder_path,
                    'episodes': episodes
                }

                if group_key in grouped_animes:
                    grouped_animes[group_key]['seasons'].append(season_data)
                else:
                    grouped_animes[group_key] = {
                        'id': group_key,
                        'main_title': main_title,
                        'folder_path': folder_path,
                        'seasons': [season_data]
                    }

        except Exception as e:
            print(f"Erro ao escanear animes locais: {e}")

        return list(grouped_animes.values())
