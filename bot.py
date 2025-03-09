from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CallbackQueryHandler, filters
import logging
import requests
from googletrans import Translator

# Configuração de logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Insira o token do seu bot aqui
TOKEN = '[REDACTED_SECRET]'

# Chave da API de geolocalização (substitua pela sua chave)
IPINFO_TOKEN = '[REDACTED_SECRET]'

# Função para obter a localização via IP
def get_location_by_ip(ip):
    url = f"https://ipinfo.io/{ip}?token={IPINFO_TOKEN}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('country')  # Retorna o código do país (ex: 'BR' para Brasil)
    return None

# Função para traduzir a mensagem
def translate_message(text, dest_language):
    translator = Translator()
    translation = translator.translate(text, dest=dest_language)
    return translation.text

# Função para obter a bandeira do país
def get_country_flag(country_code):
    # Converte código do país (ex: 'BR') em emoji de bandeira
    base = ord('🇦') - ord('A')  # Offset para emojis de bandeiras
    return ''.join(chr(base + ord(char)) for char in country_code.upper())

# Função para enviar mensagem de boas-vindas
async def welcome(update: Update, context):
    logger.info(f"Novo membro detectado: {update.message.new_chat_members}")
    if update.message.new_chat_members:
        for member in update.message.new_chat_members:
            user_ip = update.message.from_user.id  # Aproximação, não é IP real
            country_code = get_location_by_ip(user_ip)
            if country_code:
                if country_code == 'BR':
                    language = 'pt'
                elif country_code == 'US':
                    language = 'en'
                elif country_code == 'ES':
                    language = 'es'
                else:
                    language = 'en'
                welcome_message = translate_message("Welcome to our official VKINHA community!", language)
                warning_message = translate_message("⚡️⚡️MAKE SURE YOU ARE ON OUR OFFICIAL WEBSITE VKINHA⚡️⚡️", language)
                admin_message = translate_message("‼️‼️ ADMIN DONT PM YOU OR ASK FOR FUNDS ‼️‼️", language)
                location_message = translate_message("Sua localização é:", language)
                flag = get_country_flag(country_code)
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"{welcome_message}\n\n{warning_message}\n\n{admin_message}\n\n{location_message} {flag}"
                )
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Welcome to our official VKINHA community!\n\n⚡️⚡️MAKE SURE YOU ARE ON OUR OFFICIAL WEBSITE VKINHA⚡️⚡️\n\n‼️‼️ ADMIN DONT PM YOU OR ASK FOR FUNDS ‼️‼️"
                )

            keyboard = [
                [InlineKeyboardButton("Contract", url="https://bscscan.com/token/0x7Bd2024cAd405ccA960fE9989334A70153c41682")],
                [InlineKeyboardButton("Pre-Sale", callback_data='pre_sale')],
                [InlineKeyboardButton("Site", url="https://www.vkinha.com.br")],
                [InlineKeyboardButton("Instagram", url="https://www.instagram.com/vkinhacoin/")],
                [InlineKeyboardButton("X", url="https://x.com/vkinhacoin")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Escolha uma opção:",
                reply_markup=reply_markup
            )

# Função para lidar com os botões
async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    if query.data == 'pre_sale':
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Pre-sale prevista para começar na dxsale no dia 30/03/2025"
        )

def main():
    logger.info("Iniciando o bot...")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    application.add_handler(CallbackQueryHandler(button_handler))
    logger.info("Bot está rodando...")
    application.run_polling()

if __name__ == '__main__':
    main()