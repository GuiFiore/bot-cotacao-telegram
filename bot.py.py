import telebot
import requests

TOKEN = "SEU_TOKEN_AQUI"  # Substitua pelo seu token
bot = telebot.TeleBot(TOKEN)

def get_cotacao():
    try:
        url = "https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,BTC-BRL"
        response = requests.get(url)
        data = response.json()

        dolar = float(data["USDBRL"]["bid"])
        euro = float(data["EURBRL"]["bid"])
        bitcoin = float(data["BTCBRL"]["bid"])

        mensagem = (
            "💰 *Cotações em tempo real*\n\n"
            f"🇺🇸 Dólar:   R$ {dolar:.2f}\n"
            f"🇪🇺 Euro:    R$ {euro:.2f}\n"
            f"₿  Bitcoin: R$ {bitcoin:,.2f}\n\n"
            "_Fonte: AwesomeAPI • Atualizado agora_"
        )
        return mensagem

    except Exception as e:
        return "⚠️ Erro ao buscar cotações. Tente novamente."


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message,
        "👋 Olá! Eu sou o bot de cotações.\n\n"
        "Use os comandos abaixo:\n"
        "💵 /cotacao — Ver cotações agora\n"
        "ℹ️ /ajuda — Como usar o bot"
    )

@bot.message_handler(commands=["cotacao"])
def cotacao(message):
    bot.reply_to(message, "🔄 Buscando cotações...")
    resultado = get_cotacao()
    bot.reply_to(message, resultado, parse_mode="Markdown")

@bot.message_handler(commands=["ajuda"])
def ajuda(message):
    bot.reply_to(message,
        "ℹ️ *Como usar o bot:*\n\n"
        "/cotacao — Mostra dólar, euro e bitcoin\n"
        "/start — Reinicia o bot\n"
        "/ajuda — Mostra essa mensagem",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda msg: True)
def resposta_padrao(message):
    bot.reply_to(message,
        "Não entendi 😅 Use /cotacao para ver as cotações!"
    )

print("✅ Bot rodando...")
bot.infinity_polling()
