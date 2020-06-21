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

def exact_match_score(prediction, ground_truth):
    """Check if the prediction is a (soft) exact match with the ground truth."""
    return normalize_answer(prediction) == normalize_answer(ground_truth)


def normalize(text):
    """Resolve different type of unicode encodings."""
    return unicodedata.normalize('NFD', text)

def partition(alist, indices):
    return [alist[i:j] for i, j in zip([0]+indices, indices+[None])]

def metric_max_over_ground_truths(metric_fn, prediction, ground_truths):
    """Given a prediction and multiple valid answers, return the score of
    the best prediction-answer_n pair given a metric function.
    """
    scores_for_ground_truths = []
    for ground_truth in ground_truths:
        score = metric_fn(prediction, ground_truth)
        scores_for_ground_truths.append(score)
    return max(scores_for_ground_truths)

def evaluate(dataset_file, prediction_file, combine_file):

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
            prediction = normalize(data[0]['span'])
            predictions.append(prediction)

    answerlist = partition(answers, combinedata["linenumbers"])
    predlist = partition(predictions, combinedata["linenumbers"])

    for iteration in range(len(answerlist)):
        ans, preds = answerlist[iteration], predlist[iteration]
        exact_match = 0
        for i in range(len(preds)):
            exact_match += metric_max_over_ground_truths(
                exact_match_score, preds[i], ans[i]
            )
        total = len(preds)
        exact_match = 100.0 * exact_match / total
        logging.info({'Data': combinedata["filenames"][iteration], 'exact_match': exact_match})

if __name__ == "__main__":
    
    set_logger("eval.log")
    logging.info(25*"-" + " Evaluation " + 25*"-")
    args = parser.parse_args()
    evaluate(args.datasetfile, args.predfile, args.combinedata)