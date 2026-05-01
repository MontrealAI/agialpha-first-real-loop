SOURCE_PRIORITY = {
    'manifest': 100,
    'docket': 90,
    'scoreboard_json': 80,
    'replay_or_audit': 70,
    'parsed_scoreboard_html': 60,
    'artifact_metadata': 50,
    'workflow_metadata': 40,
    'docs_page': 30,
    'historical_backfill': 10,
}

def rank(source: str) -> int:
    return SOURCE_PRIORITY.get(source, 0)
