import pandas as pd


GRAPHRAG_FOLDER = "test_data/output"


def main():
    text_df = pd.read_parquet(
        f"{GRAPHRAG_FOLDER}/text_units.parquet", columns=["id", "text", "n_tokens", "document_ids"]
    )
    text_df.head(2)


if __name__ == "__main__":
    main()
