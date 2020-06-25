import logging
import json
import os.path
import jsonlines
from logger.logger import set_logger



def formatLAMAsquad(path):

    """
    Opens LAMA Squad file and returns dictionary with
    questions, targets and ids.
    """

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

    """
    Retrieves squad data and returns a dictionary with ids linked to
    questions
    """

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

    """
    Uses ids to match cloze questions to natural questions
    """

    lamadict = formatLAMAsquad(lamapath)
    squaddict = formatsquad(squadpath)
    targets = lamadict["targets"]

    questions = [squaddict[lamadict["ids"][i][:-2]] for i in range(len(lamadict["ids"]))]

    with open(squad_outputh_path, 'w') as outfile:
        for i in range(len(questions)):
            data = {"question": questions[i], "answer": [targets[i]]}
            json.dump(data, outfile)
            outfile.write('\n')


def get_triples(path, relation):

    """Retrieves triples from file"""

    triples = []

    with jsonlines.open(path) as reader:
        for item in reader:
            sub = item["sub_label"]
            obj = item["obj_label"]
            triples.append((relation, sub, obj))

    return triples


def openlama_fill_template(path, output_path, relation, template):

    """
    Using template create natural questions for a each triple
    """

    triples = get_triples(path, relation)

    questions = []
    answers = []

    for triple in triples:
        relation, sub, obj = triple
        questions.append(template[relation].replace("[X]", sub))
        answers.append(obj)

    with open(output_path, 'w') as outfile:
        for i in range(len(questions)):
            data = {"question": questions[i], "answer": [answers[i]]}
            json.dump(data, outfile)
            outfile.write('\n')


def main():

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

    trexfilenames = []
    for _, _, fname in os.walk('data/LAMA/TREx'):
        trexfilenames.extend(fname)

    relations = [os.path.splitext(os.path.basename(fname))[0] for fname in trexfilenames]

    logging.info("Processing LAMA T-REx dataset")
    for relation in relations:
        filepath = "data/LAMA/TREx/" + relation + ".jsonl"
        outputpath = "openLAMA/trex/" + relation + ".txt"
        openlama_fill_template(filepath, outputpath, relation, trex_template)


if __name__ == "__main__":
    main()
