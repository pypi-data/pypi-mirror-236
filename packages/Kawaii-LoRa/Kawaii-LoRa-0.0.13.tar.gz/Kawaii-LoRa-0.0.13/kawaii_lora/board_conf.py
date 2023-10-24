import time

import RPi.GPIO as GPIO  # type: ignore
import spidev  # type: ignore

from .my_types import Board


# -------------------------------------------------------------------------------------------- #
# Strawberry #
# -------------------------------------------------------------------------------------------- #
class Strawberry:
    BOARD: Board | None = None

    @staticmethod
    def SetBoard(board: Board):
        Strawberry.BOARD = board

    # -------------------------------------------------------------------------------------------- #
    # --- SPI (Serial Peripheral Interface) for LoRa Module (SX1278) ---  #
    # Serve per aprire una connessione seriale (SPI) utilizzato per la comunicazione tra
    # dispositivi esterni (dispositivi come sensori, display e altre periferiche) e il microcontrollore:
    #     - Bus: Il primo argomento specifica il numero del BUS SPI  si desidera utilizzare
    #       In genere, Raspberry Pi ha due bus SPI (SPI0, quello principale e SPI1 quello secondario)
    #     - Channel: Il secondo argomento specifica i PIN da utilizzare per comunicare con il dispositivo:
    #        1. SPI0 (bus 0): È accessibile tramite i pin GPIO 9 (MISO), 10 (MOSI), 11 (SCLK), 8 (CE0), e 7 (CE1).
    #        2. SPI1 (bus 1): È accessibile tramite i pin GPIO 19 (MISO), 20 (MOSI), 21 (SCLK), 18 (CE0), e 17 (CE1).
    SPI: object = None

    @staticmethod
    def SpiDev(dev: tuple[int, int] = (0, 0)):  # (bus, channel)
        # --- SpiDev --- #
        Strawberry.SPI = spidev.SpiDev()  # type: ignore
        Strawberry.SPI.open(dev[0], dev[1])  # type: ignore
        Strawberry.SPI.max_speed_hz = 5000000

    # -------------------------------------------------------------------------------------------- #
    @staticmethod
    def Setup():
        # Controllo l'Injection della Board
        if Strawberry.BOARD is None:
            raise ValueError("Selezionare la Board su cui si sta lavorando.")

        # --- GPIO --- #
        GPIO.setmode(GPIO.BCM)  # type: ignore -> Così posso utilizzare i numeri

        # Setup di tutti i pin dio
        board: Board = Strawberry.BOARD
        for pin in [board.dio0, board.dio1, board.dio2, board.dio3]:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # type: ignore

    # -------------------------------------------------------------------------------------------- #
    @staticmethod
    def AddEvents(
        callback_dio0: object,
        callback_dio1: object,
        callback_dio2: object,
        callback_dio3: object,
    ):
        # Controllo l'Injection della Board
        if Strawberry.BOARD is None:
            raise ValueError("Selezionare la Board su cui si sta lavorando.")
        board: Board = Strawberry.BOARD

        # Aggiungo tutti gli eventi da detectare
        GPIO.add_event_detect(board.dio0, GPIO.RISING, callback=callback_dio0)  # type: ignore
        GPIO.add_event_detect(board.dio1, GPIO.RISING, callback=callback_dio1)  # type: ignore
        GPIO.add_event_detect(board.dio2, GPIO.RISING, callback=callback_dio2)  # type: ignore
        GPIO.add_event_detect(board.dio3, GPIO.RISING, callback=callback_dio3)  # type: ignore

    @staticmethod
    def Reset():
        # Controllo -> None l'Injection della Board
        if Strawberry.BOARD is None:
            raise ValueError("Selezionare la Board su cui si sta lavorando.")
        board: Board = Strawberry.BOARD

        GPIO.setmode(GPIO.BCM)  # type: ignore -> Così posso utilizzare i numeri

        # Reset del modulo
        try:
            GPIO.setup(board.reset, GPIO.OUT)  # type: ignore -> Set Pin in OUTPUT mode
            GPIO.output(board.reset, GPIO.LOW)  # type: ignore -> Send low

            time.sleep(0.01)
            GPIO.output(board.reset, GPIO.HIGH)  # type: ignore -> Send High
            time.sleep(0.01)
        finally:
            GPIO.cleanup(board.reset)  # type: ignore

    # -------------------------------------------------------------------------------------------- #
    @staticmethod
    def Write(reg: int, value: int | bytes | str | list[int]):
        # Converto il value in un Array
        payload: list[int]
        if isinstance(value, int):
            payload = [value]
        elif isinstance(value, bytes):
            payload = [b for b in value]
        elif isinstance(value, str):
            payload = [ord(s) for s in value]
        else:
            payload = value

        Strawberry.SPI.xfer([reg | 0x80] + payload)  # type: ignore

    @staticmethod
    def Read(reg: int) -> int:
        return Strawberry.SPI.xfer([reg] + [0])[1]  # type: ignore

    @staticmethod
    def Reads(reg: int, length: int) -> list[int]:
        return Strawberry.SPI.xfer([reg] + [0] * length)[1:]  # type: ignore
