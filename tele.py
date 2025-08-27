from telethon import TelegramClient, functions, types
import asyncio

# Ganti dengan API ID dan API HASH kamu dari my.telegram.org
api_id = 29423686
api_hash = "0b7a35bc4270626060375248e6c69618"

# Nama session (file login akan tersimpan dengan nama ini)
client = TelegramClient("session_findgroup", api_id, api_hash)


async def main():
    # Contoh cari group publik pakai keyword
    # Bisa diganti misalnya "2022", "2023", "2024"
    keywords = ["2022", "2023", "2024"]

    for kw in keywords:
        print(f"\n🔎 Searching groups with keyword: {kw}")
        result = await client(functions.contacts.SearchRequest(
            q=kw,
            limit=10
        ))

        if result.chats:
            for chat in result.chats:
                print(f"📌 Found: {chat.title} | ID: {chat.id} | Username: {chat.username}")
        else:
            print("❌ No groups found for", kw)


with client:
    client.loop.run_until_complete(main())
