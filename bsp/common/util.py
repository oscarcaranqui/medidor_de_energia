
import copy

from datetime import datetime, timedelta, timezone, tzinfo
from dataclasses import _is_dataclass_instance, fields
from typing import Union


class Guayaquil(tzinfo):

    def utcoffset(self, dt):
      return timedelta(hours=-5)

    def tzname(self, dt):
        return "GYE"

    def dst(self, dt):
        return timedelta(0)


GYE = Guayaquil()


def asdict(obj, *, dict_factory=dict):
    """Return the fields of a dataclass instance as a new dictionary mapping
    field names to field values.

    Example usage:

      @dataclass
      class C:
          x: int
          y: int

      c = C(1, 2)deleteMany({ status : "A" })deleteMany({ status : "A" })
      assert asdict(c) == {'x': 1, 'y': 2}

    If given, 'dict_factory' will be used instead of built-in dict.
    The function applies recursively to field values that are
    dataclass instances. This will also look into built-in containers:
    tuples, lists, and dicts.
    """
    if not _is_dataclass_instance(obj):
        raise TypeError("asdict() should be called on dataclass instances")
    return _asdict_inner(obj, dict_factory)


def _asdict_inner(obj, dict_factory):
    if _is_dataclass_instance(obj):
        result = []
        for f in fields(obj):
            if f.repr and hasattr(obj, f.name):
                value = _asdict_inner(getattr(obj, f.name), dict_factory)
                result.append((f.name, value))
        return dict_factory(result)
    elif isinstance(obj, tuple) and hasattr(obj, '_fields'):
        # obj is a namedtuple.  Recurse into it, but the returned
        # object is another namedtuple of the same type.  This is
        # similar to how other list- or tuple-derived classes are
        # treated (see below), but we just need to create them
        # differently because a namedtuple's __init__ needs to be
        # called differently (see bpo-34363).

        # I'm not using namedtuple's _asdict()
        # method, because:
        # - it does not recurse in to the namedtuple fields and
        #   convert them to dicts (using dict_factory).
        # - I don't actually want to return a dict here.  The the main
        #   use case here is json.dumps, and it handles converting
        #   namedtuples to lists.  Admittedly we're losing some
        #   information here when we produce a json list instead of a
        #   dict.  Note that if we returned dicts here instead of
        #   namedtuples, we could no longer call asdict() on a data
        #   structure where a namedtuple was used as a dict key.

        return type(obj)(*[_asdict_inner(v, dict_factory) for v in obj])
    elif isinstance(obj, (list, tuple)):
        # Assume we can create an object of this type by passing in a
        # generator (which is not true for namedtuples, handled
        # above).
        return type(obj)(_asdict_inner(v, dict_factory) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)((_asdict_inner(k, dict_factory),
                          _asdict_inner(v, dict_factory))
                         for k, v in obj.items())
    elif isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%dT%H:%M:%S%z")
    else:
        return copy.deepcopy(obj)


def asdict_without_datetostr(obj, *, dict_factory=dict):
    """Return the fields of a dataclass instance as a new dictionary mapping
    field names to field values.

    Example usage:

      @dataclass
      class C:
          x: int
          y: int

      c = C(1, 2)
      assert asdict(c) == {'x': 1, 'y': 2}

    If given, 'dict_factory' will be used instead of built-in dict.
    The function applies recursively to field values that are
    dataclass instances. This will also look into built-in containers:
    tuples, lists, and dicts.
    """
    if not _is_dataclass_instance(obj):
        raise TypeError("asdict() should be called on dataclass instances")
    return _asdict_inner_without_datetostr(obj, dict_factory)


def _asdict_inner_without_datetostr(obj, dict_factory):
    if _is_dataclass_instance(obj):
        result = []
        for f in fields(obj):
            if f.repr and hasattr(obj, f.name):
                value = _asdict_inner_without_datetostr(getattr(obj, f.name), dict_factory)
                result.append((f.name, value))
        return dict_factory(result)
    elif isinstance(obj, tuple) and hasattr(obj, '_fields'):
        # obj is a namedtuple.  Recurse into it, but the returned
        # object is another namedtuple of the same type.  This is
        # similar to how other list- or tuple-derived classes are
        # treated (see below), but we just need to create them
        # differently because a namedtuple's __init__ needs to be
        # called differently (see bpo-34363).

        # I'm not using namedtuple's _asdict()
        # method, because:
        # - it does not recurse in to the namedtuple fields and
        #   convert them to dicts (using dict_factory).
        # - I don't actually want to return a dict here.  The the main
        #   use case here is json.dumps, and it handles converting
        #   namedtuples to lists.  Admittedly we're losing some
        #   information here when we produce a json list instead of a
        #   dict.  Note that if we returned dicts here instead of
        #   namedtuples, we could no longer call asdict() on a data
        #   structure where a namedtuple was used as a dict key.

        return type(obj)(*[_asdict_inner_without_datetostr(v, dict_factory) for v in obj])
    elif isinstance(obj, (list, tuple)):
        # Assume we can create an object of this type by passing in a
        # generator (which is not true for namedtuples, handled
        # above).
        return type(obj)(_asdict_inner_without_datetostr(v, dict_factory) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)((_asdict_inner_without_datetostr(k, dict_factory),
                          _asdict_inner_without_datetostr(v, dict_factory))
                         for k, v in obj.items())
    else:
        return copy.deepcopy(obj)

def get_time_from_str(datetime_str: str) -> Union[datetime, None]:
    date = None
    try:
        date = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        return date
    except Exception:
        pass

    try:
        date = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        return date
    except Exception:
        pass

    try:
        date = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')
        return date
    except Exception:
        pass

    try:
        date = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S%z')
        return date
    except Exception:
        pass

    return date


def date_to_str(date: datetime) -> str:
    return date.isoformat(timespec='milliseconds')


def get_now_date() -> datetime:
    return datetime.now(tz=timezone.utc).astimezone()


def get_now_date_str() -> str:
    return date_to_str(get_now_date())


def time_converter(data):
    for k, v in data.items():
        if isinstance(v, (dict,)):
            data[k] = time_converter(v)
        elif isinstance(v, (list,)):
            data[k] = [time_converter(item) for item in v]
        else:
            date = get_time_from_str(v)
            if date is not None:
                data[k] = date
    return data


def get_str_date_from_str_iso_date(str_iso_date: str) -> str:
    return str_iso_date.split('.')[0].split('T')[0]


def get_str_time_from_str_iso_date(str_iso_date: str) -> str:
    return str_iso_date.split('.')[0].split('T')[1]


def get_str_datetime_from_str_iso_date(str_iso_date: str) -> str:
    try:
        return str_iso_date.split('.')[0].replace('T', ' ')
    except:
        return ""
