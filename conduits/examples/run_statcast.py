"""Run the generalized Statcast pipeline without Airflow."""
from __future__ import annotations

from pathlib import Path

from conduits.pipelines.statcast_daily import StatcastDailyPipeline


def main():
    out_dir = Path(__file__).resolve().parents[1] / "artifacts" / "statcast"
    pipe = StatcastDailyPipeline.covering_current_season(str(out_dir))
    ctx = pipe.run()
    print(f"✅ Pipeline {ctx.name} wrote frames to {out_dir}")


if __name__ == "__main__":
    main()
