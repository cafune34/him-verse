"""Validate the proposed binary target from the annual CDC BRFSS XPT file."""
import argparse
import json
import pandas as pd

TARGET_COLUMNS = ["DIABETE4", "CVDINFR4", "CVDCRHD4", "CHCCOPD3", "CHCKDNY2"]

def target(frame):
    # Verify coding against the 2025 codebook before running on real data.
    diabetes = frame["DIABETE4"].map({1:1, 2:0, 3:0, 4:0})
    a = frame["CVDINFR4"].map({1:1, 2:0})
    b = frame["CVDCRHD4"].map({1:1, 2:0})
    heart = pd.Series(float("nan"), index=frame.index)
    heart[(a == 1) | (b == 1)] = 1
    heart[(a == 0) & (b == 0)] = 0
    copd = frame["CHCCOPD3"].map({1:1, 2:0})
    kidney = frame["CHCKDNY2"].map({1:1, 2:0})
    groups = pd.concat([diabetes, heart, copd, kidney], axis=1)
    valid = groups.notna().all(axis=1)
    return (groups.loc[valid].sum(axis=1) >= 2).astype(int)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("xpt")
    args = parser.parse_args()
    n = pos = neg = 0
    for batch in pd.read_sas(args.xpt, format="xport", chunksize=20000):
        batch.columns = [str(c).upper() for c in batch.columns]
        missing = set(TARGET_COLUMNS) - set(batch.columns)
        if missing:
            raise ValueError(f"Missing target columns: {sorted(missing)}")
        y = target(batch)
        n += len(batch)
        pos += int(y.sum())
        neg += int((y == 0).sum())
    valid = pos + neg
    print(json.dumps({"raw_rows": n, "eligible_rows": valid,
                      "excluded_unknown_target": n-valid,
                      "class_0": neg, "class_1": pos,
                      "minority_count": min(pos, neg),
                      "positive_share": pos/valid if valid else None}, indent=2))
    if valid < 20000 or min(pos, neg) < 300:
        raise SystemExit("Check dataset size and class coverage before submission.")

if __name__ == "__main__":
    main()
