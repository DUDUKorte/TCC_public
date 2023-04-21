#<<<<<<< HEAD
from telegram import *
from telegram.ext import *
import asyncio
import json
import logging
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

import addfaces as RF

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

#===========================================================================

async def start(update: Update, context:ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(chat_id=update.effective_chat.id, text = f'Olá, seja bem-vindo ao bot do TCC de reconhecimento facial do Eduardo e Rodrigo do 3º de INFO\nSe quiser enviar uma imagem para os testes de reconhecimento facial basta enviar a foto\n\nPor favor, envie uma imagem nítida do rosto, sem acessórios, cabelo por trás da orelha e um fundo com poucas, ou nenhuma, pessoa.\nAgradecemos pela colaboração e pela ajuda\n\n(Enviando uma foto, você automaticamente concorda com os direitos de uso de sua imagem apenas para fins de testes)')

async def save_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    username = update.effective_user.username

    photo_file = await update.message.photo[-1].get_file()

    await photo_file.download_to_drive('./trainingImages/'+username+'_photo.jpg')

    logger.info("Photo of %s: %s", user.first_name, username+"_photo.jpg")

    await update.message.reply_text("Muito Obrigado por nos ajudar, cada foto que você envia nos ajuda cada vez mais no nosso desenvolvimento")

    RF.addFace(username, "./trainingImages/"+username+'_photo.jpg')

if __name__ == '__main__':

    #pega o token no txt
    token = open('./ComunityHelp/token.txt')
    token = token.read()

    #inicializa bot
    application = ApplicationBuilder().token(token).build()

    #chama as funções por comandos
    application.add_handler(CommandHandler("start", start))

    application.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, save_photo))


    #reinicia o bot
    application.run_polling()
#=======
