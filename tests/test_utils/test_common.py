import cftime
import pytest
import xarray as xr
from dateutil.parser import ParserError
from roocs_utils.exceptions import InvalidParameterValue, MissingParameterValue

from clisops import utils
from tests._common import CMIP5_TAS_FILE


@pytest.mark.xfail(reason="parse_date removed as date parsed in TimeParameter class")
def test_parse_date():
    assert "2020-05-19" == utils.parse_date("2020-05-19")
    assert "1999-01-01" == utils.parse_date("1999-01-01T00:00:00")
    with pytest.raises(ParserError):
        utils.parse_date("tomorrow")


@pytest.mark.xfail(
    reason="parse_date_year removed as date parsed in TimeParameter class"
)
def test_parse_date_year():
    assert "2020" == utils.parse_date_year("2020-05-20")
    with pytest.raises(ParserError):
        utils.parse_date_year("yesterday")


def test_map_params():
    args = utils.map_params(
        ds=xr.open_mfdataset(CMIP5_TAS_FILE, use_cftime=True, combine="by_coords"),
        time=("1999-01-01T00:00:00", "2100-12-30T00:00:00"),
        area=(-5.0, 49.0, 10.0, 65),
        level=(1000.0, 1000.0),
    )

    # rounds to nearest time
    assert args["start_date"] == cftime.Datetime360Day(2005, 12, 16, 0, 0, 0, 0)
    assert args["end_date"] == cftime.Datetime360Day(2030, 11, 16, 0, 0, 0, 0)
    assert args["lon_bnds"] == (-5, 10)
    assert args["lat_bnds"] == (49, 65)


def test_map_params_time():
    args = utils.map_params(
        ds=xr.open_mfdataset(CMIP5_TAS_FILE, use_cftime=True, combine="by_coords"),
        time=("1999-01-01", "2100-12"),
        area=(0, -90, 360, 90),
    )
    assert args["start_date"] == cftime.Datetime360Day(2005, 12, 16, 0, 0, 0, 0)
    assert args["end_date"] == cftime.Datetime360Day(2030, 11, 16, 0, 0, 0, 0)


def test_map_params_invalid_time():
    with pytest.raises(InvalidParameterValue):
        utils.map_params(
            ds=CMIP5_TAS_FILE,
            time=("1999-01-01T00:00:00", "maybe tomorrow"),
            area=(0, -90, 360, 90),
        )
    with pytest.raises(InvalidParameterValue):
        utils.map_params(ds=CMIP5_TAS_FILE, time=("", "2100"), area=(0, -90, 360, 90))


def test_map_params_area():
    args = utils.map_params(
        ds=xr.open_mfdataset(CMIP5_TAS_FILE, use_cftime=True, combine="by_coords"),
        area=(0, 10, 50, 60),
    )
    assert args["lon_bnds"] == (0, 50)
    assert args["lat_bnds"] == (10, 60)
    # allow also strings
    args = utils.map_params(
        ds=CMIP5_TAS_FILE,
        area=("0", "10", "50", "60"),
    )
    assert args["lon_bnds"] == (0, 50)
    assert args["lat_bnds"] == (10, 60)


def test_map_params_invalid_area():
    with pytest.raises(InvalidParameterValue):
        utils.map_params(
            ds=CMIP5_TAS_FILE,
            area=(0, 10, 50),
        )
    with pytest.raises(InvalidParameterValue):
        utils.map_params(
            ds=CMIP5_TAS_FILE,
            area=("zero", 10, 50, 60),
        )


@pytest.mark.xfail(
    reason="Time, Level and area can all be none as they default to max/min values"
    "in core.subset"
)
def test_map_params_missing_param():
    with pytest.raises(MissingParameterValue):
        utils.map_params()
