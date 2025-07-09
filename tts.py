import time
import logging
from RealtimeTTS import TextToAudioStream, CoquiEngine


class TTS:
    def __init__(self, signals):
        self.stream = None
        self.engine = None
        self.voice_engines = {}  # voice path → engine map
        self.signals = signals
        self.API = self.API(self)
        self.enabled = True
        self.current_voice = None

        self.signals.tts_ready = False
        logging.info("[TTS] Initializing...")

        try:
            self._preload_voices(["voices/max.wav", "voices/zay.wav", "voices/tony.wav"])
            self.set_voice("voices/tony.wav")  # default
            self.signals.tts_ready = True
            logging.info("[TTS] Ready.")
        except Exception as e:
            logging.error(f"[TTS] Initialization failed: {e}")

    def _preload_voices(self, voice_paths):
        """Preload voice engines once at startup."""
        for path in voice_paths:
            try:
                self.voice_engines[path] = CoquiEngine(
                    use_deepspeed=True,
                    voice=path,
                    speed=1.1,
                )
                logging.info(f"[TTS] Preloaded voice: {path}")
            except Exception as e:
                logging.error(f"[TTS] Failed to preload {path}: {e}")

    def set_voice(self, voice_path):
        """Switch stream to preloaded voice engine."""
        if voice_path == self.current_voice:
            return

        if voice_path not in self.voice_engines:
            logging.error(f"[TTS] Voice not preloaded: {voice_path}")
            return

        self.current_voice = voice_path
        if self.stream:
            self.stream.stop()

        self.engine = self.voice_engines[voice_path]
        self.stream = TextToAudioStream(
            self.engine,
            on_audio_stream_start=self._on_audio_start,
            on_audio_stream_stop=self._on_audio_end,
        )
        logging.info(f"[TTS] Voice switched to: {voice_path}")

    def play(self, message):
        if not self.enabled or not message.strip():
            return

        try:
            self.signals.sio_queue.put(("current_message", message))
            self.stream.feed(message)
            self.stream.play_async()
            logging.info(f"[TTS] Playing: {message}")
        except Exception as e:
            logging.error(f"[TTS] Playback failed: {e}")

    def stop(self):
        try:
            if self.stream:
                self.stream.stop()
            self.signals.AI_speaking = False
            logging.info("[TTS] Playback stopped.")
        except Exception as e:
            logging.error(f"[TTS] Stop failed: {e}")

    def _on_audio_start(self):
        self.signals.AI_speaking = True
        logging.debug("[TTS] Audio playback started.")

    def _on_audio_end(self):
        self.signals.last_message_time = time.time()
        self.signals.AI_speaking = False
        logging.debug("[TTS] Audio playback ended.")

    class API:
        def __init__(self, outer):
            self.outer = outer

        def set_TTS_status(self, status: bool):
            self.outer.enabled = status
            if not status:
                self.outer.stop()
            self.outer.signals.sio_queue.put(("TTS_status", status))
            logging.info(f"[TTS] Status set to: {'enabled' if status else 'disabled'}.")

        def get_TTS_status(self):
            return self.outer.enabled

        def abort_current(self):
            self.outer.stop()
            logging.info("[TTS] Playback aborted.")
