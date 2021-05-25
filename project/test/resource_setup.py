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

def get_image_dict(uint16=False):
    """Method to generate an initial set of parameters to use to instantiate a basic resource for an IMAGE dataset
    Args:
        uint16 (bool) : whether to generate for uint16 dataset or uint8 dataset. False by default.
    Returns:
        dict - a dictionary of data to initialize a basic resource

    """
    data = {}

    data['collection'] = {}
    data['collection']['name'] = "col1"
    data['collection']['description'] = "Test collection 1"

    data['coord_frame'] = {}
    data['coord_frame']['name'] = "coord_frame_1"
    data['coord_frame']['description'] = "Test coordinate frame"
    data['coord_frame']['x_start'] = 0
    data['coord_frame']['x_stop'] = 2000
    data['coord_frame']['y_start'] = 0
    data['coord_frame']['y_stop'] = 5000
    data['coord_frame']['z_start'] = 0
    data['coord_frame']['z_stop'] = 200
    data['coord_frame']['x_voxel_size'] = 4
    data['coord_frame']['y_voxel_size'] = 4
    data['coord_frame']['z_voxel_size'] = 35
    data['coord_frame']['voxel_unit'] = "nanometers"

    data['experiment'] = {}
    data['experiment']['name'] = "exp1"
    data['experiment']['description'] = "Test experiment 1"
    data['experiment']['num_hierarchy_levels'] = 7
    data['experiment']['hierarchy_method'] = 'anisotropic'
    data['experiment']['num_time_samples'] = 0
    data['experiment']['time_step'] = 0
    data['experiment']['time_step_unit'] = "na"

    data['channel'] = {}
    data['channel']['description'] = "Test channel 1"
    data['channel']['type'] = "image"
    data['channel']['base_resolution'] = 0
    data['channel']['sources'] = []
    data['channel']['related'] = []
    data['channel']['default_time_sample'] = 0
    data['channel']['downsample_status'] = "NOT_DOWNSAMPLED"
    data['channel']['storage_type'] = "cloudvol"
    data['channel']['bucket'] = "bossdb-test-data"

    if uint16:
        data['boss_key'] = 'col1&exp1&ch2'
        data['lookup_key'] = '4&3&3'
        data['channel']['name'] = 'ch2'
        data['channel']['datatype'] = 'uint16'
        data['channel']['cv_path'] = 'col1/exp1/chan2'
    else:
        data['boss_key'] = 'col1&exp1&ch1'
        data['lookup_key'] = '4&3&2'
        data['channel']['name'] = 'ch1'
        data['channel']['datatype'] = 'uint8'
        data['channel']['cv_path'] = 'col1/exp1/chan1'
        
    return data


def get_anno_dict(boss_key='col1&exp1&ch2', lookup_key='4&3&345'):
    """Method to generate an initial set of parameters to use to instantiate a basic resource for an ANNOTATION dataset

    Args:
        boss_key (optional[string]): Optionally override default value.  Defaults to 'col1&exp1&ch2'.
        lookup_key (optional[string]): Optionally override default value.  Defaults to '4&3&345'.

    Returns:
        dict - a dictionary of data to initialize a basic resource
    """
    data = get_image_dict()
    data['channel']['name'] = "anno1"
    data['channel']['description'] = "Test annotation channel 1"
    data['channel']['type'] = "annotation"
    data['channel']['datatype'] = 'uint64'
    data['channel']['base_resolution'] = 0
    data['channel']['sources'] = ["ch1"]
    data['channel']['default_time_sample'] = 0
    data['channel']['cv_path'] = "col1/exp1/anno1"
    data['boss_key'] = boss_key
    data['lookup_key'] = lookup_key

    return data
