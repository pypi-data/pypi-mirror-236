#!/usr/bin/env python3# (C) Copyright 2023 ECMWF and JSC
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF and JSC do not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#
#from __future__ import annotations

from typing import Union, List
import numpy as np
import pandas as pd
import xarray as xr
import climetlab as cml
from climetlab import Dataset
from climetlab.decorators import normalize

List_or_string = Union[List, str]

__version__ = "0.3.1"


URL = "https://object-store.os-api.cci1.ecmwf.int"
PATTERN = "{url}/maelstrom-ap5/maelstrom-downscaling-tier2_{date}.nc"

@normalize("x","date-list(%Y-%m)")
def DateListNormaliser(x):
    return x

class Downscaling(Dataset):
    class_name = "Downsclaing_Dataset"
    name = "Tier-2 dataset based on ERA 5 and COSMO REA6 reanalysis data"
    home_page = "https://git.ecmwf.int/projects/MLFET/repos/maelstrom-downscaling-ap5"
    licence = "Apache Licence Version 2.0"
    documentation = "-"
    citation = "-"
    terms_of_use = (
        "By downloading data from this dataset, you agree to the terms and conditions defined at "
        "https://git.ecmwf.int/projects/MLFET/repos/maelstrom-downscaling-ap5/browse/climetlab-maelstrom-downscaling-ap5/LICENSE"
        "If you do not agree with such terms, do not download the data. "
    )

    dataset = None

    dates_all = pd.date_range("2006-01-01", "2018-12-01", freq="MS")

    all_datelist = DateListNormaliser(dates_all)    

    dataset_types = {"training": dates_all[dates_all.year.isin(list(np.arange(2006, 2017)))],
                     "validation": dates_all[dates_all.year.isin([2017])],
                     "testing": dates_all[dates_all.year.isin([2018])]}

    default_datelist = dataset_types["training"]

    def __init__(self, months: List = None, dataset: str = None):
        """
        Initialize data loader instance
        :param months: list of months for which downscaling data is requested
        :param dataset: name of dataset (see dataset_types-dictionary)
        """
        method = "{0}->{1}".format(Downscaling.class_name, Downscaling.__init__.__name__)

        assert not (months is None and dataset is None), "%{0}: Either list of months or dataset-name must be passed."\
                                                         .format(method)
        if (not dataset is None) and (not months is None):
            print("%{0}: List of months and dataset-name cannot be processed simultaneously. months will be ignored."
                  .format(method))

        if dataset is None:
            self.date = self.parse_date(months)
        else:
            if not dataset in self.dataset_types.keys():
                raise ValueError("%{0}: Unknown dataset type {1} passed. Valid choices are [{2}]"
                                 .format(method, dataset, ",".join(self.dataset_types.keys())))
            self.date = self.parse_date(self.dataset_types[dataset])
        
        # get the requested data
        self._load()

    def _load(self):
        """
        Builds the URL-request and retrieves the data
        :return: -
        """
        request_dict = dict(url=URL, date=self.date)
        self.source = cml.load_source("url-pattern", PATTERN, request_dict, merger=Merger())

    def parse_date(self, dates: List_or_string):
        """
        Parse individual date or list of dates for downscaling dataset
        :param dates: list of dates (months) or individual month
        :return: normalized date string suitable for requiring downscaling data
        """
        method = "{0}->{1}".format(Downscaling.class_name, Downscaling.__init__.__name__)

        if dates is None:
            dates = self.default_datelist
        
        dates = DateListNormaliser(dates)
        
        check_date = [d for d, date in enumerate(dates) if date not in self.all_datelist]
        if check_date:
            print("%{0}: The following passed months are not available in the dataset:".format(method))
            for index in check_date:
                print("* {0}".format(dates[index]))
            raise ValueError("%{0}: Unavailable months requested. Check your input.".format(method))

        return dates

class Merger:
    def __init__(self, engine: str = "netcdf4", options=None):
        """Initializes merger based on xarray's open_mfdataset.
        :param engine: Engine to read netCDF-files (see open_mfdataset-documentation for more details).
        :param options: Additional options passed to open_mfdataset.
        :return: -
        """
        self.engine = engine
        self.options = options if options is not None else {}

    def to_xarray(self, paths: List):
        """
        Merger to read data from multiple netCDF-files
        :param paths: list containing paths to netCDF-data files to be read
        :return: -
        """
        return xr.open_mfdataset(
            paths,
            engine=self.engine,
            parallel=True,
            **self.options
       )
