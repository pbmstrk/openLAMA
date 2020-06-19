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
