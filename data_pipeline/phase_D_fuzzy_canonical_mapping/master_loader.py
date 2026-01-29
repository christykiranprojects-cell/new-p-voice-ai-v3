import pandas as pd


def load_master_table(path: str) -> pd.DataFrame:
    df = pd.read_excel(path)

    df.columns = (
        df.columns
        .str.strip()
        .str.upper()
    )

    required = {
        "ITEM_CODE",
        "CLEANED_MEDICINE_NAME",
        "MEDICINE_TYPE"
    }

    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in master table: {missing}")

    return df
