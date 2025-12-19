from pydub import effects

def master_basic(audio):
    return effects.normalize(audio)

def master_advanced(audio, preset):
    audio = effects.normalize(audio)
    # Add stereo widen, compression, etc. here
    return audio
