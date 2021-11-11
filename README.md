consumi elettrici Trentino
==============================

Breve progetto di data science sui dati relativi ai consumi elettrici del territorio Trentino nei mesi di novembre e dicembre.
Il progetto è principalmente strutturato sulla base di 3 jupiter notebook appunto nella cartella "notebooks" in cui vengono affrontate separatamente le tre fasi principali di un progetto di DS:
- in "preprocessing" vengono caricati i dati raw e processati in dataframe comodi per le analisi successive, princpalmente combinando tra loro i dataframe grezzi, i dataframe così ottenuti sono caricati quindi nella cartella "data/processed".   Questo notebook in genere impiega una decina di minuti per runnare ma non è necessario farlo in quanto i risultati sono già stati caricati.
- in "EDA" viene effettuata l'exploratory data analysis dei dati processati, vengono mostrate graficamente le correlazioni principali presenti nei dati.
- in "MachineLearning" infine si costruiscono dei modelli con due principali tasks. per la prima è richiesto di poter prevedere con una regressione quali saranno i consumi elettrici giornalieri di tutta la provincia e del centro urbano di Rovereto, avendo a disposizione i dati (consumi, meteo, temperature, ecc..) relativi ai tre giorni precedenti dal giorno da prevedere,  per la seconda invece è richiesto di classificare la zona del comune di Trento con i maggiori consumi, sempre conoscendo i dati relativi ai tre giorni precedenti.   I modelli ottenuti sono salvati nella cartella "models".


Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be im
    │
    └─ src                <- Source code for use in this project.
       ├── __init__.py    <- Makes src a Python module
       │
       ├── data           <- Scripts to download or generate data
       │   └── make_dataset.py
       │
       ├── features       <- Scripts to turn raw data into features for modeling
       │   └── build_features.py
       │
       ├── models         <- Scripts to train models and then use trained models to make
       │   │                 predictions
       │   ├── predict_model.py
       │   └── train_model.py
       │
       └── visualization  <- Scripts to create exploratory and results oriented visualizations
           └── visualize.py


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
