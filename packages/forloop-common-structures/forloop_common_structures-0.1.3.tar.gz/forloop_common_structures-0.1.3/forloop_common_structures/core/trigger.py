from dataclasses import dataclass, field
from typing import ClassVar, Any, Dict, List
import datetime

@dataclass
class Trigger:
    
    trigger_name: str=""
    machine_uid: int=""
    pipeline_uid: int=""
    first_run_datetime: datetime.datetime=datetime.datetime.now()
    frequency: int=""
    project_uid: str="0"
    
    
    
    
    uid: int = field(init=False)
    instance_counter: ClassVar[int] = 0


    def __post_init__(self):
        self.__class__.instance_counter += 1
        self.uid = str(self.instance_counter)
        
