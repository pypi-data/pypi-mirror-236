import time

from .board_conf import Strawberry
from .constants import DEFAULT, PA_DAC, REG
from .my_types import IRQ, MODE, ModemConfig


class LoRa(object):
    # ID del dispositivo
    _device_id: bytes

    # Frequency of Transmission
    _frequency: float

    # TX Power (Potenza di Trasmissione): rappresenta la quantità di potenza RF (radiofrequenza) utilizzata dal dispositivo
    # per inviare un segnale, espressa in dBm (decibel-milliwatt)
    #     - Potenza massima 23 dBm
    #     - Potenza minima   5 dBm
    _tx_power: int

    # Mode:
    #   - É la modalità di inizio, utilizzata per salvare la modalità quando si effettuano più operazioni
    #   -  É la modalità CURRENT
    _initial_mode: int | None = None
    _current_mode: int | None = None

    # -------------------------------------------------------------------------------------------- #
    def __init__(
        self,
        device_id: str,
        frequency: float = DEFAULT.FREQUENCY,
        tx_power: int = DEFAULT.TX_POWER,
        modem_config: ModemConfig = DEFAULT.MODEM_CONFIG,
    ):
        # --- Convert Device ID to Hash --- #
        self._device_id = hash(device_id).to_bytes(
            length=8, byteorder="little", signed=True
        )

        # --- SPI --- #
        Strawberry.SpiDev()  # Open Serial Peripheral
        Strawberry.Setup()  # Setup all GPIO
        Strawberry.AddEvents(
            callback_dio0=self._handle_interrupt_dio0,
            callback_dio1=self._handle_interrupt_dioX,
            callback_dio2=self._handle_interrupt_dioX,
            callback_dio3=self._handle_interrupt_dioX,
        )

        # --- Settings --- #
        self.check_module()  # Check if module LoRa is connected
        self.set_mode(MODE.SLEEP)  # For calibration
        # self.reset_fifo()  # Reset Fifo buffer
        self.set_modem_config(modem_config)  # Set Modem Config
        # self.set_preamble()  # Set Preamble
        self.set_frequency(frequency)  # Frequency
        self.set_tx_power(tx_power)  # Transmission Power
        self.set_mode(
            MODE.STANDBY
        )  # Module in Standby -> In questo modo sarà il Main a scegliere il da farsi

    # -------------------------------------------------------------------------------------------- #
    # --- Events --- #
    def on_receive(self, h_from: bytes, payload: bytes, rssi: float, snr: float):
        pass

    # -------------------------------------------------------------------------------------------- #
    # --- Module Function --- #
    def check_module(self):
        # Controllo se il modulo è stato correttamente collegato al microcontrollore
        #     Scrivo nel registro e quando rileggo mi devo aspettare lo stesso risultato
        Strawberry.Write(REG.OP_MODE, MODE.SLEEP)
        time.sleep(0.1)

        if Strawberry.Read(REG.OP_MODE) != MODE.SLEEP:
            raise ConnectionError("LoRa initialization failed!")

    def reset_fifo(self):
        # Imposto la posizione di base del buffer FIFO di trasmissione ('FIFO TX') e di ricezione ('FIFO RX) a 0
        # In questo modo i dati trasmessi/ricevuti verranno scritti/letti dall'inizio del Buffer
        Strawberry.Write(REG.FIFO_TX_BASE_ADDR, 0)
        Strawberry.Write(REG.FIFO_RX_BASE_ADDR, 0)

    def set_modem_config(self, modem_config: ModemConfig):
        # Modem Config: si riferisce alla configurazione del modem LoRa, responsabile della modulazione
        # e della demodulazione dei dati da trasmettere e ricevere su una rete LoRa.
        # La configurazione del modem è una serie di parametri:
        #     - Larghezza di banda (BW)
        #     - Fattore di spreading (SF)
        #     - Codice di correzione degli errori (CR)
        #     - Frequenza di trasmissione:
        #     - Potenza di trasmissione
        #     - Lunghezza del pacchetto
        #     - Tipo di modulazione
        Strawberry.Write(REG.MODEM_CONFIG_1, modem_config[0])
        Strawberry.Write(REG.MODEM_CONFIG_2, modem_config[1])
        Strawberry.Write(REG.MODEM_CONFIG_3, modem_config[2])

    def set_preamble(self):
        # Set Preamble: è una sequenza di bit inviata prima dei dati effettivi nella trasmissione ed è utilizzato per sincronizzare il ricevitore con il trasmettitore.
        # La configurazione del preambolo è importante perché aiuta il ricevitore a riconoscere l'inizio di una trasmissione e sincronizzarsi con il trasmettitore.
        Strawberry.Write(REG.PREAMBLE_MSB, 0)
        Strawberry.Write(REG.PREAMBLE_LSB, 8)
        pass

    def set_mode(self, mode: int):
        if self._current_mode == mode:
            return

        # Aggiorno il registro della modalità
        self._current_mode = mode
        Strawberry.Write(REG.OP_MODE, mode)

        # 1. Interrupt on RXDone: Se trasmetto imposto il dio0 per notificarmi dell'invio dei dati
        # 2. Interrupt on TxDone: Se ricevo imposto il dio0 per notificarmi che ci sta un nuovo messaggio da leggere
        Strawberry.Write(REG.DIO_MAPPING_1, 0x40 if mode == MODE.TX else 0x00)

    def set_frequency(self, frequency: float):
        # Set Frequency: a cui il dispositivo trasmette e riceve dati.
        self._frequency = frequency

        i = int(frequency * 16384.0)
        msb = i // 65536
        i -= msb * 65536
        mid = i // 256
        i -= mid * 256
        lsb = i
        Strawberry.Write(REG.FR_MSB, [msb, mid, lsb])

    def set_tx_power(self, tx_power: int):
        self._tx_power: int = max(min(tx_power, 23), 5)

        # Set TX Power:
        #     - in base alla potenza che si vorrà utilizzare per trasmettere i dati, si attiverà/disattiverà un amplificatore di potenza
        #     - imposto la potenza di trasmissione
        if self._tx_power < 20:
            Strawberry.Write(REG.PA_DAC, PA_DAC.ENABLE)
            self._tx_power -= 3
        else:
            Strawberry.Write(REG.PA_DAC, PA_DAC.DISABLE)

        Strawberry.Write(REG.PA_CONFIG, PA_DAC.SELECT | (self._tx_power - 5))

    # -------------------------------------------------------------------------------------------- #
    # --- Writer --- #
    def send(self, payload: list[int]):
        # Mi salvo la modalità, in questo modo appena ricevo il TxDone la rimetto
        self._initial_mode = self._current_mode

        # Size del messaggio
        payload_size = len(payload)
        Strawberry.Write(REG.PAYLOAD_LENGTH, payload_size)

        # Entro in modalità Standby, in questo modo mentre modifico il FIFO non ci sarà il rischio che il modulo si metta in mezzo
        self.set_mode(MODE.STANDBY)
        base_addr = Strawberry.Read(REG.FIFO_TX_BASE_ADDR)
        Strawberry.Write(REG.FIFO_ADDR_PTR, base_addr)
        Strawberry.Write(REG.FIFO, payload)

        # Quando c'è il passaggio dalla modalità di Standby alla modalità di TX (Trasmissione), il modulo trasmette i dati.
        # Infatti esso andrà a leggere dal fifo quello che abbiamo appena inserito
        self.set_mode(MODE.TX)

    # -------------------------------------------------------------------------------------------- #
    # --- Interrupts --- #
    # FIFO (First-In, First-Out): è un buffer dove vengono memorizzati temporaneamente i dati che devono essere
    # trasmetti o che sono stati ricevuti, in ordine FIFO.
    #
    # Questo buffer è diviso in due parti:
    #   - FIFO RX: per i dati che vengono ricevuti
    #   - FIFO TX: per i dati che vengono trasmessi
    #
    # Esso ha 3 puntatori, dove 1 è gestito da noi (FifoAddrPtr) e gli altri due sono gestiti dal modulo (RX Addr e TX Addr):
    #   - FifoAddrPtr (Fifo Address Pointer): punta nella locazione in cui vogliamo effettuare un'operazione di lettura/scrittura.
    #     Ogni volta che vorremmo leggere/scrivere nel FIFO dobbiamo puntare in quella locazione utilizzando questo registro.
    #
    #   - FIFO RX Addr: punta nella locazione di memoria dove sono stati appena ricevuti dei dati
    #   - FIFO TX Addr: punta nella locazione di memoria dove sono stati appena trasmessi dei dati
    #
    # Quando il puntatore raggiunge la fine della FIFO, spesso si "ricicla" all'inizio in modo circolare,
    # poiché la FIFO è una struttura dati circolare.
    #

    # DIO0 00: RxDone
    # DIO0 01: TxDone
    def _handle_interrupt_dio0(self, _: int):
        irq_flags = self.read_irq_flags()

        # DIO0 00: RxDone
        if self._current_mode == MODE.RX_CONTINUOUS and (irq_flags & IRQ.RxDone):
            self.clear_irq_flags(IRQ.RxDone)  # Clear RxDone Flag
            self._on_rx_done()

        # DIO0 01: TxDone
        elif self._current_mode == MODE.TX and (irq_flags & IRQ.TxDone):
            self.clear_irq_flags(IRQ.TxDone)  # Clear TxDone Flag
            self._on_tx_done()

    def _handle_interrupt_dioX(self, channel: int):
        print("Handle Interrupt:", channel)

    # -------------------------------------------------------------------------------------------- #
    # --- On ---- #

    # Messaggio:
    #   [0..7] to -> Il destinatario del messaggio
    #   [8..15] from -> Il mittente del messaggio
    #   [15:] payload -> Il messaggio

    def _on_rx_done(self):
        # Recupero la lunghezza del packet appena ricevuto
        packet_len = Strawberry.Read(REG.RX_NB_BYTES)

        # 1. Ottengo l'indirizzo del messaggio appena ricevuto
        # 2. Imposto il puntatore del FIFO a questo indirizzo, così potrò leggere
        fifo_rx_current_addr = Strawberry.Read(REG.FIFO_RX_CURR_ADDR)
        Strawberry.Write(
            REG.FIFO_ADDR_PTR, fifo_rx_current_addr
        )  # Recupero l'indirizzo dell'inizio packet

        # Recupero il packet dal FIFO
        packet = Strawberry.Reads(REG.FIFO, packet_len)

        # (Rapporto segnale-rumore, Potenza del segnale ricevuto)
        (snr, rssi) = self._get_signal_info()

        if packet_len >= 16:
            h_to = bytes(packet[0:7])
            h_from = bytes(packet[8:15])
            payload = bytes(packet[15:]) if packet_len > 16 else b""

            # Se non è un messaggio di Broadcasting e Io non sono il destinatario -> Ignoro il messaggio
            if h_to != DEFAULT.BROADCASTING and h_to != self._device_id:
                return

            # New Evento receive
            self.on_receive(h_from, payload, rssi, snr)

    def _on_tx_done(self):
        # Una volta che ho ricevuto la conferma che il packed che ho appena inserito nel FIFO è stato trasmetto, ritorno alla modalità iniziale (Prima del send)
        self.set_mode(
            self._initial_mode if self._initial_mode is not None else MODE.SLEEP
        )
        self._initial_mode = None

    # -------------------------------------------------------------------------------------------- #
    # --- Utils --- #
    def clear_irq_flags(self, flags: int):
        Strawberry.Write(REG.IRQ_FLAGS, flags)

    def read_irq_flags(self) -> int:
        return Strawberry.Read(REG.IRQ_FLAGS)

    def _get_signal_info(self) -> tuple[float, float]:
        # Rapporto segnale-rumore (SNR) espresso in db. Un valore SNR più alto indica una migliore qualità del segnale rispetto al rumore
        snr = Strawberry.Read(REG.PKT_SNR_VALUE) / 4
        # Potenza del segnale ricevuto (RSSI) espresso in dBm. Rappresenta la potenza del segnale ricevuto
        rssi = Strawberry.Read(REG.PKT_RSSI_VALUE)

        # Valori calcoli per correggere l'rssi a seconda di varie condizioni
        if snr < 0:
            rssi = snr + rssi
        else:
            rssi = rssi * 16 / 15
        if self._frequency >= 779:
            rssi = round(rssi - 157, 2)
        else:
            rssi = round(rssi - 164, 2)

        return (snr, rssi)

    def get_all_registers(self) -> list[int]:
        return [0] + Strawberry.Reads(0x00, 0x3E)[1:]
