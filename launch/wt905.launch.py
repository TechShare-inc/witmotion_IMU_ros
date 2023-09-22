import os
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    config = os.path.join(
        get_package_share_directory('witmotion_ros'),
        'config',
        'wt905.yml'
        )
    # Declare use_sim_time as an argument
    use_sim_time_arg = DeclareLaunchArgument(
        'sim',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )
    node=Node(
        package = 'witmotion_ros',
        executable = 'witmotion_ros_node',
        parameters = [config,
         {'use_sim_time': LaunchConfiguration('sim')}]
    )

    base_link_to_imu  =  Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name="base_link_to_velodyne",
            arguments='-0.08 0.0 0.25 0.0 0.0 0.0 base_footprint imu_link'.split(' '),
            output='screen',
            )
    ld.add_action(node)
    ld.add_action(base_link_to_imu)
    return ld