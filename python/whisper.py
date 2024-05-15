import sys
import json
from faster_whisper import WhisperModel
import os

def main(args):

    os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
    # Convertir l'argument JSON en un objet Python
    data = json.loads(args[0])

    # Extraire l'URL et le nom du modèle
    url = data['url']
    name = data['name']

    model = WhisperModel('tiny', device="cpu", compute_type="int8", download_root="models")

    segments, info = model.transcribe(url, beam_size=5)

    json_result = process_segments(segments, info)
    print(json_result)

def process_segments(segments, info):
    text = " ".join(segment.text for segment in segments)
    result = {
        "language": info.language,
        "language_probability": info.language_probability,
        "text": text
    }

    return json.dumps(result)

if __name__ == '__main__':
    main(sys.argv[1:])