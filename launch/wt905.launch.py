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

    ld.add_action(node)
    return ld