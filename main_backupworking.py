#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# F1 25 – Essential Telemetry (UDP 2025) – prints player's key data in real time

import socket, struct, time
from datetime import datetime

UDP_IP = "0.0.0.0"
UDP_PORT = 20777
SOCKET_TIMEOUT = 2.0
PRINT_PERIOD = 1.0

HEADER_LEN = 29           # PacketHeader is 29 bytes (packed, little-endian) in 2025
ID_CAR_TELEMETRY = 6
ID_CAR_STATUS    = 7
CAR_TEL_BLOCK    = 60     # bytes per car in CarTelemetry
CAR_STA_BLOCK    = 55     # ~55 bytes per car in CarStatus (enough for our offsets)
MAX_CARS         = 22

def main():
    print("=== F1 25: Essential Telemetry (UDP 20777, format 2025) ===")
    print("Telemetry ON, Format=2025, Port=20777. Intră pe pistă.\n")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(SOCKET_TIMEOUT)
    sock.bind((UDP_IP, UDP_PORT))

    player_idx = None
    # Telemetry (ID 6)
    speed = 0
    throttle = steer = brake = 0.0
    gear = 0
    rpm  = 0
    drs_active = 0
    tyres_surf = [None, None, None, None]   # RL, RR, FL, FR (vom reordona la print)
    # Status (ID 7)
    drs_allowed = 0
    fuel_laps = None
    ers_j = None

    last_print = time.monotonic()

    try:
        while True:
            try:
                data, _ = sock.recvfrom(4096)
            except socket.timeout:
                pass
            else:
                if len(data) < HEADER_LEN:
                    continue

                packet_id = data[6]    # correct for 2025
                player_idx = data[27]  # correct for 2025
                if player_idx >= MAX_CARS:
                    continue

                if packet_id == ID_CAR_TELEMETRY:
                    base = HEADER_LEN + CAR_TEL_BLOCK * player_idx
                    if len(data) >= base + CAR_TEL_BLOCK:
                        speed    = struct.unpack_from("<H", data, base + 0)[0]
                        throttle = struct.unpack_from("<f", data, base + 2)[0]
                        steer    = struct.unpack_from("<f", data, base + 6)[0]
                        brake    = struct.unpack_from("<f", data, base + 10)[0]
                        gear     = struct.unpack_from("<b", data, base + 15)[0]
                        rpm      = struct.unpack_from("<H", data, base + 16)[0]
                        drs_active = data[base + 18]
                        tyres_surf = list(data[base + 30 : base + 34])  # RL, RR, FL, FR

                elif packet_id == ID_CAR_STATUS:
                    base = HEADER_LEN + CAR_STA_BLOCK * player_idx
                    if len(data) >= base + CAR_STA_BLOCK:
                        fuel_laps    = struct.unpack_from("<f", data, base + 13)[0]
                        drs_allowed  = data[base + 23]
                        ers_j        = struct.unpack_from("<f", data, base + 41)[0]

            now = time.monotonic()
            if now - last_print >= PRINT_PERIOD:
                ts = datetime.now().strftime("%H:%M:%S")
                def fmt(x, suf=""):
                    if x is None: return "—"
                    return f"{x:.1f}{suf}" if isinstance(x, float) else f"{x}{suf}"

                if all(t is not None for t in tyres_surf):
                    FL, FR, RL, RR = tyres_surf[2], tyres_surf[3], tyres_surf[0], tyres_surf[1]
                    tyres = f"{FL}°C/{FR}°C/{RL}°C/{RR}°C"
                else:
                    tyres = "—/—/—/—"

                print(
                    f"[{ts}] SPD={speed:>3d} km/h  GEAR={gear:>2d}  RPM={rpm:>5d}  "
                    f"THR={fmt(throttle)}  BRK={fmt(brake)}  STR={fmt(steer)}  "
                    f"DRS={'ON' if drs_active else 'OFF'}  ALW={'Y' if drs_allowed else 'N'}  "
                    f"ERS={fmt(ers_j,' J')}  Fuel≈{fmt(fuel_laps,' laps')}  "
                    f"Tyres FL/FR/RL/RR={tyres}"
                )
                last_print = now

    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
