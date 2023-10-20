#!/usr/bin/env python3


"""Sample data set for r5py, covering Helsinki city centre, downloaded upon first access."""


import warnings


__version__ = "0.1.1.dev1"
__all__ = ["__version__"]


try:
    from r5py.util.sample_data_set import SampleDataSet

    BASE_URL = (
        f"https://github.com/r5py/r5py.sampledata.helsinki/raw/v{__version__}/data/"
    )

    gtfs = SampleDataSet(
        f"{BASE_URL}/helsinki_gtfs.zip",
        "8ecccde3e76441b47e90c7f311fc57a8d38df92e9ee592e8f440a9b7e3abf228",
    )
    osm_pbf = SampleDataSet(
        f"{BASE_URL}/kantakaupunki.osm.pbf",
        "94f1a86cb8defaca4b6eea64fba699fde957a848151642b2ad2599bd5ad1e858",
    )
    population_grid = SampleDataSet(
        f"{BASE_URL}/helsinki_population_grid_2020.gpkg",
        "b421cb753fa00771b0e1d853422a0f485abb81f1bb2961eb832fa498612d7cd4",
    )

    __all__ += [
        "gtfs",
        "osm_pbf",
        "population_grid",
    ]

except ImportError:
    warnings.warn(
        "Install r5py>=0.1.1.dev1 to use the sample data sets",
        RuntimeWarning,
    )
