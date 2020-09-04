import logging
from datetime import datetime

import cftime
from dateutil import parser as date_parser
from roocs_utils.parameter import parameterise

from ..exceptions import InvalidParameterValue, MissingParameterValue


def nearest(array, datetime):
    return min(array, key=lambda x: abs(x - datetime))


def get_nearest_time(ds, time):
    if time is not None:
        try:
            calendar = ds.time.data[0].calendar
        except AttributeError:
            calendar = "standard"

        t = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")

        t = cftime.datetime(
            t.year,
            t.month,
            t.day,
            t.hour,
            t.minute,
            t.second,
            t.microsecond,
            calendar=calendar,
        )

        t = nearest(ds.time.values, t)
        return t


def map_params(ds, time=None, area=None, level=None):
    args = dict()
    parameters = parameterise.parameterise(
        collection=ds, time=time, area=area, level=level
    )

    for parameter in ["time", "area"]:  # , 'level']: # level not implemented yet

        if parameters.get(parameter).tuple is not None:
            args.update(parameters.get(parameter).asdict())

    # rename start_time and end_time to start_date and end_date to
    # match clisops/core/subset
    if "start_time" in args:
        args["start_time"] = get_nearest_time(ds, args["start_time"])
        args["start_date"] = args.pop("start_time")

    if "end_time" in args:
        args["end_time"] = get_nearest_time(ds, args["end_time"])
        args["end_date"] = args.pop("end_time")

    return args
