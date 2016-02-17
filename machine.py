
from trapepper import SpeechRecognition
from trapepper import QueryNormalizer
from trapepper import QueryParser
from trapepper import ActionDeterminer
from trapepper import QueryExecutor
from trapepper import ResponseGenerator
from trapepper import SpeechSynthesizer

class DialogueMachine:
    def __init__(self, genre_list_path=None):
        # Modules
        self.recognizer = SpeechRecognition()
        self.normalizer = QueryNormalizer()
        self.parser = QueryParser(genre_list_path)
        self.action_determiner = ActionDeterminer()
        self.executor = QueryExecutor()
        self.response_generator = ResponseGenerator()
        self.speech_synthesizer = SpeechSynthesizer()
        
        # State
        self.last_state = None

    def loop(self):
        while True:
            inp = self.recognize()
            inp = self.normalize(inp)
            parsed = self.parse(inp)
    
            # action determiner
            action = self.comprehend(parsed, self.last_state)
    
            # backend 
            data = self.execute_query(action)

            # generate response
            response = self.generate_response(data)

            # speech synthesis
            self.synthesize(response)
            
            # Try for one iteration (delete later)
            break

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
        action_type, new_state = self.action_determiner.determine(parsed, last_state)
        self.last_state = new_state
        return action_type

    def execute_query(self, action):
        return self.executor.execute(action)

    def generate_response(self, data):
        return self.response_generator.generate_response(data)

    def synthesize(self, response_str):
        self.speech_synthesizer.synthesize(response_str)

