import rclpy
from rclpy import Node
from std_msgs.msg import String
import time
import board
import busio
from adafruit_pca9685 import PCA9685

# =========================
# PCA9685 setup
# =========================
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c, address=0x40)

# 1000 Hz is acceptable for many DC motor drivers.
# If your driver dislikes it, try 500 or 200.
pca.frequency = 1000

# =========================
# Motor channel mapping
# Each motor uses: PWM, IN1, IN2
# =========================
MOTOR_CHANNELS = {
    "RL": (0, 2, 1),
    "RR": (4, 5, 6),
    "FL": (8, 10, 9),
    "FR": (12, 13, 14),
}

# PCA9685 duty_cycle is 16-bit for the library interface.
FULL_ON = 0xFFFF
FULL_OFF = 0x0000

class max_motor_controller:

    def set_pwm_percent(channel: int, percent: float) -> None:
        percent = max(0.0, min(100.0, percent))
        duty = int((percent / 100.0) * 65535)
        pca.channels[channel].duty_cycle = duty


    def set_high(channel: int) -> None:
        pca.channels[channel].duty_cycle = FULL_ON


    def set_low(channel: int) -> None:
        pca.channels[channel].duty_cycle = FULL_OFF


    def motor_forward(name: str, speed_percent: float) -> None:
        """Forward: IN1=1, IN2=0, PWM=speed."""
        pwm_ch, in1_ch, in2_ch = MOTOR_CHANNELS[name]
        set_high(in1_ch)
        set_low(in2_ch)
        set_pwm_percent(pwm_ch, speed_percent)


    def motor_backward(name: str, speed_percent: float) -> None:
        """Backward: IN1=0, IN2=1, PWM=speed."""
        pwm_ch, in1_ch, in2_ch = MOTOR_CHANNELS[name]
        set_low(in1_ch)
        set_high(in2_ch)
        set_pwm_percent(pwm_ch, speed_percent)


    def motor_stop(name: str) -> None:
        """Stop motor."""
        pwm_ch, in1_ch, in2_ch = MOTOR_CHANNELS[name]
        set_low(in1_ch)
        set_low(in2_ch)
        set_pwm_percent(pwm_ch, 0)


    def forward(speed_percent: float) -> None:
        for motor in MOTOR_CHANNELS:
            motor_forward(motor, speed_percent)


    def backward(speed_percent: float) -> None:
        for motor in MOTOR_CHANNELS:
            motor_backward(motor, speed_percent)


    def stop() -> None:
        for motor in MOTOR_CHANNELS:
            motor_stop(motor)

    def right_shift(speed_percent: float) -> None:
        motor_forward('FL', speed_percent)
        motor_forward('RR', speed_percent)
        motor_backward('FR', speed_percent)
        motor_backward('RL', speed_percent)

    def left_shift(speed_percent: float) -> None:
        motor_forward('FR', speed_percent)
        motor_forward('RL', speed_percent)
        motor_backward('FL', speed_percent)
        motor_backward('RR', speed_percent)

    def fw_right_45(speed_percent: float) -> None:
        motor_forward('FL', speed_percent)
        motor_forward('RR', speed_percent)

    def fw_left_45(speed_percent: float) -> None:
        motor_forward('FR', speed_percent)
        motor_forward('RL', speed_percent)

    def bw_right_45(speed_percent: float) -> None:
        motor_backward('FR', speed_percent)
        motor_backward('RL', speed_percent)

    def bw_left_45(speed_percent: float) -> None:
        motor_backward('FL', speed_percent)
        motor_backward('RR', speed_percent)

    def rotate_cw(speed_percent: float) -> None:
        motor_forward('FL', speed_percent)
        motor_forward('RL', speed_percent)
        motor_backward('FR', speed_percent)
        motor_backward('RR', speed_percent)

    def rotate_ccw(speed_percent: float) -> None:
        motor_forward('FR', speed_percent)
        motor_forward('RR', speed_percent)
        motor_backward('FL', speed_percent)
        motor_backward('RL', speed_percent)
