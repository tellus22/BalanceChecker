from Blockchain.Extractor import extract_crypto_addresses
from aiogram import types
from aiogram.types import ContentType
from loader import dp, bot


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer("Отправь файл с расширением .txt", parse_mode='HTML')


@dp.message_handler(content_types=ContentType.DOCUMENT)
async def handle_text_file(message: types.Message):
    if message.document.file_name.endswith('.txt'):

        file = await bot.get_file(message.document.file_id)
        file_path = file.file_path
        file_name = message.document.file_name
        downloaded_file = await bot.download_file(file_path, f'./Addresses/{file_name}')
        downloaded_file_name = f'./Addresses/{file_name}'

        await message.answer("Ща погодь минутку")
        print(f"Файл успешно сохранен как {message.document.file_name}")
    else:
        await message.answer("Отправь файл с расширением .txt")

    input_files = [downloaded_file_name]
    output_file = "output_addresses.txt"
    extract_crypto_addresses(input_files, output_file)

    doc = open(('output_addresses') + '.txt', 'rb')
    await message.reply_document(doc)
    print("Keep Pushin")
