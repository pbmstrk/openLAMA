import logging
from logger.logger import set_logger
import jsonlines
import json
import os.path

def formatLAMAsquad(path):

    cloze_questions = []
    targets = []
    ids = []
    
    with jsonlines.open(path) as reader:
        for obj in reader:
            cloze_questions.append(obj["masked_sentences"][0])
            targets.append(obj["obj_label"])
            ids.append(obj["id"])

    return {"cq": cloze_questions, "targets": targets, "ids": ids}

def formatsquad(path):
    squad_questions = []
    squad_ids = []

    with open(path) as json_file:
        data = json.load(json_file)
        for article in data['data']:
            for paragraph in article["paragraphs"]:
                for qa in paragraph["qas"]:
                    squad_questions.append(qa["question"])
                    squad_ids.append(qa["id"])

    return {squad_ids[i]: squad_questions[i] for i in range(len(squad_ids))} 

def openlama_squad(lamapath, squadpath, squad_outputh_path):

    if os.path.isfile(squad_outputh_path):
        logging.info("%s exists, skipping processing" % squad_outputh_path)
        return 

    lamadict = formatLAMAsquad(lamapath)
    squaddict = formatsquad(squadpath)
    targets = lamadict["targets"]

    questions = [squaddict[lamadict["ids"][i][:-2]] for i in range(len(lamadict["ids"]))]

    with open(squad_outputh_path, 'a') as outfile:
        for i in range(len(questions)):
            data = {"question": questions[i], "answer": [targets[i]]}
            json.dump(data, outfile)
            outfile.write('\n')


def get_triples(path, relation):

    triples = []

    with jsonlines.open(path) as reader:
        for item in reader:
            sub = item["sub_label"]
            obj = item["obj_label"]
            triples.append((relation, sub, obj))
    
    return triples

def openlama_fill_template(path, output_path, relation, template):

    if os.path.isfile(output_path):
        logging.info("%s exists, skipping processing" % output_path)
        return

    triples = get_triples(path, relation)

    questions = []
    answers = []

    for triple in triples:
        relation, sub, obj = triple
        questions.append(template[relation].replace("[X]", sub))
        answers.append(obj)

    with open(output_path, 'a') as outfile:
        for i in range(len(questions)):
            data = {"question": questions[i], "answer": [answers[i]]}
            json.dump(data, outfile)
            outfile.write('\n')


if __name__ == "__main__":
    
    set_logger("convert.log")

    logging.info("Processing LAMA Squad dataset")
    openlama_squad("./data/LAMA/Squad/test.jsonl", "./data/SQUAD/dev-v1.1.json", "./openLAMA/SQUAD/squad.txt")

    with open("templates/google_re.json") as JSON:
        re_template = json.load(JSON)

    logging.info("Processing LAMA Google-RE dataset")
    openlama_fill_template("data/LAMA/Google_RE/place_of_birth_test.jsonl", "./openLAMA/Google_RE/place_of_birth.txt", "place_of_birth", re_template)
    openlama_fill_template("data/LAMA/Google_RE/place_of_death_test.jsonl", "./openLAMA/Google_RE/place_of_death.txt", "place_of_death", re_template)
    openlama_fill_template("data/LAMA/Google_RE/date_of_birth_test.jsonl", "./openLAMA/Google_RE/date_of_birth.txt", "date_of_birth", re_template)

    with open("templates/trex.json") as JSON:
        trex_template = json.load(JSON)

    relations = ["P17", "P19", "P20", "P27", "P30", "P31", "P36", "P37", "P39", "P103", "P127", "P131", 
                "P136", "P138", "P140", "P159", "P176", "P264", "P276", "P279", "P361", "P364", "P407", 
                "P413", "P449", "P495", "P740", "P1376"]

    for relation in relations:
        filepath = "data/LAMA/TREX/" + relation + ".jsonl"
        outputpath = "openLAMA/trex/" + relation + ".txt"
        openlama_fill_template(filepath, outputpath, relation, trex_template)
    


