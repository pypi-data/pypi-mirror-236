from pydantic import BaseModel

from albatros.enums import CommandResult, MissionResult, MissionType


class MavMessage(BaseModel):
    """MAVLink message super class."""

    mavpackettype: str = "UNKNOWN"
    """Message name."""

    timestamp_ms: int = -1
    """Received timestamp (ms)."""


class Heartbeat(MavMessage):
    """The heartbeat message shows that a system or component is present and responding.
    The type and autopilot fields (along with the message component id), allow the receiving system
    to treat further messages from this system appropriately (e.g. by laying out the user interface based on the autopilot).
    """

    type: int = 0
    """Vehicle or component type. For a flight controller component the vehicle type (quadrotor, helicopter, etc.).
    For other components the component type (e.g. camera, gimbal, etc.).
    This should be used in preference to component id for identifying the component type.
    """
    autopilot: int = 0
    """Autopilot type / class. Use MAV_AUTOPILOT_INVALID for components that are not flight controllers."""
    base_mode: int = 0
    """System mode bitmap."""
    custom_mode: int = 0
    """A bitfield for use for autopilot-specific flags."""
    system_status: int = 0
    """System status flag."""
    mavlink_version: int = 0
    """MAVLink version, not writable by user, gets added by protocol because of magic data type: uint8_t_mavlink_version."""


class GlobalPositionInt(MavMessage):
    """The filtered global position (e.g. fused GPS and accelerometers).
    The position is in GPS-frame (right-handed, Z-up). It is designed as scaled integer
    message since the resolution of float is not sufficient.
    """

    time_boot_ms: int = 0
    """Time since system boot (ms)."""
    lat: int = 0
    """Latitude, expressed (degE7)."""
    lon: int = 0
    """Longitude, expressed (degE7)."""
    alt: int = 0
    """Altitude (MSL). Note that virtually all GPS modules provide both WGS84 and MSL (mm)."""
    relative_alt: int = 0
    """Altitude above ground (mm)."""
    vx: int = 0
    vy: int = 0
    vz: int = 0
    hdg: int = 0


class SysStatus(MavMessage):
    """The general system state."""

    onboard_control_sensors_present: int = 0
    """Bitmap showing which onboard controllers and sensors are present.
    Value of 0: not present. Value of 1: present.
    """
    onboard_control_sensors_enabled: int = 0
    """Bitmap showing which onboard controllers and sensors are enabled.
    Value of 0: not enabled. Value of 1: enabled.
    """
    onboard_control_sensors_health: int = 0
    """Bitmap showing which onboard controllers and sensors have an error (or are operational).
    Value of 0: error. Value of 1: healthy.
    """
    load: int = 0
    """Maximum usage in percent of the mainloop time. Values: [0-1000]."""
    voltage_battery: int = 0
    """Battery voltage, UINT16_MAX: Voltage not sent by autopilot."""
    current_battery: int = 0
    """Battery current, -1: Current not sent by autopilot."""
    battery_remaining: int = 0
    """Battery energy remaining, -1: Battery remaining energy not sent by autopilot."""
    drop_rate_comm: int = 0
    """Communication drop rate, (UART, I2C, SPI, CAN), dropped packets on all links
    (packets that were corrupted on reception on the MAV).
    """


class GPSRawInt(MavMessage):
    """The global position, as returned by the Global Positioning System (GPS).
    This is NOT the global position estimate of the system, but rather a RAW sensor value.
    """

    time_usec: int = 0
    """Timestamp (UNIX Epoch time or time since system boot)."""
    fix_type: int = 0
    """GPS fix type."""
    lat: int = 0
    """Latitude (WGS84)"""
    lon: int = 0
    """Longitude (WGS84)"""
    alt: int = 0
    """Altitude (MSL). Positive for up. Note that virtually all GPS modules provide the MSL altitude in addition to the WGS84 altitude."""
    eph: int = 0
    """GPS HDOP horizontal dilution of position (unitless * 100). If unknown, set to: UINT16_MAX."""
    epv: int = 0
    """GPS VDOP vertical dilution of position (unitless * 100). If unknown, set to: UINT16_MAX."""
    vel: int = 0
    """GPS ground speed. If unknown, set to: UINT16_MAX."""
    cog: int = 0
    """Course over ground (NOT heading, but direction of movement) in degrees * 100, 0.0..359.99 degrees.
    If unknown, set to: UINT16_MAX
    """
    satellites_visible: int = 0
    """Number of satellites visible. If unknown, set to UINT8_MAX."""
    alt_ellipsoid: int = 0
    """Altitude (above WGS84, EGM96 ellipsoid). Positive for up."""
    h_acc: int = 0
    """Position uncertainty."""
    v_acc: int = 0
    """Altitude uncertainty."""
    vel_acc: int = 0
    """Speed uncertainty."""
    hdg_acc: int = 0
    """Heading / track uncertainty"""
    yaw: int = 0
    """Yaw in earth frame from north. Use 0 if this GPS does not provide yaw.
    Use UINT16_MAX if this GPS is configured to provide yaw and is currently unable to provide it. Use 36000 for north.
    """


class GPSStatus(MavMessage):
    """The positioning status, as reported by GPS. This message is intended
    to display status information about each satellite visible to the receiver.
    This message can contain information for up to 20 satellites.
    """

    satellites_visible: int = 0
    """Number of satellites visible."""
    satellite_prn: int = 0
    """Global satellite ID."""
    satellite_used: int = 0
    "0: Satellite not used, 1: used for localization."
    satellite_elevation: int = 0
    """Elevation (0: right on top of receiver, 90: on the horizon) of satellite."""
    satellite_azimuth: int = 0
    """Direction of satellite, 0: 0 deg, 255: 360 deg."""
    satellite_snr: int = 0
    """Signal to noise ratio of satellite."""


class Attitude(MavMessage):
    """The attitude in the aeronautical frame (right-handed, Z-down, Y-right, X-front, ZYX, intrinsic)."""

    time_boot_ms: int = 0
    """Time since system boot (ms)."""
    roll: float = 0
    """Roll angle (-pi..+pi)."""
    pitch: float = 0
    """Pitch angle (-pi..+pi)."""
    yaw: float = 0
    """Yaw angle (-pi..+pi)."""
    rollspeed: float = 0
    """Roll angular speed."""
    pitchspeed: float = 0
    """Pitch angular speed."""
    yawspeed: float = 0
    """Yaw angular speed."""


class RcChannelsRaw(MavMessage):
    """The RAW values of the RC channels received. The standard PPM modulation
    is as follows: 1000 microseconds: 0%, 2000 microseconds: 100%.
    """

    time_boot_ms: int = 0
    """Time since system boot (ms)."""
    port: int = 0
    """Servo output port (set of 8 outputs = 1 port).
    Flight stacks running on Pixhawk should use: 0 = MAIN, 1 = AUX.
    """
    chan1_raw: int = 0
    """RC channel 1 value."""
    chan2_raw: int = 0
    """RC channel 2 value."""
    chan3_raw: int = 0
    """RC channel 3 value."""
    chan4_raw: int = 0
    """RC channel 4 value."""
    chan5_raw: int = 0
    """RC channel 5 value."""
    chan6_raw: int = 0
    """RC channel 6 value."""
    chan7_raw: int = 0
    """RC channel 7 value."""
    chan8_raw: int = 0
    """RC channel 8 value."""
    rssi: int = 0
    """Receive signal strength indicator in device-dependent units/scale.
    Values: [0-254], UINT8_MAX: invalid/unknown.
    """


class ServoOutputRaw(MavMessage):
    """The RAW values of the servo outputs. The standard PPM
    modulation is as follows: 1000 microseconds: 0%, 2000 microseconds: 100%.
    """

    time_usec: int = 0
    """Timestamp (UNIX Epoch time or time since system boot)."""
    servo1_raw: int = 0
    """Servo output 1 value"""
    servo2_raw: int = 0
    """Servo output 2 value"""
    servo3_raw: int = 0
    """Servo output 3 value"""
    servo4_raw: int = 0
    """Servo output 4 value"""
    servo5_raw: int = 0
    """Servo output 5 value"""
    servo6_raw: int = 0
    """Servo output 6 value"""
    servo7_raw: int = 0
    """Servo output 7 value"""
    servo8_raw: int = 0
    """Servo output 8 value"""
    servo9_raw: int = 0
    """Servo output 9 value"""
    servo10_raw: int = 0
    """Servo output 10 value"""
    servo11_raw: int = 0
    """Servo output 11 value"""
    servo12_raw: int = 0
    """Servo output 12 value"""
    servo13_raw: int = 0
    """Servo output 13 value"""
    servo14_raw: int = 0
    """Servo output 14 value"""
    servo15_raw: int = 0
    """Servo output 15 value"""
    servo16_raw: int = 0
    """Servo output 16 value"""


class RadioStatus(MavMessage):
    """Status generated by radio and injected into MAVLink stream."""

    rssi: int = 0
    """Local (message sender) received signal strength indication in device-dependent units/scale.
    Values: [0-254], UINT8_MAX: invalid/unknown.
    """
    remrssi: int = 0
    """Remote (message receiver) signal strength indication in device-dependent units/scale.
    Values: [0-254], UINT8_MAX: invalid/unknown.
    """
    txbuf: int = 0
    """Remaining free transmitter buffer space."""
    noise: int = 0
    """Local background noise level. These are device dependent RSSI values (scale as approx 2x dB on SiK radios).
    Values: [0-254], UINT8_MAX: invalid/unknown.
    """
    remnoise: int = 0
    """Remote background noise level. These are device dependent RSSI values (scale as approx 2x dB on SiK radios).
    Values: [0-254], UINT8_MAX: invalid/unknown.
    """
    rxerrors: int = 0
    """Count of radio packet receive errors (since boot)."""
    fixed: int = 0
    """Count of error corrected radio packets (since boot)."""


class MissionRequestInt(MavMessage):
    """Request the information of the mission item with the sequence number seq.
    The response of the system to this message should be a MISSION_ITEM_INT message.
    https://mavlink.io/en/services/mission.html
    """

    target_system: int = 0
    target_component: int = 0
    seq: int = 0
    mission_type: MissionType = MissionType.MISSION


class MissionACK(MavMessage):
    """Acknowledgment message during waypoint handling. The type field states
    if this message is a positive ack (type=0) or if an error happened (type=non-zero).
    """

    target_system: int = 0
    target_component: int = 0
    type: MissionResult = MissionResult.NOT_RECEIVED
    mission_type: MissionType = MissionType.MISSION


class MissionItemReached(MavMessage):
    """A certain mission item has been reached."""

    seq: int = 0
    """Sequence number of reached mission item."""


class CommandACK(MavMessage):
    """Report status of a command. Includes feedback whether the command was executed.
    The command microservice is documented at https://mavlink.io/en/services/command.html
    """

    command: int = 0
    """Command ID."""
    result: CommandResult = CommandResult.NOT_RECEIVED
    """Command result."""


class ParamValue(MavMessage):
    """Emit the value of a onboard parameter. The parameter microservice is documented at
    https://mavlink.io/en/services/parameter.html
    """

    param_id: str = ""
    param_value: float = 0.0
    param_type: int = 0
    param_count: int = 0
    """"Total number of onboard parameters"""
    param_index: int = 0
    """Index of this onboard parameter"""
