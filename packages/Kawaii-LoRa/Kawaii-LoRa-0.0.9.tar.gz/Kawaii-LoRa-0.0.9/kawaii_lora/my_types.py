from dataclasses import dataclass
from enum import Enum, Flag


# -------------------------------------------------------------------------------------------- #
# Boards #
# -------------------------------------------------------------------------------------------- #
@dataclass
class Board:
    # --- Name of StrawBerry --- #
    name: str

    # --- Pins --- #
    dio0: int  # Rx Done (Receiver)
    dio1: int  # Tx Done (Transmitter)
    dio2: int  # FHSS (Frequency Hopping Spread Spectrum)
    dio3: int  # CAD Done (Channel Activity Detection done)
    reset: int  # Reset module


class Boards(Enum):
    MODEL_B = Board(
        name="Raspberry PI model B", dio0=4, dio1=17, dio2=18, dio3=27, reset=22
    )
    # TODO : CAMBIARE I DIO
    PICO_W = Board(
        name="Raspberry PI Pico W", dio0=4, dio1=17, dio2=18, dio3=27, reset=22
    )


# -------------------------------------------------------------------------------------------- #
# --- Modem Config --- #
# -------------------------------------------------------------------------------------------- #
class ModemConfig(Enum):
    Bw125Cr45Sf128 = (0x72, 0x74, 0x04)
    Bw500Cr45Sf128 = (0x92, 0x74, 0x04)
    Bw31_25Cr48Sf512 = (0x48, 0x94, 0x04)
    Bw125Cr48Sf4096 = (0x78, 0xC4, 0x0C)


# -------------------------------------------------------------------------------------------- #
# LoRa Modes #
# -------------------------------------------------------------------------------------------- #
class MODE(Flag):
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
class IRQ(Flag):
    CadDetected = 1
    FhssChangeChannel = 2
    CadDone = 4
    TxDone = 8
    ValidHeader = 16
    PayloadCrcError = 32
    RxDone = 64
    RxTimeout = 128
