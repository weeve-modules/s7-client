from weeve_modules import send, add_graceful_termination, weeve_logger
import asyncio
import snap7
from os import getenv

log = weeve_logger("main")


async def module_main(configuration):
    """
    Implements module's main logic for inputting data.
    Function description should not be modified.
    """

    logo_client = snap7.logo.Logo()
    logo_client.connect(
        configuration["LOGO_IP"],
        configuration["LOCAL_TSAP"],
        configuration["REMOTE_TSAP"],
        configuration["PORT"],
    )

    vm_addrs = [
        vm_addr.strip() for vm_addr in configuration["VM_ADDR"].strip(",").split(",")
    ]

    while True:
        if logo_client.get_connected():
            body = {}
            for vm_addr in vm_addrs:
                body[vm_addr] = int(logo_client.read(vm_addr))

            send_error = send(body)

            if send_error:
                log.error(send_error)
            else:
                log.debug("Data sent sucessfully.")
        else:
            log.error("not connected")

        if configuration["POLL_INTERVAL"] <= 0:
            break

        await asyncio.sleep(configuration["POLL_INTERVAL"])


async def main():
    log.info(
        "%s running with end-point set to %s",
        getenv("MODULE_NAME"),
        getenv("EGRESS_URLS"),
    )
    configuration = {
        "LOGO_IP": getenv("LOGO_IP"),
        "LOCAL_TSAP": int(getenv("LOCAL_TSAP", "0x3000"), 16),
        "REMOTE_TSAP": int(getenv("REMOTE_TSAP", "0x2000"), 16),
        "PORT": int(getenv("PORT", "102")),
        "VM_ADDR": getenv("VM_ADDR"),
        "POLL_INTERVAL": int(getenv("POLL_INTERVAL", "5")),
    }

    print(configuration)

    await module_main(configuration)


if __name__ == "__main__":
    add_graceful_termination()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
