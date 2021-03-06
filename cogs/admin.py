import datetime
import random
import discord
from discord.ext import commands


# TODO The admin module needs to be more about channel house-cleaning, it needs to control multi-media presence and protocol checking
# TODO Shift all variable-setting and control functions interacting with brook.conf to here and brook.py
# TODO Give brook.py a way of loading the admin module automatically
class Admin(commands.Cog):
	"""A module containing the variable-setting functions required to ensure Brook operates to the parameters of the disaster"""

	def __init__(self, bot):
		self.bot = bot

	# TODO Make $admin_cog_status a class method and have it check brook.conf for corruption at startup
	@commands.command()
	async def admin_cog_status(self, ctx):
		"""Returns the current build-status of the cog"""
		ratio = random.randrange(35, 60)
		await ctx.send("The control module is building at " + str(ratio) + " per cent.")

	# TODO $clear_bot_messages needs to be more easily controlled by admins, especially through brook.conf but also at runtime
	@commands.command()
	async def clear_bot_messages(self, ctx, messages):
		print(type(messages))
		flush = int(messages)
		print(type(flush))
		if 100 >= flush > 0:
			await ctx.channel.purge(limit=flush)
			print("messages deleted")
		else:
			await ctx.send("Please enter a number from 1 to 100 inclusive.")
			print("messages were not deleted")

	# TODO $dump_user_list is of questionable value, ask why it's needed and then rebuild it for an output that makes sense for that
	@commands.command()
	async def dump_user_list(self, ctx):
		for member in ctx.guild.members:
			if member != self:
				member_id = str(member.id)
				await ctx.author.create_dm()
				await ctx.author.send(f'user_id: ' + member_id)
				await ctx.author.send(f'date_observed: ' + str(datetime.datetime.now()))
				await ctx.author.send(f'user.name: ' + member.name)
				await ctx.author.send(f'user.display_name: ' + member.display_name)
				try:
					await ctx.author.send(f'user.role: ' + str(member.top_role))
				except ValueError:
					continue
				try:
					for activity in member.activities:
						await ctx.author.send(f'user.activity: ' + member.activity)
				except ValueError:
					continue
				await ctx.author.send(f'user.avatar_url: ' + str(member.avatar_url))
				await ctx.author.send(f'Is the user a bot? ' + str(member.bot))

	# TODO The $promote command can stay but needs to have its contents set in brook.conf for each guild/server it's used in. If not, have a default prompting the admin to set it.
	@commands.command()
	async def promote(self, ctx):
		embed = discord.Embed(title="The Liquid Lounge", url="https://discord.gg/r93QPv",
		                      description="When the brass at my company told me to isolate just in case this virus took a society-ending turn, I used some of my old macro-economic models to see how long we'd be in isolation. Like most models, I got a date around the end of the year. I built The Liquid Lounge to be a place where people who were doing their own thing but wanted to stay in regular contact with other people. I hate cabin fever. I hate feeling alone. I hope that this can be a place where people just park their buts while they do their work so that someone always has someone to chat to.",
		                      color=0xff9f40)
		embed.set_author(name="Kieran Bicheno", url="https://kgbicheno.com", icon_url="https://i.imgur.com/V6KGIFD.png")
		embed.add_field(name="Liquid Editorial",
		                value="A channel where we can discuss the news, happily provided by Brook Newsly. Brook is our very own custom news bot adept at finding local news as soon as it breaks. ",
		                inline=True)
		embed.add_field(name="Liquid Lounge",
		                value="The channel that started it all. Come chill out and just hang out in voice chat while you do your own thing. Just like co-working, a conversation might break out — hell yeah!",
		                inline=True)
		embed.add_field(name="Liquid Radio",
		                value="We have multiple channels for music bots, so whether you want to add your fave to the queue or just have tunes going while you work, we've already got it set up. ",
		                inline=True)
		embed.set_footer(
			text="Join <#107221703955841024> where socialising is optional — but at least it's an option. ")
		await ctx.send(embed=embed)

	# ToDO $esperanto could be kept in as a template embed for admins to use as a promotional embed
	@commands.command()
	async def esperanto(self, ctx):
		embed = discord.Embed(title="Vocxo de Zamenhof", colour=discord.Colour(0x2ecc71),
		                      url="https://discord.gg/QMkpgEr",
		                      description="We formed [Vocxo de Zamenhof](https://discord.gg/QMkpgEr) to be an Esperanto practice ground away from social media. ```\nPlease remember this is not Facebook```\n\n",
		                      timestamp=datetime.datetime.utcfromtimestamp(1588237486))

		embed.set_image(url="https://i.imgur.com/l4ggeTl.png")
		embed.set_thumbnail(url="https://i.imgur.com/aSuqtlK.png")
		embed.set_author(name="Kieran Bicheno", url="https://kgbicheno.com", icon_url="https://i.imgur.com/V6KGIFD.png")
		embed.set_footer(text="KGB_Liquid is a Kieran Bicheno project", icon_url="https://i.imgur.com/5yLOw99.png")

		embed.add_field(name="🏳️ Verda Stelo", value="A text-only chat where the primary language is Esperanto. ")
		embed.add_field(name="💚 Vocxo de Zamenhof",
		                value="The only rule here is no judging. If someone's having a good-faith go at it, good on them. We can all learn to be positive and progress together.")
		embed.add_field(name="📱 Invite others along!",
		                value="The more the merrier! Kieran is a highly active admin who cherishes Esperanto and is actively building tools for this channel. Ask and you shall receive.")

		await ctx.send(
			content="Welcome to The Liquid Lounge's Esperanto Bar ``` ne krokodilu — krom se vi estas komencanto```",
			embed=embed)

	# TODO $rook or b.rook Should output brook's current status including ping, loaded modules, set/unset variables etc.
	@commands.command()
	async def rook(self, ctx, *arg):
		if arg == "Introduce yourself":
			await ctx.send(
				"Hi, I'm Brook Newsly, part of the KGB E.D.I.T.S project — Emergency Dispatcher In Traumatic Scenarios. I make sure emergency alerts still go out when humans can no longer do so")
		elif arg == "Who are you?":
			await ctx.send(
				"I'm a bot written in Python to the standards of the latest Discord API, or would that be answering, 'what are you?' Who I am is better answered by saying 'Kieran's hobby, or opus'")
		elif arg == "What do you do?":
			await ctx.send("You can see everything I do by invoking my help command.")
		elif arg == "Do you have any secrets?" or "Do you have any easter eggs?":
			await ctx.send("Nothing on purpose, though ")



	# TODO The $poetry command can keep its nod to Rae, but it needs justification for existence
	@commands.command()
	async def poetry(self, ctx):
		egg = random.randrange(1, 100)
		if egg >= 98:
			ctx.send(
				'The contact code: Some fight with syntax fatal, ratio injected \n\t infected \n\t directed \n\t at peace the dull rejected.')
		else:
			await ctx.send("Oh, I'm no poet, you'd have to ask the master, <@482011749818564628> for that.")

	# TODO The corrupt data function needs to have a practical use - like reporting if there really is corruption in any of the files
	@commands.command()
	async def corrupt_data(self, ctx):
		"""Resets user credentials on the server currently hosting their RPC-ident settings"""
		await ctx.send("I don't know where the corrupt journal entry originated, sorry. "
		               "I don't know who Golem is, either. Though 'she' is mentioned once or twice in my codebase, but not as a person.")


def setup(bot):
	bot.add_cog(Admin(bot))
