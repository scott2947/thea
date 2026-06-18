from thea.pipeline import Pipeline
from thea.detection.yolo.detector import YoloDetector
from thea.planning.head.planner import HeadPlanner

if __name__ == "__main__":
    pl = Pipeline("yolo-head", YoloDetector(), HeadPlanner())
    pl.build()
    pl.start()
