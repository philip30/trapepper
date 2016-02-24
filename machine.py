
import sys
from trapepper import SpeechRecognition
from trapepper import QueryNormalizer
from trapepper import QueryParser
from trapepper import ActionDeterminer
from trapepper import QueryExecutor
from trapepper import ResponseGenerator
from trapepper import SpeechSynthesizer
from trapepper import ResultFilterer
from trapepper.util import log
from trapepper.lib import ActionType

class DialogueMachine:
    def __init__(self, genre_list_path=None, debug=False):
        # Modules
        self.recognizer = SpeechRecognition(debug)
        self.normalizer = QueryNormalizer()
        self.parser = QueryParser(genre_list_path)
        self.action_determiner = ActionDeterminer()
        self.executor = QueryExecutor()
        self.filterer = ResultFilterer()
        self.response_generator = ResponseGenerator()
        self.speech_synthesizer = SpeechSynthesizer()

    def loop(self):
        data = None
        state = None
        while True:
            inp = self.recognize()
            if inp is None: break
            inp = self.normalize(inp)
            parsed = self.parse(inp)
    
            # action determiner
            action, state = self.comprehend(parsed, state)
            
            # backend
            data = self.execute_query(action, state, data)
            
            # generate response
            response = self.generate_response(action, data, state)

            # speech synthesis
            self.synthesize(response)
            log("==============================================================")
            
    # speech recognition 
    def recognize(self):
        return self.recognizer.recognize()

    # query normalizer
    def normalize(self, inp):
        return self.normalizer.normalize(inp)

    # query parser
    def parse(self, inp):
        return self.parser.parse(inp)

    # state transition
    def comprehend(self, parsed, last_state):
        action, new_state = self.action_determiner.determine(parsed, last_state)
        log("Action Type:", action)
        return action, new_state

    def execute_query(self, action, state, data):
        # Do a new query:
        if action.action_type == ActionType.exec_rest:
            self.synthesize(["レストランを探しますね。"])
            data = self.executor.execute(action)
            self.filterer.reset(data)
        
        data, modified = self.filterer.filter(state)

        if not modified:
            pass # do something with the action?
        return data

    def generate_response(self, action, data, filt):
        if filt is not None: filt = filt["entities"]["filter"]
        return self.response_generator.generate_response(action, data, filt)

    def synthesize(self, responses):
        for response_str in responses:
            self.speech_synthesizer.synthesize(response_str)

