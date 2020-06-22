# openLAMA

Code to convert the cloze questions of the [LAMA dataset](https://github.com/facebookresearch/LAMA/tree/master) to natural questions.

## Details

The LAMA probe is based on various sources:

1. Google-RE (specifically, the relations `birth-place`, `birth-date` and `death-place`)
2. T-REx 
3. ConceptNet (not implemented yet)
4. Squad

To convert to natural questions, for Squad the original questions from the Squad dataset are taken which correspond to 
the masked questions in the LAMA probe.  For the other datasets we define templates mapping a triple to a natural question, 
see the example below.

```
relation: capital-city
template: "What is the capital of [X]?"
```

## Generating natural questions

```
downloaddata.sh
python convert.py
```

The script `downloaddata.sh` downloads the LAMA dataset as well as part of the SQUAD dataset, and creates a folder structure to store the created openLAMA data. `convert.py` uses templates to convert the cloze style questions to natural questions.

The `combine.py` script combines multiple files to make inference using an open-domain QA system easier. `eval.py` can then be used to evaluate the results.




