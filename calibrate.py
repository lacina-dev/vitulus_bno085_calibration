# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
# Modified for VITULUS by robert@lacina.dev

import time
import adafruit_bno08x
from adafruit_bno08x.uart import BNO08X_UART

import serial
uart = serial.Serial("/dev/ttyUSB0", baudrate=3000000)
bno = BNO08X_UART(uart, debug=False)

bno.begin_calibration()
bno.enable_feature(adafruit_bno08x.BNO_REPORT_MAGNETOMETER)
bno.enable_feature(adafruit_bno08x.BNO_REPORT_GAME_ROTATION_VECTOR)
bno.enable_feature(adafruit_bno08x.BNO_REPORT_ACCELEROMETER)
bno.enable_feature(adafruit_bno08x.BNO_REPORT_GYROSCOPE)

start_time = time.monotonic()
time_get_status = time.monotonic()
calibration_good_at = None
mag_status, acc_status, gyro_status, game_status = bno.calibration_status
while True:
    time.sleep(0.02)

    # print("Magnetometer:")
    mag_x, mag_y, mag_z = bno.magnetic  # pylint:disable=no-member
    # print("X: %0.6f  Y: %0.6f Z: %0.6f uT" % (mag_x, mag_y, mag_z))
    # print("")

    # print("Game Rotation Vector Quaternion:")
    (
        game_quat_i,
        game_quat_j,
        game_quat_k,
        game_quat_real,
    ) = bno.game_quaternion  # pylint:disable=no-member
    # print(
    #     "I: %0.6f  J: %0.6f K: %0.6f  Real: %0.6f"
    #     % (game_quat_i, game_quat_j, game_quat_k, game_quat_real)
    # )

    if (time.monotonic() - time_get_status) > 2:
        mag_status, acc_status, gyro_status, game_status = bno.calibration_status
        time_get_status = time.monotonic()
        print(
            "Magnetometer Calibration quality:",
            adafruit_bno08x.REPORT_ACCURACY_STATUS[mag_status],
            " (%d)" % mag_status,
        )
        print(
            "Acc Calibration quality:",
            adafruit_bno08x.REPORT_ACCURACY_STATUS[acc_status],
            " (%d)" % acc_status,
        )
        print(
            "Gyro Calibration quality:",
            adafruit_bno08x.REPORT_ACCURACY_STATUS[gyro_status],
            " (%d)" % gyro_status,
        )
        print(
            "Game Calibration quality:",
            adafruit_bno08x.REPORT_ACCURACY_STATUS[game_status],
            " (%d)" % game_status,
        )
        print("**************************************************************")

    if not calibration_good_at and mag_status == 3 and acc_status == 3 and gyro_status == 3 and game_status == 3:
        calibration_good_at = time.monotonic()
    if mag_status < 3 or acc_status < 3 or gyro_status < 3 or game_status < 3:
        calibration_good_at = None
    if calibration_good_at and (time.monotonic() - calibration_good_at > 5.0):
        input_str = input("\n\nEnter S to save or anything else to continue: ")
        if input_str.strip().lower() == "s":
            bno.save_calibration_data()
            break

        calibration_good_at = None
    # print("**************************************************************")

print("calibration done")
