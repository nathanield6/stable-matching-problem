# Matching visualization

From the project root, start the replay server:

```sh
python -m visualizations
```

The server opens the replay in your browser. Keep the terminal running and
press Ctrl+C to stop it.

- `visualize_matching.py` serves the page and generates algorithm traces.
- `brute_force_visualization.py` and `gale_shapley_visualization.py` report
  algorithm steps through callbacks.
- `output/stable-matching-replay.html` contains the replay interface.
- `tmp/stable-matching-trace.json` contains saved example trace data.

The visualization modules share `groups.py` with the algorithms at the project
root. To import them in Python, use the `visualizations` package, for example:

```python
from visualizations.gale_shapley_visualization import gale_shapley
```
