import os
import discord
import logging

listpath = os.path.join(os.path.dirname(__file__), 'list.txt')
with open(listpath, 'r', encoding='utf-8') as f:
	words = f.readline().strip().split(',')

tokenpath = os.path.join(os.path.dirname(__file__), 'token.txt')
with open(tokenpath, 'r') as f:
	token = f.readline().strip()

logpath = os.path.join(os.path.dirname(__file__), 'log.txt')
logging.basicConfig(filename=logpath, level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', encoding='utf-8')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print('起動しました')

@client.event
async def on_message(message):
	for word in words:
		if word in message.content:
			await message.delete()
			logging.info(f"メッセージを削除しました: {message.content}")
			break

@client.event
async def on_member_update(before, after):
	for word in words:
		if after.nick is not None and word in after.nick:
			try:
				await after.edit(nick=None)
				logging.info(f"ニックネームを解除しました: {after}")
			except discord.Forbidden:
				logging.info(f"権限不足でニックネームを解除できませんでした: {after}")
			except discord.HTTPException as e:
				logging.info(f"エラー: {e}")

client.run(token)