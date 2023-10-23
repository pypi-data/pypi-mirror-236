from research_framework.container.container import Container
from research_framework.pipeline.pipeline import FitPredictPipeline, FitPredictGridSearchPipeline
from research_framework.container.model.global_config import GlobalConfig
from research_framework.flyweight.flyweight import FlyWeight
from pydantic import BaseModel

PIPELINE = {
    "FitPredictPipeline": FitPredictPipeline,
    "FitPredictGridSearchPipeline": FitPredictGridSearchPipeline
}

class PipelineManager:
    
    @staticmethod
    def start_pipeline(project:str, pl_conf:BaseModel, log:bool=False, store:bool=True, overwrite:bool=False):
        Container.fly = FlyWeight()
        
        Container.global_config = GlobalConfig(
            log=log,
            overwrite=overwrite,
            store=store
        )
        
        pipeline = PIPELINE[pl_conf._clazz](pl_conf,project)
        pipeline.start()
        pipeline.log_metrics()