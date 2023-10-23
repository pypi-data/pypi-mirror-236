import asyncio
import sys
import argparse

from . import SmartOilGaugeClient

# create parser for arguments
parser = argparse.ArgumentParser(
    usage="python -m aiosmartoilgauge clientid clientsecret"
)
parser.add_argument("clientid", help="account client id")
parser.add_argument("clientsecret", help="account client secret")

# if no arguments specified, show help
if len(sys.argv) < 3:
    parser.print_help()
    sys.exit(1)

# parse for arguments
args = parser.parse_args()


async def run_async():
    client = SmartOilGaugeClient(args.clientid, args.clientsecret)
    await client.async_login()

    accounts = await client.async_get_tank_data()

    for account in accounts:
        print(account.sensor_ids)


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(run_async())
loop.close()
