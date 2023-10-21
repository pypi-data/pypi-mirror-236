from ..crazy import CrazyDragon

from threading import Thread

from .._base._navigation_base.imu       import IMU
from .._base._navigation_base.imu_setup import preflight_sequence
from .._base._navigation_base.qualisys  import Qualisys

from time import sleep



class Navigation( Thread ):

    def __init__( self, cf: CrazyDragon, config ):

        super().__init__()

        self.daemon = True

        self.cf = cf

        self.imu = IMU( cf )
        self.qtm = Qualisys( config['body_name'] )

        self.navigate = True


    @classmethod
    def _on_pose( cls, cf: CrazyDragon, data: list ):
        
        cf.pos[:] = data[0:3]
        cf.att[:] = data[3:6]

        cf.extpos.send_extpos( data[0], data[1], data[2] )


    def run( self ):

        cf = self.cf

        imu = self.imu
        qtm = self.qtm

        preflight_sequence( cf )

        sleep( 1 )

        imu.start_get_acc()
        imu.start_get_vel()

        qtm.on_pose = lambda pose: __class__._on_pose( cf, pose )

        while self.navigate:

            sleep( 0.1 )


    def join( self ):

        self.navigate = False

        super().join()