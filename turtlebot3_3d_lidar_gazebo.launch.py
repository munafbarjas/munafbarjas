from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.parameter_descriptions import ParameterValue, Path
from launch.substitutions import Command
import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node




def generate_launch_description():
    model = os.environ.get('TURTLEBOT3_MODEL', 'waffle_pi')
    urdf_file = os.path.join(
        get_package_share_directory('turtlebot3_description'),
        'urdf', f'turtlebot3_{model}.urdf'
    )

    robot_description = ParameterValue(Command(['xacro ', urdf_file]), value_type=str)
    

    return LaunchDescription([
        # Gazebo
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory('gazebo_ros'),
                    'launch', 'gazebo.launch.py')),
        ),

        # URDF publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[
                {'robot_description': robot_description},
                {'use_sim_time': True}
            ],
            output='screen'
        ),

        # joint state publisher
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            parameters=[{'use_sim_time': True}],
            output='screen'
        ),



        # Spawn robot into Gazebo
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-topic', 'robot_description', '-entity', 'turtlebot3'],
            output='screen'
        )


   


    ])
