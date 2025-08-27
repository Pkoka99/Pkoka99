from telethon import TelegramClient
import asyncio

# isi dengan data dari my.telegram.org
api_id = 29423686
api_hash = "0b7a35bc4270626060375248e6c69618"

async def main():
    async with TelegramClient("session", api_id, api_hash) as client:
        # contoh search group publik
        result = await client(functions.contacts.SearchRequest(
            q="toko",   # kata kunci group
            limit=10
        ))

        for chat in result.chats:
            print(f"Nama: {chat.title} | ID: {chat.id}")

            # cek history pesan pertama (untuk kira2 tahun dibuat)
            messages = await client.get_messages(chat.id, limit=1, offset_id=1, reverse=True)
            if messages:
                first_msg = messages[0]
                year = first_msg.date.year
                if 2022 <= year <= 2024:
                    print(f"✅ Group ini dibuat sekitar {year}")

asyncio.run(main())
