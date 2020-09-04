import os
from datetime import datetime

import cftime
import pytest
import xarray as xr

from clisops.core.subset import subset_bbox, subset_time
from clisops.ops.subset import subset

from .._common import CMIP5_RH, CMIP5_TAS, CMIP5_TAS_FILE, CMIP5_ZOSTOGA, TESTS_HOME
from .._common import XCLIM_TESTS_DATA as TESTS_DATA

nc_poslons = os.path.join(
    TESTS_DATA, "cmip3", "tas.sresb1.giss_model_e_r.run1.atm.da.nc"
)


def test_year_subset_time():
    ds = xr.open_mfdataset(CMIP5_TAS, use_cftime=True, combine="by_coords")

    start_date = "2050"
    end_date = "2059"

    result = subset_time(ds, start_date=start_date, end_date=end_date)
    assert result == ds.sel(time=slice(start_date, end_date))


def test_full_date_subset_time_max_and_min():
    ds = xr.open_mfdataset(CMIP5_TAS, use_cftime=True, combine="by_coords")

    start_date = "2050-01-16"
    end_date = "2059-12-16"

    result = subset_time(ds, start_date=start_date, end_date=end_date)
    assert result == ds.sel(time=slice(start_date, end_date))


def test_full_date_subset_time():
    with pytest.raises(ValueError) as exc:
        ds = xr.open_mfdataset(CMIP5_TAS, use_cftime=True, combine="by_coords")
        subset_time(ds, start_date="2050-02-05", end_date="2059-07-15")
        assert (
            exc.value
            == "zero-size array to reduction operation minimum which has no identity"
        )


def test_year_subset_bbox():
    ds = xr.open_mfdataset(CMIP5_TAS, use_cftime=True, combine="by_coords")

    start_date = "2050"
    end_date = "2059"

    result = subset_bbox(
        ds,
        start_date=start_date,
        end_date=end_date,
        lon_bnds=(0, 10),
        lat_bnds=(49, 60),
    )

    assert result is not None


def test_full_date_subset_bbox():
    with pytest.raises(ValueError) as exc:
        ds = xr.open_mfdataset(CMIP5_TAS, use_cftime=True, combine="by_coords")
        subset_bbox(
            ds,
            start_date="2050-02-05",
            end_date="2059-07-15",
            lon_bnds=(0, 10),
            lat_bnds=(49, 60),
        )
        assert (
            exc.value
            == "zero-size array to reduction operation minimum which has no identity"
        )


def test_select_date():
    ds = xr.open_mfdataset(CMIP5_TAS, use_cftime=True, combine="by_coords")
    da = ds.tas
    start_date = "2050-02-05"
    end_date = "2059-07-15"
    start = da.time.sel(time=start_date)
    print(start)
    end = da.time.sel(time=end_date)
    assert len(start) == 0
    assert len(end) == 0

    start_date = "2050-01-16"
    end_date = "2059-12-16"
    start = da.time.sel(time=start_date)
    print(start)
    end = da.time.sel(time=end_date)
    assert len(start) != 0
    assert len(end) != 0

    start_date = "2050"
    end_date = "2059"
    start = da.time.sel(time=start_date)
    print(start)
    end = da.time.sel(time=end_date)
    assert len(start) != 0
    assert len(end) != 0


def test_select_date_different_method():
    ds = xr.open_mfdataset(CMIP5_TAS, use_cftime=True, combine="by_coords")
    start_date = "2050-02-05"
    end_date = "2059-07-15"
    start = ds.sel(time=start_date).time
    end = ds.sel(time=end_date).time
    assert len(start) == 0
    assert len(end) == 0

    start_date = "2050-01-16"
    end_date = "2059-12-16"
    start = ds.sel(time=start_date).time
    end = ds.sel(time=end_date).time
    assert len(start) != 0
    assert len(end) != 0

    start_date = "2050"
    end_date = "2059"
    start = ds.sel(time=start_date).time
    end = ds.sel(time=end_date).time
    assert len(start) != 0
    assert len(end) != 0


def test_time_subset():
    ds = xr.open_mfdataset(CMIP5_TAS, use_cftime=True, combine="by_coords")
    da = ds.tas
    start_date = "2050-02-05"
    end_date = "2059-07-15"
    da_subset = da.sel(time=slice(start_date, end_date))
    assert len(da_subset) != 0

    start_date = "2050-01-16"
    end_date = "2059-12-16"
    da_subset = da.sel(time=slice(start_date, end_date))
    assert len(da_subset) != 0

    start_date = "2050"
    end_date = "2059"
    da_subset = da.sel(time=slice(start_date, end_date))
    assert len(da_subset) != 0


def test_with_xclim_dataset():
    # try with xclim dataset - this is daily data so works
    da = xr.open_dataset(nc_poslons).tas

    start_date = "2050-02-05"
    end_date = "2059-07-15"
    start = da.time.sel(time=start_date)
    end = da.time.sel(time=end_date)
    assert len(start) != 0
    assert len(end) != 0

    start_date = "2050-01-16"
    end_date = "2059-12-16"
    start = da.time.sel(time=start_date)
    end = da.time.sel(time=end_date)
    assert len(start) != 0
    assert len(end) != 0

    start_date = "2050"
    end_date = "2059"
    start = da.time.sel(time=start_date)
    end = da.time.sel(time=end_date)
    assert len(start) != 0
    assert len(end) != 0


def test_with_open_mfdataset():
    # using open_mfdataset isn't the problem
    da = xr.open_mfdataset(nc_poslons, combine="by_coords")

    start_date = "2050-02-05"
    end_date = "2059-07-15"
    start = da.time.sel(time=start_date)
    end = da.time.sel(time=end_date)
    assert len(start) != 0
    assert len(end) != 0

    # using use_cftime doesn't cause an issue
    da = xr.open_mfdataset(nc_poslons, use_cftime=True, combine="by_coords")

    start_date = "2050-02-05"
    end_date = "2059-07-15"
    start = da.time.sel(time=start_date)
    end = da.time.sel(time=end_date)
    assert len(start) != 0
    assert len(end) != 0


def test_with_different_datasets():
    # try rh dataset as normal
    ds = xr.open_mfdataset(CMIP5_RH, use_cftime=True, combine="by_coords").rh
    start_date = "1860-02-05"
    end_date = "2003-07-15"

    start = ds.sel(time=start_date).time
    end = ds.sel(time=end_date).time
    assert len(start) == 0
    assert len(end) == 0

    # try with open dataset for cmip5 tas file
    ds = xr.open_dataset(CMIP5_TAS_FILE, use_cftime=True).tas
    start_date = "2006-02-05"
    end_date = "2029-07-15"

    start = ds.sel(time=start_date).time
    end = ds.sel(time=end_date).time
    assert len(start) == 0
    assert len(end) == 0


def test_difference_between_datasets():
    f = open("da_xclim_test.txt", "w+")
    for time in xr.open_dataset(nc_poslons).time.values:
        f.write(time.strftime())
    f.close()

    f1 = open("da_ceda_test.txt", "w+")
    for time in xr.open_mfdataset(
        CMIP5_TAS, use_cftime=True, combine="by_coords"
    ).time.values:
        f1.write(time.strftime())
    f1.close()


def test_ceda_day_data():
    ds = xr.open_mfdataset(
        os.path.join(
            TESTS_HOME,
            "mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/land"
            "/day/r1i1p1/latest/mrsos/*.nc",
        ),
        use_cftime=True,
        combine="by_coords",
    )
    start_date = "2006-02-05"
    end_date = "2029-07-15"

    start = ds.sel(time=start_date).time
    end = ds.sel(time=end_date).time

    assert len(start) != 0
    assert len(end) != 0


def test_subset_with_ceda_day_data():
    ds = xr.open_mfdataset(
        os.path.join(
            TESTS_HOME,
            "mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/land"
            "/day/r1i1p1/latest/mrsos/*.nc",
        ),
        use_cftime=True,
        combine="by_coords",
    )

    start_date = "2050-01-16"
    end_date = "2059-12-16"

    result = subset_time(ds, start_date=start_date, end_date=end_date)
    assert result == ds.sel(time=slice(start_date, end_date))


def test_method_nearest():
    ds = xr.open_mfdataset(CMIP5_TAS, use_cftime=True, combine="by_coords")
    da = ds.tas
    start_date = "2050-02-05"
    end_date = "2059-07-15"

    start = da.time.sel(time=start_date, method="nearest")
    end = da.time.sel(time=end_date, method="nearest")

    # doesn't work as wanted - still returns empty array
    assert len(start) == 0
    assert len(end) == 0


def nearest(array, datetime):
    return min(array, key=lambda x: abs(x - datetime))


def test_round_to_nearest_time():
    # this works - rounds to closest time

    ds = xr.open_mfdataset(CMIP5_TAS, use_cftime=True, combine="by_coords")
    calendar = ds.time.data[0].calendar

    start_date = "2050-02-05"
    end_date = "2059-07-15"

    sd = datetime.strptime(start_date, "%Y-%m-%d")
    ed = datetime.strptime(end_date, "%Y-%m-%d")

    start_date = cftime.datetime(
        sd.year,
        sd.month,
        sd.day,
        sd.hour,
        sd.minute,
        sd.second,
        sd.microsecond,
        calendar=calendar,
    )
    end_date = cftime.datetime(
        ed.year,
        ed.month,
        ed.day,
        ed.hour,
        ed.minute,
        ed.second,
        ed.microsecond,
        calendar=calendar,
    )

    start_date = nearest(ds.time.values, start_date)
    end_date = nearest(ds.time.values, end_date)

    start = ds.time.sel(time=start_date)
    end = ds.time.sel(time=end_date)

    assert start != 0
    assert end != 0


def test_full_date_clisops_subset_time(tmpdir):
    ds = xr.open_mfdataset(CMIP5_TAS, use_cftime=True, combine="by_coords")
    result = subset(ds, time=("2050-02-05", "2059-07-15"), output_dir=tmpdir)
    assert "output.nc" in result


def teardown_module():
    os.remove("da_xclim_test.txt")
    os.remove("da_ceda_test.txt")
