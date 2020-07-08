# openLAMA

Code to convert the cloze questions of the [LAMA dataset](https://github.com/facebookresearch/LAMA/tree/master) to natural questions.

## Details

We use a subset of the LAMA probe, which is based on various sources:

1. Google-RE (specifically, the relations `birth-place`, `birth-date` and `death-place`)
2. T-REx [(Elsahar et al., 2018)](https://www.aclweb.org/anthology/L18-1544/)
3. Squad [(Rajpurkar et al., 2016)](https://www.aclweb.org/anthology/D16-1264/)

Converting to natural questions:
- for Squad the original questions from the Squad dataset are used, which correspond to 
the masked questions in the LAMA probe.  
 - for T-REx and Google-RE we define templates mapping a triple to a natural question, 
see the example below.

```
relation: capital-city
template: "What is the capital of [X]?"
```

## Generating natural questions

```
download.sh
python convert.py
```

The script `download.sh` downloads the LAMA dataset as well as part of the SQUAD dataset (needed to align questions), and creates a folder structure to store the created openLAMA dataset. The python script `convert.py` uses templates to convert the cloze style questions to natural questions.

The `combine.py` script combines multiple files to make prediction using an open-domain QA system easier. `eval.py` can then be used to evaluate the results.

```
python combine.py filespath outputpath
python eval.py datasetfile predfile --combine_data --k
```


## Results 

### DrQA

| Dataset |  | Hits@1 | Hits@5 | Hits@10 |
|:------| :------:| :----:| :----:| :----:| 
| Squad | | 28.52 | 41.31 | 47.87 |
| Google-RE  | `birth-place` <br> `birth-date` <br> `death-place`  | 50.63 <br> 47.78 <br> 47.78| 68.81 <br> 71.56 <br> 69.32 | 71.91 <br> 75.61 <br> 73.10 |
| T-REx | `1-1` <br> `N-1` <br> `N-M`  | 41.83 <br> 25.51 <br> 19.11 | 61.79 <br> 45.71 <br> 35.57 | 68.52 <br> 53.41 <br> 42.67 |

### ODQA (BM25 + BERTReader)

| Dataset |  | Hits@1 | Hits@5 | Hits@10 |
|:------| :------:| :----:| :----:| :----:| 
| Squad | | 42.62 | 64.59 | 70.81 |
| Google-RE  | `birth-place` <br> `birth-date` <br> `death-place`  | 69.81 <br> 48.18 <br> 28.85| 83.45 <br> 76.03 <br> 53.39 | 85.69 <br> 79.26 <br> 57.70 |
| T-REx | `1-1` <br> `N-1` <br> `N-M`  | 56.24 <br> 22.39 <br> 17.40 | 87.94 <br> 47.89 <br> 39.18 | 91.57 <br> 57.02 <br> 47.24 |

