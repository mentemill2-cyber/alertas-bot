import requests
import asyncio
from telegram import Bot

TOKEN = "8660205091:AAEmp1p96xmURqgcd38qRbQME4wKcjVvz5I"
CHAT_ID = "1537440859"

ALERTAS = [
    ("BTC",     55777,    81000),
    ("ETH",      1427,     4000),
    ("HYPE",   56.277,   58.447),
    ("LITE",      832.27,      862.27),
    ("SNDK",   1647.2,   1887.2),
    ("HYUNDAI", 367.16,  414.47),
    ("SAMSUNG", 191.46,     240.14),
    ("OPENAI",    1232.2,     1327),
    ("WTIOIL",      82.27,   92.277),
    ("ANTHROPIC", 1466.8,  2000),
    ("LLY",      1075.2,   1500),
    ("SOY",        1037,   1500),
    ("CBRS",        207.27,    300),
    ("CRCL",      74.712,  89.477),
]
INTERVALO = 60
alertas_enviadas = {}

def obtener_precios():
    try:
        r = requests.post("https://api.hyperliquid.xyz/info", json={"type": "allMids"}, timeout=10)
        return r.json()
    except Exception as e:
        print(f"Error: {e}")
        return {}

async def enviar_mensaje(bot, mensaje):
    await bot.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode="HTML")

async def revisar_alertas(bot):
    precios = obtener_precios()
    for moneda, minimo, maximo in ALERTAS:
        if moneda not in precios:
            continue
        precio = float(precios[moneda])
        if minimo > 0 and precio <= minimo and not alertas_enviadas.get(moneda+"_min"):
            await enviar_mensaje(bot, f"🔴 <b>{moneda}</b>: ${precio:,.2f} bajo del minimo ${minimo:,.2f}")
            alertas_enviadas[moneda+"_min"] = True
        elif precio > minimo:
            alertas_enviadas[moneda+"_min"] = False
        if maximo < 9999999 and precio >= maximo and not alertas_enviadas.get(moneda+"_max"):
            await enviar_mensaje(bot, f"🟢 <b>{moneda}</b>: ${precio:,.2f} supero el maximo ${maximo:,.2f}")
            alertas_enviadas[moneda+"_max"] = True
        elif precio < maximo:
            alertas_enviadas[moneda+"_max"] = False

async def main():
    bot = Bot(token=TOKEN)
    await enviar_mensaje(bot, "✅ <b>Bot de alertas iniciado</b>")
    print("Bot iniciado.")
    while True:
        print("Revisando precios...")
        await revisar_alertas(bot)
        await asyncio.sleep(INTERVALO)

if __name__ == "__main__":
    asyncio.run(main())
