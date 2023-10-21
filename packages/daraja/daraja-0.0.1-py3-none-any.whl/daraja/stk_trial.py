from mpesa import Mpesa
import asyncio

billing_number = "254748467252"
amount = 3

async def pay():
    mpesa = Mpesa(config_file="config.json", env="prod")
    res = await mpesa.stk(billing_number, amount)
    print(res)

asyncio.run(pay())
