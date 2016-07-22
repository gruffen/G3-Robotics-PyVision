# Sets the appropriate camera exposure and other settings before running the vision processing code

v4l2-ctl -d /dev/video1 -c exposure_auto=1 -c exposure_absolute=4
chmod +x new_find_high_goal.py
python new_find_high_goal.py
