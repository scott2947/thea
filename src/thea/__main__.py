from thea.pipeline import Pipeline
from thea.detection.color.detector import ColorDetector
from thea.planning.head.planner import HeadPlanner

if __name__ == "__main__":
    pl = Pipeline("colour-head", ColorDetector(), HeadPlanner())
    pl.build()
    pl.start()
