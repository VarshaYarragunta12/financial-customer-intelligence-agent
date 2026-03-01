import numpy as np
import pandas as pd

np.random.seed(7)

def make_data(months=18):
    dates = pd.date_range("2024-01-01", periods=months, freq="MS")
    vendors = ["AWS", "Microsoft", "Adobe", "Snowflake", "Datadog"]
    categories = ["Cloud", "SaaS", "Security"]

    rows = []
    for d in dates:
        for v in vendors:
            for c in categories:
                base = {"AWS": 12000, "Microsoft": 9000, "Adobe": 5000, "Snowflake": 7000, "Datadog": 3000}[v]
                season = 1 + 0.1 * np.sin((d.month / 12) * 2 * np.pi)
                noise = np.random.normal(0, 0.08)
                amt = base * season * (1 + noise)

                # inject one spike and one drop
                if str(d)[:7] == "2025-04" and v == "AWS" and c == "Cloud":
                    amt *= 2.2
                if str(d)[:7] == "2025-06" and v == "Adobe" and c == "SaaS":
                    amt *= 0.3

                rows.append([d.date(), v, c, round(max(0, amt), 2), "USD"])

    df = pd.DataFrame(rows, columns=["date", "vendor", "category", "amount", "currency"])
    df.to_csv("sample_spend.csv", index=False)
    print("Created sample_spend.csv")

if __name__ == "__main__":
    make_data()