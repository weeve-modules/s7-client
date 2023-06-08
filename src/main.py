from weeve_modules import send, add_graceful_termination, weeve_logger
import asyncio
import snap7
from os import getenv

log = weeve_logger("main")

DEFAULTS = {
    "LOCAL_TSAP": "0x3000",
    "REMOTE_TSAP": "0x2000",
    "PORT": "102",
    "POLL_INTERVAL": "5",
}

CONFIG = {
    "LOGO_IP": getenv("LOGO_IP"),
    "LOCAL_TSAP": int(getenv("LOCAL_TSAP", DEFAULTS["LOCAL_TSAP"]), 16),
    "REMOTE_TSAP": int(getenv("REMOTE_TSAP", DEFAULTS["REMOTE_TSAP"]), 16),
    "PORT": int(getenv("PORT", DEFAULTS["PORT"])),
    "VM_ADDR": getenv("VM_ADDR"),
    "POLL_INTERVAL": int(getenv("POLL_INTERVAL", DEFAULTS["POLL_INTERVAL"])),
}

vm_addrs = [vm_addr.strip() for vm_addr in CONFIG["VM_ADDR"].strip(",").split(",")]


async def read_and_send(logo_client):
    body = {}
    for vm_addr in vm_addrs:
        body[vm_addr] = int(logo_client.read(vm_addr))

    send_error = send(body)

    if send_error:
        log.error(send_error)
    else:
        log.debug("Data sent sucessfully.")


async def main():
    """
    Implements module's main logic for inputting data.
    Function description should not be modified.
    """

    log.info(
        "%s running with end-point set to %s",
        getenv("MODULE_NAME"),
        getenv("EGRESS_URLS"),
    )

    logo_client = snap7.logo.Logo()

    log.info(
        "Connecting to LOGO! at %s:%d Local TSAP: %s, Remote TSAP: %s",
        CONFIG["LOGO_IP"],
        CONFIG["PORT"],
        hex(CONFIG["LOCAL_TSAP"]),
        hex(CONFIG["REMOTE_TSAP"]),
    )
    err_code = logo_client.connect(
        CONFIG["LOGO_IP"],
        CONFIG["LOCAL_TSAP"],
        CONFIG["REMOTE_TSAP"],
        CONFIG["PORT"],
    )
    if err_code != 0:
        log.error("Could not connect to LOGO! Error code: %d", err_code)
        return

    if CONFIG["POLL_INTERVAL"] > 0:
        while logo_client.get_connected():
            await asyncio.gather(
                read_and_send(logo_client),
                asyncio.sleep(CONFIG["POLL_INTERVAL"])
            )
        else:
            log.error("Got disconnected from LOGO!")
            return
    else:  # Polling once
        if logo_client.get_connected():
            await read_and_send(logo_client)
            while True:  # Wait for graceful termination
                await asyncio.sleep(1)
        else:
            log.error("Got disconnected from LOGO!")
            return


if __name__ == "__main__":
    add_graceful_termination()

    asyncio.run(main())
    exit(1)  # Should never reach this line unless an error occurs
