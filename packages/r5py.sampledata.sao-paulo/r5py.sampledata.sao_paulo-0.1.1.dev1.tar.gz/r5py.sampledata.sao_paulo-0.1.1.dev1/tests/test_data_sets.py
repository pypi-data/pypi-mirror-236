#!/usr/bin/env python3


import r5py.util


class TestDataSets:
    def test_download_and_checksum(self, data_sets):
        for data_set in data_sets:
            assert isinstance(data_set, r5py.util.data_set.DataSet)
            assert data_set.exists()
