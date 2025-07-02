import socketio
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

connected_event = asyncio.Event()

sio = socketio.AsyncClient(logger=True, engineio_logger=True)  # Enable logging for debugging

@sio.event
async def connect():
    logging.info('Verbindung zum Server als Sende-Client hergestellt.')
    connected_event.set()


@sio.event
async def disconnect():
    logging.info('Verbindung zum Server als Sende-Client getrennt.')


async def publish_finding(case_id: str, title: str, text: str):
    payload = {
        "case_id": case_id,
        "finding": {
            "title": title,
            "text": text
        }
    }
    await sio.emit('publish_to_case', payload)
    logging.info(f"Befund '{title}' an Fall '{case_id}' gesendet.")


async def main():
    try:
        await sio.connect('http://localhost:5000', wait_timeout=10)

        # Warte hier auf das Signal vom 'connect' Event-Handler...
        await connected_event.wait()

        logging.info("\nSende strukturierte Befunde blitzschnell...")

        await publish_finding(
            case_id="fall_123",
            title="Makroskopie",
            text="Ein 2,5 x 1,5 x 1,0 cm großes, bräunliches Gewebestück.\nSchnittfläche unauffällig."
        )

        await publish_finding(
            case_id="fall_456",
            title="Klinische Angaben",
            text="Zustand nach Resektion eines Adenokarzinoms."
        )

        await publish_finding(
            case_id="fall_123",  # Send another one to the first case
            title="Mikroskopie",
            text="Ausgedehnte Verbände von Plattenepithel ohne Atypien.\nKein Anhalt für Malignität."
        )

        logging.info("Test abgeschlossen.")

    except socketio.exceptions.ConnectionError as e:
        logging.error(f"Verbindung fehlgeschlagen: {e}")
    finally:
        # Give the last message time to send before disconnecting
        await asyncio.sleep(1)
        if sio.connected:
            await sio.disconnect()


if __name__ == '__main__':
    asyncio.run(main())