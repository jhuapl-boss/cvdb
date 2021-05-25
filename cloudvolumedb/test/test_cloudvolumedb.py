import numpy as np
from cloudvolume import CloudVolume

from cvdb.cloudvolumedb import Cube, CloudVolumeDB, CVDBError
from cvdb.project import BossResourceBasic
from cvdb.project.test.resource_setup import get_image_dict, get_anno_dict

class CloudvolumeDBImageDataTestMixin(object):

    CHUNKSIZE = (512, 512, 16)

    def write_test_cube(self, cv, resource, res, cube, corner=(0,0,0)):
        """
        Method to write data to test read operations.
        Args:
            cv (cvdb.CloudVolumeDatabase): cloudvolume database (not used since we dont have write yet)
            resource (spdb.project.BossResource): Data model info based on the request or target resource
            res (int): resolution
            corner (tuple(int)) : bottom left corner of the data
            cube (bytes): cube data in XYZ

        Returns:
            True if cube written succesfully, False otherwise.
        """
        channel = resource.get_channel()
        coord_frame = resource.get_coord_frame()
        extents = [
            coord_frame.x_stop - coord_frame.x_start,
            coord_frame.y_stop - coord_frame.y_start,
            coord_frame.z_stop - coord_frame.z_start
        ]
        data = cube.data
        info = CloudVolume.create_new_info(
            num_channels = 1,
            layer_type = 'image' if channel.type == 'image' else 'segmentation', 
            data_type = channel.datatype, 
            encoding = 'raw', 
            resolution = [ coord_frame.x_voxel_size, coord_frame.y_voxel_size, coord_frame.z_voxel_size ], 
            voxel_offset = [ coord_frame.x_start, coord_frame.y_start, coord_frame.z_start ],
            chunk_size = self.CHUNKSIZE, 
            volume_size = extents
        )

        vol = CloudVolume(f"s3://{channel.bucket}/{channel.cv_path}", info=info)
        vol.commit_info()

        vol[
            corner[0]: corner[0]+data.shape[0], 
            corner[1]: corner[1]+data.shape[1], 
            corner[2]: corner[2]+data.shape[2]
            ] = data

    def test_cutout_aligned_single(self):
        """Test the cutout method - aligned - single"""
        # Generate random data
        cube1 = Cube.create_cube(self.resource, self.CHUNKSIZE)
        cube1.random()

        db = CloudVolumeDB()

        # populate dummy data
        self.write_test_cube(db, self.resource, 0, cube1)

        cube2 = db.cutout(self.resource, (0, 0, 0), self.CHUNKSIZE, 0)

        np.testing.assert_array_equal(cube1.data, cube2.data)

    def test_cutout_misalgined_single(self, fake_get_region):
        """Test the cutout method - misaligned - single"""
        # Generate random data
        cube1 = Cube.create_cube(self.resource, self.CHUNKSIZE)
        cube1.random()

        db = CloudVolumeDB()

        # populate dummy data
        self.write_test_cube(db, self.resource, 0, cube1, corner=(256, 256, 8))

        cube2 = db.cutout(self.resource, (256, 256, 8), self.CHUNKSIZE, 0)

        np.testing.assert_array_equal(cube1.data, cube2.data)

    def test_cutout_aligned_multiple(self):
        """Test the cutout method - aligned - multiple"""
        # Generate random data
        extents = [4*x for x in self.CHUNKSIZE] 
        cube1 = Cube.create_cube(self.resource, extents)
        cube1.random()

        db = CloudVolumeDB()

        # populate dummy data
        self.write_test_cube(db, self.resource, 0, cube1)

        cube2 = db.cutout(self.resource, (0, 0, 0), extents, 0)

        np.testing.assert_array_equal(cube1.data, cube2.data)

    def test_cutout_misalgined_multiple(self, fake_get_region):
        """Test the cutout method - misaligned - multiple"""
        extents = [4*x for x in self.CHUNKSIZE] 
        # Generate random data
        cube1 = Cube.create_cube(self.resource, extents)
        cube1.random()

        db = CloudVolumeDB()

        # populate dummy data
        self.write_test_cube(db, self.resource, 0, cube1, corner=(256, 256, 8))

        cube2 = db.cutout(self.resource, (256, 256, 8), extents, 0)

        np.testing.assert_array_equal(cube1.data, cube2.data)


class TestCloudvolumeDBImage8Data(CloudvolumeDBImageDataTestMixin, unittest.TestCase):

    def setUp(self):
        """ Set everything up for testing """
        self.data = get_image_dict()
        self.resource = BossResourceBasic(self.data)


    def tearDown(self):
        pass


class TestCloudvolumeDBImage16Data(CloudvolumeDBImageDataTestMixin, unittest.TestCase):


    def setUp(self):
        """ Set everything up for testing """
        self.data = get_image_dict(uint16=True)
        self.resource = BossResourceBasic(self.data)


    def tearDown(self):
        pass

class TestCloudvolumeDBAnnotation64Data(CloudvolumeDBImageDataTestMixin, unittest.TestCase):


    def setUp(self):
        """ Set everything up for testing """
        self.data = get_anno_dict()
        self.resource = BossResourceBasic(self.data)


    def tearDown(self):
        pass