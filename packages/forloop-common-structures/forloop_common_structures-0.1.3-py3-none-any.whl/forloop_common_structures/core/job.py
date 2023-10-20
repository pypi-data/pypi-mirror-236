from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, TypedDict

from src.core.node import Node

from forloop_common_structures.core.edge import Edge
from forloop_common_structures.core.variable import Variable


class JobSortableColumnsEnum(str, Enum):
    STATUS = "status"
    CREATED_AT = "created_at"
    STARTED_AT = "started_at"
    COMPLETED_AT = "completed_at"
    PIPELINE_UID = "pipeline_uid"


class JobStatusEnum(str, Enum):
    QUEUED = "QUEUED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    PAUSED = "PAUSED"
    CANCELLING = "CANCELLING"  # Job in the process of being canceled, but not yet canceled
    CANCELED = "CANCELED"


@dataclass
class NodeJob:
    pipeline_uid: str
    node: Node

    uid: Optional[str] = None
    machine_uid: Optional[str] = None
    status: JobStatusEnum = JobStatusEnum.QUEUED
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    message: Optional[str] = None
    pipeline_job_uid: Optional[int] = None

    def __post_init__(self):
        # Deserialize dict into a Node if NodeJob is instantiated from a JSON
        if isinstance(self.node, dict):
            self.node = Node(**self.node)

        # Deserialize into Enum if instantiated from JSON
        if isinstance(self.status, str):
            self.status = JobStatusEnum(self.status)

    def __str__(self) -> str:
        """Create string representation of the class used in logging."""
        return f"{type(self).__name__}:{self.uid}"


class PipelineElements(TypedDict):
    nodes: list[Node]
    edges: list[Edge]
    variables: list[Variable]


@dataclass
class PipelineJob:
    pipeline_uid: str
    pipeline_elements: PipelineElements

    uid: Optional[str] = None
    machine_uid: Optional[str] = None
    status: JobStatusEnum = JobStatusEnum.QUEUED
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    message: Optional[str] = None

    def __post_init__(self) -> None:
        # Deserialize into Enum if instantiated from JSON
        if isinstance(self.status, str):
            self.status = JobStatusEnum(self.status)

        # Deserialize a dict with nodes/edges/variables dicts
        self._deserialize_pipeline_elements()

    def _deserialize_pipeline_elements(self) -> None:
        """Deserialize nodes, edges, variables into list of objects in case the Job was instantiated from JSON."""
        name_mapping = {"nodes": Node, "edges": Edge, "variables": Variable}
        deserialized_elements = {"nodes": [], "edges": [], "variables": []}

        for element_type, elements in self.pipeline_elements.items():
            # Iterate over Nodes/Edges/Variables groups if instantiated as dicts
            if elements and isinstance(elements[0], dict):
                object_cls = name_mapping[element_type]
                deserialized_elements[element_type] = [
                    object_cls(**element) for element in elements
                ]

        self.pipeline_elements = deserialized_elements

    def __str__(self) -> str:
        """Create string representation of the class used in logging."""
        return f"{type(self).__name__}:{self.uid}"
