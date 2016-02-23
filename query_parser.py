import re
import MeCab
import os
from collections import defaultdict

RESOURCE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources/small_search.tsv")

class QueryParser:
    def __init__(self, genre_list_path):
        
        self.genre2id = {}
        with open(genre_list_path, "r") as genre_list:
            for lst in genre_list:
                genre_id, genre_name = tuple(lst.strip().split())
                self.genre2id[genre_name] = genre_id

        self.mec = MeCab.Tagger("-Owakati")
        self.nearby_regex       = re.compile(r"(このあたり|このへん|この近く)")
        self.location_regex     = re.compile(r"(NAIST|奈良先端|奈良駅|京都駅|大阪駅|奈良|京都|大阪)")
        self.genre_regex        = re.compile("(" + "|".join(self.genre2id.keys()) + ")")
        self.requirements_regex = re.compile(r"(飲み放題)")
        self.price_low_regex    = re.compile(r"(安い)")
        self.price_high_regex    = re.compile(r"(高い)")
        self.closer_regex     = re.compile(r"(近い|もっと近)")

        self.where_regex    = re.compile(r"(どこ)")
        self.how_regex      = re.compile(r"(どうやって)")
        self.is_there_regex = re.compile(r"(ある|あり|探し)")
        self.which_regex    = re.compile(r"(どの)")
        self.details_regex  = re.compile(r"(詳しく|詳しい)")
        self.others_regex   = re.compile(r"(他の|他に|他は)")
        self.hello_regex    = re.compile(r"(こんにちは)")
        self.bye_regex      = re.compile(r"(さようなら|さよなら|バイバイ|ありがとう)")
        self.pardon_regex   = re.compile(r"(もう一度|聞こえない)")

    def guess_question_type(self, inp, words):
        for word in words:
            q = self.where_regex.findall(word)
            if q: return "where"
            q = self.how_regex.findall(word)
            if q or "どうやって" in inp: return "how" # TODO parser cant handle this word because tokenizer split this word into 3 parts
            q = self.is_there_regex.findall(word)
            if q: return "is_there"
            q = self.which_regex.findall(word)
            if q: return "which"
        return None

    def guess_query_type(self, inp, words):
        q = self.guess_question_type(inp, words)
        if q: return "question"
        q = self.details_regex.findall(inp)
        if q: return "details"
        q = self.others_regex.findall(inp)
        if q: return "others"
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
        entities = defaultdict(str)

        if isinstance(inp, list):
            sentence = ''.join(inp)
            words    = inp
        else:
            sentence = inp
            words    = self.mec.parse(inp).strip().split()

        entities["looking_for"] = "restaurant"
        query_type   = self.guess_query_type(sentence, words)

        question     = self.guess_question_type(sentence, words)
        genre        = self.genre_regex.findall(sentence)
        requirements = self.requirements_regex.findall(sentence)

        location     = self.location_regex.findall(sentence)
        if location:     entities["location"]     = location[0]
        location     = self.nearby_regex.findall(sentence)
        if location:     entities["location"]     = "nearby"
        closer       = self.closer_regex.findall(sentence)
        if closer:       entities["location"] = "closer"
        if requirements: entities["requirements"] = requirements
        if question:     entities["question"] = question
        price        = self.price_low_regex.findall(sentence)
        if price:        entities["price"] = "low"
        price        = self.price_high_regex.findall(sentence)
        if price:        entities["price"] = "high"
        closer       = self.closer_regex.findall(sentence)
        if genre:
            entities["genre"]        = genre[0]
            entities["genre_id"]     = self.genre2id[genre[0]]

        result = {
                "query_type": query_type,
                "raw_tokens": words,
                "entities": entities
                }
        print(str(result))
        return result

def __main__():
    qparser = QueryParser(RESOURCE)
    inp = "このあたりにフランス料理のお店はありますか"
    inp = "奈良駅の近くにフランス料理のお店はありますか"
    print(qparser.parse(inp))

if __name__ == "__main__":
    __main__()
