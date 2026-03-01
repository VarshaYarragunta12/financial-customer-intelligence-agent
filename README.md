# AI-Powered Financial Customer Intelligence Agent

This Streamlit application provides a no-code/low-code interface for analyzing customer financial data. It automatically detects column types, offers several analysis intents, and supports simple natural-language queries. An optional OpenAI toggle enables additional intelligence if you configure an API key.

## Features

1. Upload CSV and preview data (first 50 rows) with row/column counts.
2. Robust column detection for dimensions, numeric metrics, and dates.
3. Analysis intents:
   - Top entities (rank)
   - Breakdown / share
   - Count / volume
   - Trend (time series; enabled only if a date column exists)
4. User controls for metric, group-by, date column, aggregation (sum/mean/median/count), and top N.
5. Natural language query box to auto-select options.
6. Validation to prevent crashes and informative error messages.
7. Debug panel showing detection results, chosen plan, and result shapes.
8. Optional OpenAI integration (toggle in sidebar).
9. Sample error handling for bad files, missing columns, empty CSVs, and delimiters.

## Folder Structure

```
app.py
requirements.txt
README.md
src/
  __init__.py
  data_loader.py
  schema_detect.py
  nl_parser.py
  analysis.py
  charts.py
```

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Example Prompts

| Prompt | Behavior |
|--------|----------|
| `Average Total_Spent by Location` | breakdown intent, metric `Total_Spent`, groupby `Location`, agg `mean` |
| `Top 10 customers` | top intent, groupby inferred if `Customer_ID` present |
| `Trend of Total_Spent last year` | trend intent, date column chosen automatically |
| `Count transactions by merchant category` | count intent, metric ignored, groupby `merchant_category` |

## Error Handling Examples

- **Missing numeric columns**: shows "Please select a numeric metric column." when required.
- **Missing date column for trend**: shows "Trend analysis requires a valid date column." and disables run.
- **Empty CSV**: error during upload and message displayed.
- **Bad delimiter**: attempts to sniff delimiter, shows error if unreadable.

## Screenshots

*(Insert app screenshots here)*

## Notes

The app works completely offline with pandas and plotly. OpenAI usage is optional; if enabled, you should set `OPENAI_API_KEY` in a secure way.
