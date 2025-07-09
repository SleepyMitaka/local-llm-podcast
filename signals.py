import queue


class Signals:
    def __init__(self):
        self._AI_speaking = False
        self._AI_thinking = False
        self._tts_ready = False
        self._history = []
        self._terminate = False
        self.sio_queue = queue.SimpleQueue()

    @property
    def AI_speaking(self):
        return self._AI_speaking

    @AI_speaking.setter
    def AI_speaking(self, value):
        self._AI_speaking = value
        self.sio_queue.put(('AI_speaking', value))
        if value:
            print("agent: Talking Start")
        else:
            print("agent: Talking Stop")

    @property
    def AI_thinking(self):
        return self._AI_thinking

    @AI_thinking.setter
    def AI_thinking(self, value):
        self._AI_thinking = value
        self.sio_queue.put(('AI_thinking', value))
        if value:
            print("agent: Thinking Start")
        else:
            print("agent: thinking stop")

   

    @property
    def tts_ready(self):
        return self._tts_ready

    @tts_ready.setter
    def tts_ready(self, value):
        self._tts_ready = value

    @property
    def stt_ready(self):
        return self._stt_ready

  
    @property
    def terminate(self):
        return self._terminate

    @terminate.setter
    def terminate(self, value):
        self._terminate = value
