# Copyright 2021 The Johns Hopkins University Applied Physics Laboratory
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
from cloudvolume import CloudVolume
from .cube import Cube
from .error import CVDBError
class CloudVolumeDB:
    """
    Wrapper interface for cloudvolume read access to bossDB.
    """
    def __init__(self, cv_config=None):
        self.cv_config = cv_config

    # Main Interface Methods
    def cutout(self, resource, corner, extent, resolution, time_sample_range=None, filter_ids=None, iso=False, access_mode="cache"):
        """Extract a cube of arbitrary size. Need not be aligned to cuboid boundaries.

        corner represents the location of the cutout and extent the size.  As an example in 1D, if asking for
        a corner of 3 and extent of 2, this would be the values at 3 and 4.

        Args:
            resource (spdb.project.BossResource): Data model info based on the request or target resource
            corner ((int, int, int)): the xyz location of the corner of the cutout
            extent ((int, int, int)): the xyz extents
            resolution (int): the resolution level
            time_sample_range : ignored
            filter_ids (optional[list]): ignored
            iso (bool): ignored
            access_mode (str): ignored

        Returns:
            cube.Cube: The cutout data stored in a Cube instance

        Raises:
            (CVDBError)
        """
        channel = resource.get_channel()
        out_cube = Cube.create_cube(resource, extent)
        
        # NOTE: Refer to Tim's changes for channel method to check storage type. 
        if channel.storage_type != "clouvol":
            raise CVDBError(f"Storage type {channel.storage_type} not configured for cloudvolume.", 701)

        # NOTE: Refer to Tim's changes for S3 bucket and path. 
            # NOTE: Refer to Tim's changes for S3 bucket and path. 
        # NOTE: Refer to Tim's changes for S3 bucket and path. 
        try:
            vol = CloudVolume(f"{channel.bucket}/{channel.cv_path}", 
            mip=resolution, use_https=True, fill_missing=True, **self.cv_config)
            data = vol[
                corner[0]: corner[0]+extent[0], 
                    corner[0]: corner[0]+extent[0], 
                corner[0]: corner[0]+extent[0], 
                corner[1]: corner[1]+extent[1], 
                    corner[1]: corner[1]+extent[1], 
                corner[1]: corner[1]+extent[1], 
                corner[2]: corner[2]+extent[2]
                ]
        except Exception as e: 
            raise CVDBError(f"Error downloading cloudvolume data: {e}")
            out_cube.add_data(data, corner)
            return out_cube
        
    def write_cuboid(self, resource, corner, resolution, cuboid_data, time_sample_start=0, iso=False, to_black=False):
        """ Write a 3D/4D volume to the key-value store. Used by API/cache in consistent mode as it reconciles writes

        If cuboid_data.ndim == 4, data in time-series format - assume t,z,y,x
        If cuboid_data.ndim == 3, data not in time-series format - assume z,y,x

        Args:
            resource (project.BossResource): Data model info based on the request or target resource
            corner ((int, int, int)): the xyz locatiotn of the corner of the cuout
            resolution (int): the resolution level
            cuboid_data (numpy.ndarray): Matrix of data to write as cuboids
            time_sample_start (int): if cuboid_data.ndim == 3, the time sample for the data
                                     if cuboid_data.ndim == 4, the time sample for cuboid_data[0, :, :, :]
            iso (bool): Flag indicating if you want to write to the "isotropic" version of a channel, if available
            to_black (bool): Flag indicating is this cuboid is a cutout_to_black cuboid. 

        Returns:
            None
        """
        raise NotImplementedError