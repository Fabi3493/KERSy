
# F1 25 (UDP format 2025) constants and offsets

# Networking
UDP_IP = "0.0.0.0"
UDP_PORT = 20777
SOCKET_TIMEOUT = 2.0

# Packet header (packed, little-endian)
HEADER_LEN = 29            # bytes
PACKET_ID_OFFSET = 6       # uint8
PLAYER_INDEX_OFFSET = 27   # uint8
MAX_CARS = 22

# Packet IDs
ID_CAR_TELEMETRY = 6
ID_CAR_STATUS    = 7

# Car Telemetry packet (per-car block)
CAR_TEL_BLOCK = 60  # bytes
# Offsets within a car telemetry block
TEL_SPEED_U16      = 0     # uint16 km/h
TEL_THROTTLE_F32   = 2     # float32
TEL_STEER_F32      = 6     # float32
TEL_BRAKE_F32      = 10    # float32
TEL_GEAR_I8        = 15    # int8
TEL_RPM_U16        = 16    # uint16
TEL_DRS_U8         = 18    # uint8 (0/1)
TEL_TYRES_SURF_ARR = 30    # 4x uint8 (order: RL, RR, FL, FR)

# Car Status packet (per-car block) — only needed offsets
CAR_STA_BLOCK      = 55    # ~55 bytes
STA_FUEL_LAPS_F32  = 13    # float32
STA_DRS_ALLOWED_U8 = 23    # uint8 (0/1)
STA_ERS_J_F32      = 41    # float32

# Printing / UI
PRINT_PERIOD = 1.0  # seconds
