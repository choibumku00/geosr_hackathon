def test_core_imports():
    import numpy, pandas, xarray, yaml
    import netCDF4  # noqa: F401
    assert xarray.__version__
