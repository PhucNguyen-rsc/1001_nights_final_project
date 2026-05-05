import argparse
import os.path
import sys
import traceback
import warnings

# Silence the harmless macOS warning when SDL clamps the window to fit under
# the title bar / dock chrome. The game still runs at the correct scale.
warnings.filterwarnings("ignore", message=".*forcibly resized.*")

from engine.game import game

main_dir = os.path.split(os.path.abspath(__file__))[0]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", type=int, default=None,
                        help="Dev mode: jump straight into mission N (e.g. --dev 3)")
    args = parser.parse_args()

    error_log = open(os.path.join(main_dir + "/error_report.txt"), "w",
                     encoding="utf-8")  # create error log when game start
    python_ver = sys.version.split(" ")[0].split(".")
    if int(python_ver[0]) < 3 or (python_ver[0] == 3 and int(python_ver[1]) < 10):
        print("This game requires Python version 3.10 and above to run.")
    try:  # for printing error log when error exception happen
        game.Game(main_dir, error_log, dev_mission=args.dev)
    except Exception:  # Save any error output to txt file for any exception
        traceback.print_exc()
        sys.stdout = error_log
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print("".join("!! " + line for line in lines))  # Log it or whatever here
    error_log.close()
