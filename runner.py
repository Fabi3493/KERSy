
import socket
import time
from datetime import datetime
from typing import Optional

import f1_constants as C
from telemetry_state import TelemetryState
from f1_parser import parse_header, parse_car_telemetry, parse_car_status

def fmt(v, suf=""):
    if v is None:
        return "—"
    return f"{v:.1f}{suf}" if isinstance(v, float) else f"{v}{suf}"

def format_tyre_string(tyres_surf):
    # tyres_surf is RL, RR, FL, FR → print FL, FR, RL, RR
    if all(t is not None for t in tyres_surf):
        FL, FR, RL, RR = tyres_surf[2], tyres_surf[3], tyres_surf[0], tyres_surf[1]
        return f"{FL}°C/{FR}°C/{RL}°C/{RR}°C"
    return "—/—/—/—"

def run():
    print("=== F1 25: Essential Telemetry (modular) ===")
    print(f"Listening on {C.UDP_IP}:{C.UDP_PORT}  |  Telemetry ON, Format=2025, Port=20777. Go on track.\n")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(C.SOCKET_TIMEOUT)
    sock.bind((C.UDP_IP, C.UDP_PORT))

    state = TelemetryState()
    last_print = time.monotonic()

    try:
        while True:
            try:
                data, _ = sock.recvfrom(4096)
            except socket.timeout:
                pass
            else:
                hdr = parse_header(data)
                if not hdr:
                    continue
                packet_id, player_idx = hdr

                if packet_id == C.ID_CAR_TELEMETRY:
                    tel = parse_car_telemetry(data, player_idx)
                    if tel:
                        state.speed = tel["speed"]
                        state.throttle = tel["throttle"]
                        state.steer = tel["steer"]
                        state.brake = tel["brake"]
                        state.gear = tel["gear"]
                        state.rpm = tel["rpm"]
                        state.drs_active = tel["drs_active"]
                        state.tyres_surf = tel["tyres_surf"]

                elif packet_id == C.ID_CAR_STATUS:
                    sta = parse_car_status(data, player_idx)
                    if sta:
                        state.fuel_laps = sta["fuel_laps"]
                        state.drs_allowed = sta["drs_allowed"]
                        state.ers_j = sta["ers_j"]

            now = time.monotonic()
            if now - last_print >= C.PRINT_PERIOD:
                ts = datetime.now().strftime("%H:%M:%S")
                tyres = format_tyre_string(state.tyres_surf)
                print(
                    f"[{ts}] "
                    f"SPD={state.speed:>3d} km/h  GEAR={state.gear:>2d}  RPM={state.rpm:>5d}  "
                    f"THR={fmt(state.throttle)}  BRK={fmt(state.brake)}  STR={fmt(state.steer)}  "
                    f"DRS={'ON' if state.drs_active else 'OFF'}  ALW={'Y' if state.drs_allowed else 'N'}  "
                    f"ERS={fmt(state.ers_j, ' J')}  Fuel≈{fmt(state.fuel_laps, ' laps')}  "
                    f"Tyres FL/FR/RL/RR={tyres}"
                )
                last_print = now

    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        sock.close()
