import pandas as pd
from datetime import datetime

def format_train(dataset):
    dtypes = [
        ("date", "datetime"),
    ]
    return set_dataset_dtypes(dataset, dtypes)

def format_transactions(dataset):
    dtypes = [
        ("date", "datetime"),
        ("store_nbr", "uint8")
    ]
    return set_dataset_dtypes(dataset, dtypes)

def format_stores(dataset):
    dtypes = [
        ("store_nbr", "uint8"),
        ("city", "category"),
        ("state", "category"),
        ("type", "category"),
        ("cluster", "uint8")]
    return set_dataset_dtypes(dataset, dtypes)

def format_oil(dataset):
    dtypes = [
        ("date", "datetime")
    ]
    return set_dataset_dtypes(dataset, dtypes)

def format_holidays(dataset):
    # Ensure descriptions of the same holiday match
    def remove_buffer_text(s):
        # Beginning
        strings_to_remove = ["Traslado", "Recupero", "Puente", "puente"]
        for s_rem in strings_to_remove:
            s_rem = s_rem + " "
            s = s.replace(s_rem, "")
        # Ending
        found_i = max(s.find('+'), s.find('-'))
        if found_i == -1:
            return s
        if not s[found_i+1].isnumeric():
            return s
        return s[:found_i]

    
    dataset.description = dataset.description.apply(remove_buffer_text)
    dataset = dataset.loc[dataset.transferred == False].copy()
    dataset = dataset.reset_index().drop("index", axis=1)
    
    # Reformat types
    dtypes = [
        ("date", "datetime"),
        ("type", "category"),
        ("locale", "category"),
        ("locale_name", "category"),
        ("description", "category")
    ]
    return set_dataset_dtypes(dataset, dtypes)

def set_dataset_dtypes(dataset, dtypes):
    for col, dtype in dtypes:
        if dtype == "datetime":
            dataset[col] = pd.to_datetime(dataset[col])
            continue
        dataset[col] = dataset[col].astype(dtype)
    return dataset