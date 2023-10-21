import datetime
import json
import typing
from asyncio import StreamReader
from typing import Optional


def _to_dict_list(obj: list[any]) -> list[dict]:
    if obj is None:
        return []
    return [o.to_dict() for o in obj if o is not None]


class Metadata:
    def __init__(self, id: str, version: str, date: datetime.datetime, name: str, description: str, documentation: str):
        self.id = id
        self.version = version
        self.date = date
        self.name = name
        self.description = description
        self.documentation = documentation


class DocumentationItem:
    def __init__(self, type: str, label: str, url: Optional[str], text: str):
        self.type = type
        self.label = label
        self.url = url
        self.text = text

    def to_dict(self) -> dict:
        return dict(type=self.type, label=self.label, url=self.url, text=self.text)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class PdfDocumentationItem(DocumentationItem):
    def __init__(self, label: str, url: str, text: str):
        super().__init__('pdf', label, url, text)


class InlineDocumentationItem(DocumentationItem):
    def __init__(self, label: str, text: str):
        super().__init__('text', label, None, text)


class LinkDocumentationItem(DocumentationItem):
    def __init__(self, label: str, url: str, text: str):
        super().__init__('link', label, url, text)


TaskItemScalarValue = typing.Union[str, float, bool, None]
TaskItemValue = typing.Union[TaskItemScalarValue, list[TaskItemScalarValue]]

DefinitionType = typing.Literal['select-single', 'select-multiple', 'number', 'boolean']


class TaskItemValueMap(dict[str, TaskItemValue]):
    pass


class PointOption:
    def __init__(self, label: str, value: TaskItemScalarValue, id: Optional[str] = None, annotation: Optional[str] = None):
        self.id = id
        self.label = label
        self.value = value
        self.annotation = annotation

    def to_dict(self) -> dict:
        return dict(id=self.id, label=self.label, value=self.value, annotation=self.annotation)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class BaseTaskItemDefinition:
    def __init__(self, type: DefinitionType):
        self.type = type

    def to_dict(self) -> dict:
        return dict(type=self.type)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class SelectSingleType(BaseTaskItemDefinition):
    def __init__(self, options: list[PointOption]):
        super().__init__('select-single')
        self.options = options

    def to_dict(self) -> dict:
        return {**super().to_dict(), **dict(options=_to_dict_list(self.options))}


class SelectMultipleType(BaseTaskItemDefinition):
    def __init__(self, options: list[PointOption]):
        super().__init__('select-multiple')
        self.options = options

    def to_dict(self) -> dict:
        return {**super().to_dict(), **dict(options=_to_dict_list(self.options))}


class NumberType(BaseTaskItemDefinition):
    def __init__(self, minimum: Optional[float], maximum: Optional[float], step: Optional[float]):
        super().__init__('number')
        self.minimum = minimum
        self.maximum = maximum
        self.step = step

    def to_dict(self) -> dict:
        return {**super().to_dict(), **dict(minimum=self.minimum, maximum=self.maximum, step=self.step)}


class BooleanType(BaseTaskItemDefinition):
    def __init__(self):
        super().__init__('boolean')


TaskItemDefinition = typing.Union[SelectSingleType, SelectMultipleType, NumberType, BooleanType]
CriteriaTreeElementType = typing.Literal['criterion', 'task-group', 'task', 'task-item']


class BaseElement:
    def __init__(self, type: CriteriaTreeElementType, id: str, label: Optional[str] = None, tags: Optional[list] = None,
                 documentation: Optional[list[DocumentationItem]] = None):
        self.type = type
        self.id = id
        self.label = label
        self.tags = tags
        self.documentation = documentation

    def to_dict(self) -> dict:
        return dict(type=self.type, id=self.id, label=self.label, tags=self.tags, documentation=_to_dict_list(self.documentation))

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class TaskItem(BaseElement):
    def __init__(self, id: str, definition: TaskItemDefinition, label: Optional[str] = None, tags: Optional[list] = None,
                 documentation: Optional[list[DocumentationItem]] = None, description: Optional[str] = None,
                 provided_data: Optional[dict[str, TaskItemValue]] = None,
                 calculated_data: Optional[dict[str, any]] = None):
        super().__init__('task-item', id=id, label=label, tags=tags, documentation=documentation)
        self.description = description
        self.definition = definition
        self.provided_data = provided_data
        self.calculated_data = calculated_data

    def to_dict(self) -> dict:
        return {**super().to_dict(), **dict(description=self.description, definition=self.definition.to_dict(), providedData=self.provided_data, calculatedData=self.calculated_data)}


class Task(BaseElement):
    def __init__(self, id: str, title: str, label: Optional[str] = None, tags: Optional[list] = None,
                 documentation: Optional[list[DocumentationItem]] = None, description: Optional[str] = None, items: list[TaskItem] = None):
        super().__init__('task', id=id, label=label, tags=tags, documentation=documentation)
        self.title = title
        self.description = description
        self.items = items or []

    def to_dict(self) -> dict:
        return {**super().to_dict(), **dict(title=self.title, description=self.description, items=_to_dict_list(self.items))}


class TaskGroup(BaseElement):
    def __init__(self, id: str, title: str, label: Optional[str] = None, tags: Optional[list] = None,
                 documentation: Optional[list[DocumentationItem]] = None, items: list[Task] = None):
        super().__init__('task-group', id=id, label=label, tags=tags, documentation=documentation)
        self.title = title
        self.items = items or []

    def to_dict(self) -> dict:
        return {**super().to_dict(), **dict(title=self.title, items=_to_dict_list(self.items))}


class Criterion(BaseElement):
    def __init__(self, id: str, title: str, quality: str, label: Optional[str] = None, tags: Optional[list] = None,
                 documentation: Optional[list[DocumentationItem]] = None,
                 items: list[TaskGroup] = None):
        super().__init__('criterion', id=id, label=label, tags=tags, documentation=documentation)
        self.title = title
        self.quality = quality
        self.items = items or []

    def to_dict(self) -> dict:
        return {**super().to_dict(), **dict(title=self.title, quality=self.quality, items=_to_dict_list(self.items))}


class CriteriaTree(list[Criterion]):
    def to_json(self) -> str:
        return json.dumps(_to_dict_list(self))


CriteriaTreeElement = typing.Union[Criterion, TaskGroup, Task, TaskItem]


class StreamMatrixResponse():
    def __init__(self, filename: str, content_type: str, stream: StreamReader):
        self.filename = filename
        self.content_type = content_type
        self.stream = stream
