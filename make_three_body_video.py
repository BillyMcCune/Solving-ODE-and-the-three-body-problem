from pathlib import Path

from methods_registry import MethodName
from three_body_visual import animate_three_body


# Edit these if you want different defaults, then just click Run.
METHOD = MethodName.ADAMS_BASHFORTH
DURATION_YEARS = 2000.0
STEP_HOURS = 24.0
FRAME_STRIDE = 10
FPS = 30
OUTPUT_PATH = Path("three_body_videos/three_body_video_AB2_2.mp4")


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    animate_three_body(
        step_hours=STEP_HOURS,
        duration_years=DURATION_YEARS,
        frame_stride=FRAME_STRIDE,
        method_name=METHOD,
        save_path=OUTPUT_PATH,
        fps=FPS,
        show_plot=False,
    )

    print(f"Saved animation to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
