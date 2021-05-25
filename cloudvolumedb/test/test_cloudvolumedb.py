import unittest
import numpy as np
from cloudvolume import CloudVolume

from cvdb.cloudvolumedb import Cube, CloudVolumeDB, CVDBError
from cvdb.project import BossResourceBasic
from cvdb.project.test.resource_setup import get_image_dict, get_anno_dict
from .setup import create_new_cloudvolume

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
        data = np.squeeze(cube.data).T

        self.vol[
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

    def test_cutout_misalgined_single(self):
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
        extents = [2*x for x in self.CHUNKSIZE] 
        cube1 = Cube.create_cube(self.resource, extents)
        cube1.random()

        db = CloudVolumeDB()

        # populate dummy data
        self.write_test_cube(db, self.resource, 0, cube1)

        cube2 = db.cutout(self.resource, (0, 0, 0), extents, 0)

        np.testing.assert_array_equal(cube1.data, cube2.data)

    def test_cutout_misalgined_multiple(self):
        """Test the cutout method - misaligned - multiple"""
        extents = [2*x for x in self.CHUNKSIZE] 
        # Generate random data
        cube1 = Cube.create_cube(self.resource, extents)
        cube1.random()

        db = CloudVolumeDB()

        # populate dummy data
        self.write_test_cube(db, self.resource, 0, cube1, corner=(256, 256, 8))

        cube2 = db.cutout(self.resource, (256, 256, 8), extents, 0)

        np.testing.assert_array_equal(cube1.data, cube2.data)


class TestCloudvolumeDBImage8Data(CloudvolumeDBImageDataTestMixin, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Set everything up for testing """
        # Set up BossResource
        cls.data = get_image_dict()
        cls.resource = BossResourceBasic(cls.data)

        # Set up external cloudvolume instance
        cls.vol = create_new_cloudvolume(cls.resource, cls.CHUNKSIZE)


class TestCloudvolumeDBImage16Data(CloudvolumeDBImageDataTestMixin, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Set everything up for testing """
        cls.data = get_image_dict(uint16=True)
        cls.resource = BossResourceBasic(cls.data)

        # Set up external cloudvolume instance
        cls.vol = create_new_cloudvolume(cls.resource, cls.CHUNKSIZE)

class TestCloudvolumeDBAnnotation64Data(CloudvolumeDBImageDataTestMixin, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Set everything up for testing """
        cls.data = get_anno_dict()
        cls.resource = BossResourceBasic(cls.data)
        
        # Set up external cloudvolume instance
        cls.vol = create_new_cloudvolume(cls.resource, cls.CHUNKSIZE)
