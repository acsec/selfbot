import discord, asyncio, sys, re, base64

client = discord.Client()
token = input("Token: ")
global REACT
REACT = False

if token.startswith('\"'):
	token = token.strip('\"')	

def resolve(string):
	byte_string = string.encode('utf-8')
	encoded_string = base64.b64encode(byte_string)
	final_string = encoded_string.decode('utf-8')
	return final_string

async def on_ready():
	print("Logged in as: {0} ({0.id})".format(client.user))
	
async def on_message(message):
	if message.author == client.user.id:
		if message.startswith('.D'):
			if re.search(r'\d+$', message) != None:
				x = message.strip('.D ')
			else:
				x = 9999
			async for m in client.logs_from(message.channel, limit=x):
				await client.delete_message(m)
		if message.startswith('.B'):
			u = message.strip('.B ')
			if len(u) == 18:
				token_string = "<@{0}>'s token: ```{1}.******.***************************```".format(u, resolve(u))
				await client.send_message(token_string, message.channel)
			else:
				await client.send_message("```Incorrect Usage: .B [userID]```", message.channel)
		if message.startswith('.T'):
			u = message.strip('.T ')
			if len(u) == 18:
				await client.send_message("```Typing to <@{0}>```".format(get_user(u)))	
				await client.send_typing(u)
			else:
				await client.send_message("```Incorrect Usage: .T [userID]```", message.channel)
		if message.startswith('.R'):
			REACTIONS = {}
			if message.startswith('.R add'):
				try:
					c, a, u, e = message.split()
					d[u] = e
				except:
					await client.send_message("```Incorrect Usage: .R add [userID] [emoji]```", message.channel)
			if message.startswith('.R rem'):
				c, r, u = message.split()
				if u in REACTIONS:
					REACTIONS.pop(u)
				else:
					await client.send_message("```Incorrect Usage: .R rem [userID]```", message.channel)
			if REACT == False:
				REACT = True
			elif REACT == True:
				REACT = False
			else:
				await client.send_message("```Incorrect Usage: .R```", message.channel)
		if message.content == '.X':
			print("\nExit\n")
			sys.exit(1)
		while REACT == True:
			for k, v in REACTIONS:
				if message.author.id == k:
					emoji = get(client.get_all_emojis(), name=v.strip(':'))
					await client.add_reaction(message, emoji)
		
client.run(token, bot=False)