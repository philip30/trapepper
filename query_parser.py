import re
import MeCab

class QueryParser:
    def __init__(self):
        self.mec = MeCab.Tagger("-Owakati")

        self.location_regex     = re.compile(r"(このあたり|NAIST|奈良|京都|大阪)")
        self.genre_regex        = re.compile(r"(フランス|スペイン|日本|中華|ドイツ|ラーメン)")
        self.requirements_regex = re.compile(r"(飲み放題)")

        self.question_regex = re.compile(r"(どこ|どうやって|ある|どの|あり)")
        self.details_regex  = re.compile(r"(詳しく|詳しい)")
        self.hello_regex    = re.compile(r"(こんにちは)")
        self.bye_regex      = re.compile(r"(さようなら|さよなら|バイバイ|ありがとう)")
        self.pardon_regex   = re.compile(r"(もう一度|聞こえない)")

    def guess_question_type(self, inp, words):
        for word in words:
            q = self.question_regex.findall(word)
            if q: return q[0]
        return None

    def guess_query_type(self, inp, words):
        q = self.guess_question_type(inp, words)
        if q: return "question"
        q = self.details_regex.findall(inp)
        if q: return "details"
        q = self.hello_regex.findall(inp)
        if q: return "hello"
        q = self.bye_regex.findall(inp)
        if q: return "bye"
        return "pardon"

    def parse(self, inp):
    ## query_type 
    #   question, details, hello, bye, pardon
    ## entities
    #   looking_for: "restaurant"
    #   genre: "french", "japanese", "italian", "ramen", "chinese", "german"
    #   requirements: "nomihodai"
    #   location: "nearby", "nara", "osaka", "kyoto"
    #   question: "where", "what", "which", "how"
        sentence, words = "", []
        if isinstance(inp, list):
            sentence = ''.join(inp)
            words    = inp
        else:
            sentence = inp
            words    = self.mec.parse(inp).strip().split()

        entities     = {"looking_for": "レストラン"}
        query_type   = self.guess_query_type(sentence, words)

        question     = self.guess_question_type(sentence, words)
        location     = self.location_regex.findall(sentence)
        genre        = self.genre_regex.findall(sentence)
        requirements = self.requirements_regex.findall(sentence)

        if location:     entities["location"]     = location[0]
        if genre:        entities["genre"]        = genre[0]
        if requirements: entities["requirements"] = requirements
        if question:     entities["question"] = question

        return {"query_type": query_type,
                "raw_tokens": words,
                "entities": entities
                }

def __main__():
    qparser = QueryParser()
    # print(qparser.parse(["where", "is", "the", "nearby", "french", "restaurant"]))
    inp = "このあたりにフランス料理のお店はありますか"
    print(qparser.parse(inp))

if __name__ == "__main__":
    __main__()
