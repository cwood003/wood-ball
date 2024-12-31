# Woodball

## Rough outline on plans for this repo
1. Finalize structure for table visualization. This will include game score template provided by Owen from the F5 substack (How to: Score Margin Frequency Charts etc https://thef5.substack.com/p/how-to-score-margin-frequency-charts). This may include designing data ingestions pipelines for various sources (stats.nba.com, bball_ref, odds.api)
2. Create my own RAPM metric devlopment process using the information in tutorials and articles linked here (https://medium.com/@johnchenmbb/1a78e1476b1f, https://github.com/anpatton/basic-nba-tutorials/blob/main/rapm/how_to_calculate_rapm.md)
3. Develop some sort of advanced stats game and season-to-date summary
4. Publish streamlit app to community hosting website with these visualizations with pipelines built to populate on button press (or command typing)
5. Should I use DLT to load data in a seperate codebase? No, buzzword stuff not needed for my project. Do stuff with polars and duckdb forget about the rest
6. Should I create a seperate codebase for the streamlit app?
