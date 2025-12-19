from spleeter.separator import Separator
from pydub import AudioSegment

def separate_stems_premium(beat_path, vocal_paths):
    separator = Separator('spleeter:4stems')
    output_dir = "/tmp/spleeter_output"
    os.makedirs(output_dir, exist_ok=True)
    separator.separate_to_file(beat_path, output_dir)

    # Combine vocals
    vocal_audio = [AudioSegment.from_file(v).normalize() for v in vocal_paths]
    beat_audio = AudioSegment.from_file(os.path.join(output_dir, "accompaniment.wav"))
    return beat_audio, vocal_audio
