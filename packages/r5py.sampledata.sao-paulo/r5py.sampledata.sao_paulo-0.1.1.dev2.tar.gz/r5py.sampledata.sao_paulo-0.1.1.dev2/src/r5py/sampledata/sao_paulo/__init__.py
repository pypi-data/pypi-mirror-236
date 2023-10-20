#!/usr/bin/env python3


"""Sample data set for r5py, covering São Paulo city centre, downloaded upon first access."""


__version__ = "0.1.1.dev2"
__all__ = ["__version__"]


try:
    from r5py.util.sample_data_set import SampleDataSet

    BASE_URL = (
        f"https://github.com/r5py/r5py.sampledata.sao_paulo/raw/v{__version__}/data/"
    )

    gtfs = SampleDataSet(
        f"{BASE_URL}/spo_gtfs.zip",
        "57d0d5f3359cbd0d42cc7467c51ec9b14e0c9dc1665308246644fbc3bddd9a1f",
    )

    hexgrid_csv = SampleDataSet(
        f"{BASE_URL}/spo_hexgrid.csv",
        "769660f8f1bc95d2741bbc4225e5e0e77e73461ea8b3e225a58e397b0748bdd4",
    )

    hexgrid_gpkg = SampleDataSet(
        f"{BASE_URL}/spo_hexgrid_EPSG32723.gpkg.zip",
        "0c95ec2566627fae5dc049802cbba34effc2c01028dbd233f282957611f9aaca",
    )

    osm_pbf = SampleDataSet(
        f"{BASE_URL}/spo_osm.pbf",
        "5cb72c6df5428ca0b90d0646f9e9ebc32b6ac6b189b53f8afc7a239abfe4d2ef",
    )

    __all__ += [
        "gtfs",
        "hexgrid_csv",
        "hexgrid_gpkg",
        "osm_pbf",
    ]

except ImportError as exception:
    raise ImportError(
        "Install r5py>=0.1.1.dev1 to use the sample data sets"
    ) from exception
