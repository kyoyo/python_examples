from gtts import gTTS
from io import BytesIO
import urllib3

urllib3.disable_warnings()

mp3_fp = BytesIO()
tts = gTTS('hello', 'en')
tts.write_to_fp(mp3_fp)