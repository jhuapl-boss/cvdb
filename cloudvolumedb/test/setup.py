from cloudvolume import CloudVolume
from cvdb.project import BossResourceBasic


def create_new_cloudvolume(resource, chunksize):
    """
    Creates a new cloudvolume resource in S3 for testing purposes.
    """
    channel = resource.get_channel()
    coord_frame = resource.get_coord_frame()
    extents = [
        coord_frame.x_stop - coord_frame.x_start,
        coord_frame.y_stop - coord_frame.y_start,
        coord_frame.z_stop - coord_frame.z_start
    ]
    info = CloudVolume.create_new_info(
        num_channels = 1,
        layer_type = 'image' if channel.type == 'image' else 'segmentation', 
        data_type = channel.datatype, 
        encoding = 'raw', 
        resolution = [ coord_frame.x_voxel_size, coord_frame.y_voxel_size, coord_frame.z_voxel_size ], 
        voxel_offset = [ coord_frame.x_start, coord_frame.y_start, coord_frame.z_start ],
        chunk_size = chunksize, 
        volume_size = extents
    )

    vol = CloudVolume(f"s3://{channel.bucket}/{channel.cv_path}", info=info, fill_missing=True)
    vol.commit_info()
    return vol