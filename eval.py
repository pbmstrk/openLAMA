import argparse
import json
import unicodedata
import string
import logging
from logger.logger import set_logger
import re

parser = argparse.ArgumentParser()
parser.add_argument('datasetfile',
                    help="path to files that should be combined")
parser.add_argument('predfile',
                    help="path to outputfile, path/to/output.txt")
parser.add_argument('combinedata')
parser.add_argument('k', type=int,
                    help="Hits@k")

def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))

def hits_at_k(preds, ans, k):
    """accepts list of predictions and answers"""

    preds_k = [normalize_answer(pred) for pred in preds[:k]]
    ans = [normalize_answer(a) for a in ans]
   
    any_in = lambda a, b: bool(set(a).intersection(b))

    return any_in(preds_k, ans)


def normalize(text):
    """Resolve different type of unicode encodings."""
    return unicodedata.normalize('NFD', text)

def partition(alist, indices):
    return [alist[i:j] for i, j in zip([0]+indices, indices+[None])]

def evaluate(dataset_file, prediction_file, combine_file, k):

    with open(combine_file) as f:
        combinedata = json.load(f)

    answers = []
    for line in open(dataset_file):
        data = json.loads(line)
        answer = [normalize(a) for a in data['answer']]
        answers.append(answer)
    
    predictions = []
    with open(prediction_file) as f:
        for line in f:
            data = json.loads(line)
            preds = [normalize(d['span']) for d in data]
            predictions.append(preds)

    answerlist = partition(answers, combinedata["linenumbers"])
    predlist = partition(predictions, combinedata["linenumbers"])

    with open('results_{}.txt'.format(combinedata["dataset"]), 'w') as f:
        for iteration in range(len(answerlist)):
            ans, preds = answerlist[iteration], predlist[iteration]
            score = 0
            for i in range(len(preds)):
                score += hits_at_k(preds[i], ans[i], k)
            total = len(preds)
            hitsk = 100.0 * score / total
            logging.info({'Data': combinedata["filenames"][iteration], 'Hits@{}'.format(k): hitsk})
            res = {'Data': combinedata["filenames"][iteration], 'Hits@{}'.format(k): hitsk}
            json.dump(res, f)
            f.write('\n')

if __name__ == "__main__":
    
    set_logger("eval.log")
    logging.info(25*"-" + " Evaluation " + 25*"-")
    args = parser.parse_args()
    evaluate(args.datasetfile, args.predfile, args.combinedata, args.k)