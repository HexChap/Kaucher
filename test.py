from app.controllers.launcher import get_current_launch_data, launch_java


launch_java(
    get_current_launch_data("1.7.10", "tesla")
)
