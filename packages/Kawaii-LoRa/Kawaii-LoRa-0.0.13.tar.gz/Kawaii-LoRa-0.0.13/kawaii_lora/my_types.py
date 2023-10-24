# -------------------------------------------------------------------------------------------- #
# Boards #
# -------------------------------------------------------------------------------------------- #
class Board:
    # --- Name of StrawBerry --- #
    name: str

    # --- Pins --- #
    dio0: int  # Rx Done (Receiver)
    dio1: int  # Tx Done (Transmitter)
    dio2: int  # FHSS (Frequency Hopping Spread Spectrum)
    dio3: int  # CAD Done (Channel Activity Detection done)
    reset: int  # Reset module

    def __init__(
        self, name: str, dio0: int, dio1: int, dio2: int, dio3: int, reset: int
    ):
        self.name = name
        self.dio0 = dio0
        self.dio1 = dio1
        self.dio2 = dio2
        self.dio3 = dio3
        self.reset = reset


class Boards:
    MODEL_B = Board(
        name="Raspberry PI model B", dio0=4, dio1=17, dio2=18, dio3=27, reset=22
    )
    PICO_W = Board(
        name="Raspberry PI Pico W", dio0=7, dio1=10, dio2=18, dio3=27, reset=9
    )


# -------------------------------------------------------------------------------------------- #
# --- Modem Config --- #
# -------------------------------------------------------------------------------------------- #
ModemConfig = tuple[int, int, int]


class ModemConfigs:
    Bw125Cr45Sf128: ModemConfig = (0x72, 0x74, 0x04)
    Bw500Cr45Sf128: ModemConfig = (0x92, 0x74, 0x04)
    Bw31_25Cr48Sf512: ModemConfig = (0x48, 0x94, 0x04)
    Bw125Cr48Sf4096: ModemConfig = (0x78, 0xC4, 0x0C)


# -------------------------------------------------------------------------------------------- #
# LoRa Modes #
# -------------------------------------------------------------------------------------------- #
class MODE:
    SLEEP = 0x80
    # In questa modalità il modulo non fa nulla, questo è molto utile quando bisogna lavorare sui buffer, tipo FIFO
    STANDBY = 0x81

    # Ricezione continua -> Continuo a ricevere fino a quando non cambierò MODE
    RX_CONTINUOUS = 0x85
    # Ricezione singola -> Ricevo una singola volta per poi tornare nello stato STANDBY (Tutto questo in automatico)
    RX_SINGLE = 0x86

    # Modalità di Invio: TX | LONG_RANGE
    TX = 0x83


# -------------------------------------------------------------------------------------------- #
# LoRa IRF (Interrupt Request Flags) #
# -------------------------------------------------------------------------------------------- #
class IRQ:
    CadDetected = 1
    FhssChangeChannel = 2
    CadDone = 4
    TxDone = 8
    ValidHeader = 16
    PayloadCrcError = 32
    RxDone = 64
    RxTimeout = 128
