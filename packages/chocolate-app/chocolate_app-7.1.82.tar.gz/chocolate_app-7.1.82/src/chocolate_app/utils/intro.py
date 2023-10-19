import recurring_content_detector as rcd
import csv, os

# Liste des fichiers vidéo
videos = "/media/Dockarr/downloads-vpn/media/Séries/Malcolm/Season 1/"
artifacts_dir = "/var/chocolate/artifacts/"
videos = os.listdir(videos)
results = rcd.detect(videos, artifacts_dir=artifacts_dir, resize_width=240)

print(results)
