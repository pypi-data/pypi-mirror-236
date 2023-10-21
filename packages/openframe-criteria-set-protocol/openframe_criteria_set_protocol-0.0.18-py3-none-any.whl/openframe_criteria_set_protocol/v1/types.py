import datetime
import typing
from abc import ABC
from asyncio import StreamReader
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Metadata:
    id: str
    version: str
    date: datetime.datetime
    name: str
    description: str
    documentation: str


@dataclass
class DocumentationItem(ABC):
    type: str
    label: str
    text: str
    url: Optional[str] = None


@dataclass
class PdfDocumentationItem(DocumentationItem):
    type: str = field(init=False, default='pdf')


@dataclass
class InlineDocumentationItem(DocumentationItem):
    type: str = field(init=False, default='text')


@dataclass
class LinkDocumentationItem(DocumentationItem):
    type: str = field(init=False, default='link')


TaskItemScalarValue = typing.Union[str, float, bool, None]
TaskItemValue = typing.Union[TaskItemScalarValue, list[TaskItemScalarValue]]

DefinitionType = typing.Literal['select-single', 'select-multiple', 'number', 'boolean']


@dataclass
class TaskItemValueMap(dict[str, TaskItemValue]):
    pass


@dataclass
class PointOption:
    label: str
    value: TaskItemScalarValue
    id: Optional[str] = None
    annotation: Optional[str] = None


@dataclass
class BaseTaskItemDefinition(ABC):
    type: DefinitionType


@dataclass
class SelectSingleType(BaseTaskItemDefinition):
    type: DefinitionType = field(init=False, default='select-single')
    options: list[PointOption]


@dataclass
class SelectMultipleType(BaseTaskItemDefinition):
    type: DefinitionType = field(init=False, default='select-multiple')
    options: list[PointOption]


@dataclass
class NumberType(BaseTaskItemDefinition):
    type: DefinitionType = field(init=False, default='number')
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    step: Optional[float] = None


@dataclass
class BooleanType(BaseTaskItemDefinition):
    type: DefinitionType = field(init=False, default='boolean')


TaskItemDefinition = typing.Union[SelectSingleType, SelectMultipleType, NumberType, BooleanType]
CriteriaTreeElementType = typing.Literal['criterion', 'task-group', 'task', 'task-item']


@dataclass
class TaskItem:
    type: CriteriaTreeElementType = field(init=False, default='task-item')
    id: str
    definition: TaskItemDefinition
    label: Optional[str] = None
    tags: Optional[list] = None
    documentation: Optional[list[DocumentationItem]] = None
    description: Optional[str] = None
    provided_data: Optional[dict[str, TaskItemValue]] = None
    calculated_data: Optional[dict[str, any]] = None


@dataclass
class Task:
    type: CriteriaTreeElementType = field(init=False, default='task')
    id: str
    title: str
    label: Optional[str] = None
    tags: Optional[list] = None
    documentation: Optional[list[DocumentationItem]] = None
    description: Optional[str] = None
    items: list[TaskItem] = field(default_factory=list)


@dataclass
class TaskGroup:
    type: CriteriaTreeElementType = field(init=False, default='task-group')
    id: str
    title: str
    label: Optional[str] = None
    tags: Optional[list] = None
    documentation: Optional[list[DocumentationItem]] = None
    items: list[Task] = field(default_factory=list)


@dataclass
class Criterion:
    type: CriteriaTreeElementType = field(init=False, default='criterion')
    id: str
    title: str
    quality: str
    label: Optional[str] = None
    tags: Optional[list] = None
    documentation: Optional[list[DocumentationItem]] = None
    items: list[TaskGroup] = field(default_factory=list)


@dataclass
class CriteriaTree(list[Criterion]):
    def __init__(self, criteria: list[Criterion] = None):
        super().__init__(criteria or [])


CriteriaTreeElement = typing.Union[Criterion, TaskGroup, Task, TaskItem]


class StreamMatrixResponse:
    def __init__(self, filename: str, content_type: str, stream: StreamReader):
        self.filename = filename
        self.content_type = content_type
        self.stream = stream
