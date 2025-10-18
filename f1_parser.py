
import struct
from typing import Optional, Tuple, Dict, Any, List
import f1_constants as C

def parse_header(data: bytes) -> Optional[Tuple[int, int]]:
    """Return (packet_id, player_index) or None if too short."""
    if len(data) < C.HEADER_LEN:
        return None
    packet_id = data[C.PACKET_ID_OFFSET]
    player_idx = data[C.PLAYER_INDEX_OFFSET]
    if player_idx >= C.MAX_CARS:
        return None
    return packet_id, player_idx

def parse_car_telemetry(data: bytes, player_idx: int) -> Optional[Dict[str, Any]]:
    """Extract key telemetry fields for the player's car from a Car Telemetry packet (ID 6)."""
    base = C.HEADER_LEN + C.CAR_TEL_BLOCK * player_idx
    end  = base + C.CAR_TEL_BLOCK
    if len(data) < end:
        return None

    speed    = struct.unpack_from("<H", data, base + C.TEL_SPEED_U16)[0]
    throttle = struct.unpack_from("<f", data, base + C.TEL_THROTTLE_F32)[0]
    steer    = struct.unpack_from("<f", data, base + C.TEL_STEER_F32)[0]
    brake    = struct.unpack_from("<f", data, base + C.TEL_BRAKE_F32)[0]
    gear     = struct.unpack_from("<b", data, base + C.TEL_GEAR_I8)[0]
    rpm      = struct.unpack_from("<H", data, base + C.TEL_RPM_U16)[0]
    drs_act  = data[base + C.TEL_DRS_U8]
    tyres    = list(data[base + C.TEL_TYRES_SURF_ARR : base + C.TEL_TYRES_SURF_ARR + 4])  # RL, RR, FL, FR

    return {
        "speed": speed,
        "throttle": throttle,
        "steer": steer,
        "brake": brake,
        "gear": gear,
        "rpm": rpm,
        "drs_active": drs_act,
        "tyres_surf": tyres,   # RL, RR, FL, FR
    }

def parse_car_status(data: bytes, player_idx: int) -> Optional[Dict[str, Any]]:
    """Extract key status fields for the player's car from a Car Status packet (ID 7)."""
    base = C.HEADER_LEN + C.CAR_STA_BLOCK * player_idx
    end  = base + C.CAR_STA_BLOCK
    if len(data) < end:
        return None

    fuel_laps   = struct.unpack_from("<f", data, base + C.STA_FUEL_LAPS_F32)[0]
    drs_allowed = data[base + C.STA_DRS_ALLOWED_U8]
    ers_j       = struct.unpack_from("<f", data, base + C.STA_ERS_J_F32)[0]

    return {
        "fuel_laps": fuel_laps,
        "drs_allowed": drs_allowed,
        "ers_j": ers_j,
    }
