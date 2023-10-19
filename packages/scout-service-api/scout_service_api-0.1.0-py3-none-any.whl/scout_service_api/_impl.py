# coding=utf-8
from abc import (
    abstractmethod,
)
import builtins
from conjure_python_client import (
    ConjureBeanType,
    ConjureDecoder,
    ConjureEncoder,
    ConjureEnumType,
    ConjureFieldDefinition,
    ConjureUnionType,
    OptionalTypeWrapper,
    Service,
)
from requests.adapters import (
    Response,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
)

class scout_RunService(Service):

    def create_run(self, auth_header: str, details: "scout_run_api_CreateRunRequest") -> "scout_run_api_Run":

        _headers: Dict[str, Any] = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': auth_header,
        }

        _params: Dict[str, Any] = {
        }

        _path_params: Dict[str, Any] = {
        }

        _json: Any = ConjureEncoder().default(details)

        _path = '/scout/v1/run'
        _path = _path.format(**_path_params)

        _response: Response = self._request(
            'POST',
            self._uri + _path,
            params=_params,
            headers=_headers,
            json=_json)

        _decoder = ConjureDecoder()
        return _decoder.decode(_response.json(), scout_run_api_Run, self._return_none_for_unknown_union_types)


scout_RunService.__name__ = "RunService"
scout_RunService.__qualname__ = "RunService"
scout_RunService.__module__ = "scout_service_api.scout"


class scout_run_api_CreateRunDataSource(ConjureBeanType):
    """
    For write requests, we want to allow for optional fields
    """

    @builtins.classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            'data_source': ConjureFieldDefinition('dataSource', scout_run_api_DataSource),
            'offset': ConjureFieldDefinition('offset', OptionalTypeWrapper[scout_run_api_Duration]),
            'series_tags': ConjureFieldDefinition('seriesTags', Dict[scout_run_api_SeriesTagName, scout_run_api_SeriesTagValue])
        }

    __slots__: List[str] = ['_data_source', '_offset', '_series_tags']

    def __init__(self, data_source: "scout_run_api_DataSource", series_tags: Dict[str, str], offset: Optional["scout_run_api_Duration"] = None) -> None:
        self._data_source = data_source
        self._offset = offset
        self._series_tags = series_tags

    @builtins.property
    def data_source(self) -> "scout_run_api_DataSource":
        return self._data_source

    @builtins.property
    def offset(self) -> Optional["scout_run_api_Duration"]:
        return self._offset

    @builtins.property
    def series_tags(self) -> Dict[str, str]:
        """
        Used to resolve logical series for this datasource.
        """
        return self._series_tags


scout_run_api_CreateRunDataSource.__name__ = "CreateRunDataSource"
scout_run_api_CreateRunDataSource.__qualname__ = "CreateRunDataSource"
scout_run_api_CreateRunDataSource.__module__ = "scout_service_api.scout_run_api"


class scout_run_api_CreateRunRequest(ConjureBeanType):

    @builtins.classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            'title': ConjureFieldDefinition('title', str),
            'description': ConjureFieldDefinition('description', str),
            'start_time': ConjureFieldDefinition('startTime', scout_run_api_UtcTimestamp),
            'end_time': ConjureFieldDefinition('endTime', OptionalTypeWrapper[scout_run_api_UtcTimestamp]),
            'properties': ConjureFieldDefinition('properties', Dict[scout_run_api_PropertyName, scout_run_api_PropertyValue]),
            'labels': ConjureFieldDefinition('labels', List[scout_run_api_Label]),
            'run_prefix': ConjureFieldDefinition('runPrefix', OptionalTypeWrapper[str]),
            'data_sources': ConjureFieldDefinition('dataSources', Dict[scout_run_api_DataSourceRefName, scout_run_api_CreateRunDataSource])
        }

    __slots__: List[str] = ['_title', '_description', '_start_time', '_end_time', '_properties', '_labels', '_run_prefix', '_data_sources']

    def __init__(self, data_sources: Dict[str, "scout_run_api_CreateRunDataSource"], description: str, labels: List[str], properties: Dict[str, str], start_time: "scout_run_api_UtcTimestamp", title: str, end_time: Optional["scout_run_api_UtcTimestamp"] = None, run_prefix: Optional[str] = None) -> None:
        self._title = title
        self._description = description
        self._start_time = start_time
        self._end_time = end_time
        self._properties = properties
        self._labels = labels
        self._run_prefix = run_prefix
        self._data_sources = data_sources

    @builtins.property
    def title(self) -> str:
        return self._title

    @builtins.property
    def description(self) -> str:
        return self._description

    @builtins.property
    def start_time(self) -> "scout_run_api_UtcTimestamp":
        return self._start_time

    @builtins.property
    def end_time(self) -> Optional["scout_run_api_UtcTimestamp"]:
        return self._end_time

    @builtins.property
    def properties(self) -> Dict[str, str]:
        return self._properties

    @builtins.property
    def labels(self) -> List[str]:
        return self._labels

    @builtins.property
    def run_prefix(self) -> Optional[str]:
        return self._run_prefix

    @builtins.property
    def data_sources(self) -> Dict[str, "scout_run_api_CreateRunDataSource"]:
        return self._data_sources


scout_run_api_CreateRunRequest.__name__ = "CreateRunRequest"
scout_run_api_CreateRunRequest.__qualname__ = "CreateRunRequest"
scout_run_api_CreateRunRequest.__module__ = "scout_service_api.scout_run_api"


class scout_run_api_DataSource(ConjureUnionType):
    _dataset: Optional[str] = None
    _connection: Optional[str] = None
    _log_set: Optional[str] = None

    @builtins.classmethod
    def _options(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            'dataset': ConjureFieldDefinition('dataset', scout_run_api_DatasetRid),
            'connection': ConjureFieldDefinition('connection', scout_run_api_ConnectionRid),
            'log_set': ConjureFieldDefinition('logSet', scout_run_api_LogSetRid)
        }

    def __init__(
            self,
            dataset: Optional[str] = None,
            connection: Optional[str] = None,
            log_set: Optional[str] = None,
            type_of_union: Optional[str] = None
            ) -> None:
        if type_of_union is None:
            if (dataset is not None) + (connection is not None) + (log_set is not None) != 1:
                raise ValueError('a union must contain a single member')

            if dataset is not None:
                self._dataset = dataset
                self._type = 'dataset'
            if connection is not None:
                self._connection = connection
                self._type = 'connection'
            if log_set is not None:
                self._log_set = log_set
                self._type = 'logSet'

        elif type_of_union == 'dataset':
            if dataset is None:
                raise ValueError('a union value must not be None')
            self._dataset = dataset
            self._type = 'dataset'
        elif type_of_union == 'connection':
            if connection is None:
                raise ValueError('a union value must not be None')
            self._connection = connection
            self._type = 'connection'
        elif type_of_union == 'logSet':
            if log_set is None:
                raise ValueError('a union value must not be None')
            self._log_set = log_set
            self._type = 'logSet'

    @builtins.property
    def dataset(self) -> Optional[str]:
        return self._dataset

    @builtins.property
    def connection(self) -> Optional[str]:
        return self._connection

    @builtins.property
    def log_set(self) -> Optional[str]:
        return self._log_set

    def accept(self, visitor) -> Any:
        if not isinstance(visitor, scout_run_api_DataSourceVisitor):
            raise ValueError('{} is not an instance of scout_run_api_DataSourceVisitor'.format(visitor.__class__.__name__))
        if self._type == 'dataset' and self.dataset is not None:
            return visitor._dataset(self.dataset)
        if self._type == 'connection' and self.connection is not None:
            return visitor._connection(self.connection)
        if self._type == 'logSet' and self.log_set is not None:
            return visitor._log_set(self.log_set)


scout_run_api_DataSource.__name__ = "DataSource"
scout_run_api_DataSource.__qualname__ = "DataSource"
scout_run_api_DataSource.__module__ = "scout_service_api.scout_run_api"


class scout_run_api_DataSourceVisitor:

    @abstractmethod
    def _dataset(self, dataset: str) -> Any:
        pass

    @abstractmethod
    def _connection(self, connection: str) -> Any:
        pass

    @abstractmethod
    def _log_set(self, log_set: str) -> Any:
        pass


scout_run_api_DataSourceVisitor.__name__ = "DataSourceVisitor"
scout_run_api_DataSourceVisitor.__qualname__ = "DataSourceVisitor"
scout_run_api_DataSourceVisitor.__module__ = "scout_service_api.scout_run_api"


class scout_run_api_Duration(ConjureBeanType):

    @builtins.classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            'seconds': ConjureFieldDefinition('seconds', int),
            'nanos': ConjureFieldDefinition('nanos', int)
        }

    __slots__: List[str] = ['_seconds', '_nanos']

    def __init__(self, nanos: int, seconds: int) -> None:
        self._seconds = seconds
        self._nanos = nanos

    @builtins.property
    def seconds(self) -> int:
        return self._seconds

    @builtins.property
    def nanos(self) -> int:
        return self._nanos


scout_run_api_Duration.__name__ = "Duration"
scout_run_api_Duration.__qualname__ = "Duration"
scout_run_api_Duration.__module__ = "scout_service_api.scout_run_api"


class scout_run_api_Property(ConjureBeanType):

    @builtins.classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            'name': ConjureFieldDefinition('name', scout_run_api_PropertyName),
            'value': ConjureFieldDefinition('value', scout_run_api_PropertyValue)
        }

    __slots__: List[str] = ['_name', '_value']

    def __init__(self, name: str, value: str) -> None:
        self._name = name
        self._value = value

    @builtins.property
    def name(self) -> str:
        return self._name

    @builtins.property
    def value(self) -> str:
        return self._value


scout_run_api_Property.__name__ = "Property"
scout_run_api_Property.__qualname__ = "Property"
scout_run_api_Property.__module__ = "scout_service_api.scout_run_api"


class scout_run_api_Run(ConjureBeanType):

    @builtins.classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            'rid': ConjureFieldDefinition('rid', scout_run_api_RunRid),
            'run_number': ConjureFieldDefinition('runNumber', int),
            'run_prefix': ConjureFieldDefinition('runPrefix', OptionalTypeWrapper[str]),
            'title': ConjureFieldDefinition('title', str),
            'description': ConjureFieldDefinition('description', str),
            'start_time': ConjureFieldDefinition('startTime', scout_run_api_UtcTimestamp),
            'end_time': ConjureFieldDefinition('endTime', OptionalTypeWrapper[scout_run_api_UtcTimestamp]),
            'properties': ConjureFieldDefinition('properties', Dict[scout_run_api_PropertyName, scout_run_api_PropertyValue]),
            'labels': ConjureFieldDefinition('labels', List[scout_run_api_Label]),
            'created_at': ConjureFieldDefinition('createdAt', str),
            'updated_at': ConjureFieldDefinition('updatedAt', str),
            'data_sources': ConjureFieldDefinition('dataSources', Dict[scout_run_api_DataSourceRefName, scout_run_api_RunDataSource])
        }

    __slots__: List[str] = ['_rid', '_run_number', '_run_prefix', '_title', '_description', '_start_time', '_end_time', '_properties', '_labels', '_created_at', '_updated_at', '_data_sources']

    def __init__(self, created_at: str, data_sources: Dict[str, "scout_run_api_RunDataSource"], description: str, labels: List[str], properties: Dict[str, str], rid: str, run_number: int, start_time: "scout_run_api_UtcTimestamp", title: str, updated_at: str, end_time: Optional["scout_run_api_UtcTimestamp"] = None, run_prefix: Optional[str] = None) -> None:
        self._rid = rid
        self._run_number = run_number
        self._run_prefix = run_prefix
        self._title = title
        self._description = description
        self._start_time = start_time
        self._end_time = end_time
        self._properties = properties
        self._labels = labels
        self._created_at = created_at
        self._updated_at = updated_at
        self._data_sources = data_sources

    @builtins.property
    def rid(self) -> str:
        return self._rid

    @builtins.property
    def run_number(self) -> int:
        return self._run_number

    @builtins.property
    def run_prefix(self) -> Optional[str]:
        return self._run_prefix

    @builtins.property
    def title(self) -> str:
        return self._title

    @builtins.property
    def description(self) -> str:
        return self._description

    @builtins.property
    def start_time(self) -> "scout_run_api_UtcTimestamp":
        return self._start_time

    @builtins.property
    def end_time(self) -> Optional["scout_run_api_UtcTimestamp"]:
        return self._end_time

    @builtins.property
    def properties(self) -> Dict[str, str]:
        return self._properties

    @builtins.property
    def labels(self) -> List[str]:
        return self._labels

    @builtins.property
    def created_at(self) -> str:
        return self._created_at

    @builtins.property
    def updated_at(self) -> str:
        return self._updated_at

    @builtins.property
    def data_sources(self) -> Dict[str, "scout_run_api_RunDataSource"]:
        return self._data_sources


scout_run_api_Run.__name__ = "Run"
scout_run_api_Run.__qualname__ = "Run"
scout_run_api_Run.__module__ = "scout_service_api.scout_run_api"


class scout_run_api_RunDataSource(ConjureBeanType):
    """
    For read requests, we want to require all fields
    """

    @builtins.classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            'data_source': ConjureFieldDefinition('dataSource', scout_run_api_DataSource),
            'offset': ConjureFieldDefinition('offset', scout_run_api_Duration),
            'ref_name': ConjureFieldDefinition('refName', scout_run_api_DataSourceRefName),
            'timestamp_type': ConjureFieldDefinition('timestampType', scout_run_api_WeakTimestampType),
            'series_tags': ConjureFieldDefinition('seriesTags', Dict[scout_run_api_SeriesTagName, scout_run_api_SeriesTagValue])
        }

    __slots__: List[str] = ['_data_source', '_offset', '_ref_name', '_timestamp_type', '_series_tags']

    def __init__(self, data_source: "scout_run_api_DataSource", offset: "scout_run_api_Duration", ref_name: str, series_tags: Dict[str, str], timestamp_type: "scout_run_api_WeakTimestampType") -> None:
        self._data_source = data_source
        self._offset = offset
        self._ref_name = ref_name
        self._timestamp_type = timestamp_type
        self._series_tags = series_tags

    @builtins.property
    def data_source(self) -> "scout_run_api_DataSource":
        return self._data_source

    @builtins.property
    def offset(self) -> "scout_run_api_Duration":
        """
        This offset is used for small time-sync corrections. Notably, it is
not the offset to move a relative data source to the start of the run.
        """
        return self._offset

    @builtins.property
    def ref_name(self) -> str:
        """
        Included for convenience, duplicated from the key of the map
        """
        return self._ref_name

    @builtins.property
    def timestamp_type(self) -> "scout_run_api_WeakTimestampType":
        return self._timestamp_type

    @builtins.property
    def series_tags(self) -> Dict[str, str]:
        """
        Used to resolve logical series for this datasource.
        """
        return self._series_tags


scout_run_api_RunDataSource.__name__ = "RunDataSource"
scout_run_api_RunDataSource.__qualname__ = "RunDataSource"
scout_run_api_RunDataSource.__module__ = "scout_service_api.scout_run_api"


class scout_run_api_UtcTimestamp(ConjureBeanType):

    @builtins.classmethod
    def _fields(cls) -> Dict[str, ConjureFieldDefinition]:
        return {
            'seconds_since_epoch': ConjureFieldDefinition('secondsSinceEpoch', int),
            'offset_nanoseconds': ConjureFieldDefinition('offsetNanoseconds', OptionalTypeWrapper[int])
        }

    __slots__: List[str] = ['_seconds_since_epoch', '_offset_nanoseconds']

    def __init__(self, seconds_since_epoch: int, offset_nanoseconds: Optional[int] = None) -> None:
        self._seconds_since_epoch = seconds_since_epoch
        self._offset_nanoseconds = offset_nanoseconds

    @builtins.property
    def seconds_since_epoch(self) -> int:
        return self._seconds_since_epoch

    @builtins.property
    def offset_nanoseconds(self) -> Optional[int]:
        return self._offset_nanoseconds


scout_run_api_UtcTimestamp.__name__ = "UtcTimestamp"
scout_run_api_UtcTimestamp.__qualname__ = "UtcTimestamp"
scout_run_api_UtcTimestamp.__module__ = "scout_service_api.scout_run_api"


class scout_run_api_WeakTimestampType(ConjureEnumType):
    """
    If a CSV data source is still being split, the timestamp type is not known.
    """

    ABSOLUTE = 'ABSOLUTE'
    '''ABSOLUTE'''
    RELATIVE = 'RELATIVE'
    '''RELATIVE'''
    PENDING = 'PENDING'
    '''PENDING'''
    UNKNOWN = 'UNKNOWN'
    '''UNKNOWN'''

    def __reduce_ex__(self, proto):
        return self.__class__, (self.name,)


scout_run_api_WeakTimestampType.__name__ = "WeakTimestampType"
scout_run_api_WeakTimestampType.__qualname__ = "WeakTimestampType"
scout_run_api_WeakTimestampType.__module__ = "scout_service_api.scout_run_api"


scout_run_api_Label = str

scout_run_api_PropertyValue = str

scout_run_api_SeriesTagValue = str

scout_run_api_LogSetRid = str

scout_run_api_PropertyName = str

scout_run_api_SeriesTagName = str

scout_run_api_ConnectionRid = str

scout_run_api_DatasetRid = str

scout_run_api_DataSourceRefName = str

scout_run_api_RunRid = str

