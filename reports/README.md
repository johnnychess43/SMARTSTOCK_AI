# Reports

Scripts in `src/` generate quality reports, CSV summaries, and charts here.
Generated outputs are local artifacts and may be recreated at any time:

1. `python src/prepare_data.py`
2. `python src/explore_data.py`

All findings are based on synthetic academic data. The stockout-days figure
is a proxy based on records where units sold equal stock available; it is not
proof of unmet customer demand.
