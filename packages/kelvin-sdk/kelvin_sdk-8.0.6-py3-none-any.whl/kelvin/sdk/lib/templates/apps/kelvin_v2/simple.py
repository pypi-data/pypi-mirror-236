import asyncio

from kelvin.app.client import KelvinApp


async def main() -> None:
    # Creating instance of Kelvin App Client
    app = KelvinApp()

    # Connect the App Client
    await app.connect()

    while True:
        # Custom Loop
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
