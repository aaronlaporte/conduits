"""Run the weekly performance report pipeline."""
from __future__ import annotations

from pathlib import Path

from conduits.pipelines.weekly_performance_report import WeeklyPerformanceReportPipeline


def main():
    repo_root = Path(__file__).resolve().parents[1]
    workbook = repo_root / "artifacts" / "sample_tracking.xlsx"
    out_json = repo_root / "artifacts" / "reports" / "latest_week.json"
    pipe = WeeklyPerformanceReportPipeline(str(workbook), "p&l", out_json)
    ctx = pipe.run()
    print(f"✅ Pipeline {ctx.name} summarized {ctx.metadata.get('records')} rows")


if __name__ == "__main__":
    main()
