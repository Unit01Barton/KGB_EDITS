import os
import discord
import logging
from dotenv import load_dotenv
from discord import guild
from discord import member
from discord import Game, channel
import feedparser
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
from discord.ext import commands
from discord.ext.commands import converter
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from xml.etree.ElementTree import parse
import asyncio
import requests
from discord.ext.commands.converter import ColourConverter
import random
import re
from discord.ext import commands
import itertools

bot = commands.Bot(command_prefix="$")

now = date.today()
today = now.isoformat()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
NEWS_CHANNEL = os.getenv('DISCORD_NEWS_CHANNEL')
RAPID_API = os.getenv('X_RAPIDAPI_KEY')
client = discord.Client()
# create an expandable list of RSS URLS that users can add to

NRM_Overwatch_RSS = {"name": "NRM Regional News", "URL": "https://www.qt.com.au/feeds/rss/kierans-overwatch-latest-list/", "topic": "general"}
QPS_RSS = {"name": "QPS Crime and Missing Persons", "URL": "https://mypolice.qld.gov.au/feed/", "topic": "emergency services"}
RBA_media_RSS = {"name": "RBA media releases", "URL": "https://www.rba.gov.au/rss/rss-cb-media-releases.xml", "topic": "economy"}

RSS_URLS = [NRM_Overwatch_RSS, QPS_RSS, RBA_media_RSS]
RSS_Mod_Q = []

# create an empty list for feedparser to parse the contents of the RSS_URLS list into later
feeds= []
# create an empty list for capturing links so they are only posted once
posted = []
suggestions = []
dramatis = []

def is_me():
    def predicate(ctx):
        return ctx.message.author.id == 107221097174319104
    return commands.check(predicate)                                                        

@bot.event
async def on_ready():
    liquid_guild = discord.utils.get(bot.guilds, id=107221703955841024)    
    game = discord.Game("$Commands for commands | Partying here at the Liquid Lounge until called on for an emergency.")                
    await bot.change_presence(activity=game)            
    print(f'{bot.user} is connected to {liquid_guild.name}.\n'
          f'{liquid_guild.name}(id {liquid_guild.id})'
    )
    
@bot.command(name="Commands")
async def Help_commands(ctx):
    response = (
                "$Commands | Shows you my commands."
                "$News [number ofarticles, as message)] | Usage $News 5 -m sends the last 5 news articles as a direct message (articles required, -m optional) .\n"
                "$Advice [disaster type] | Shows links to current warnings. Argument has 3 valid values, fire, flood, and all.\n"
                "$AddFeed [name, url, topic] | Takes a name, a properly formed RSS feed's url, and a topic and adds it to the new feed moderation queue.\n"
		        "$AddFeed_help | Sends a direct message with additional help in using the AddFeed command, including suggested topics.\n"
                "$Add -request | This command will allow you to add a feature request to my feature request moderation queue.\n"
                "$Poetry | This command will display the current Poet Laureate for this server.\n"
                "$Economy [verbosity, destination] | Sends either a link or a series of links of economic updates to the destination, either 'channel', or 'dm'.\n"
                )
    await ctx.author.create_dm()
    await ctx.author.send(response)
 
@bot.command(name="News")
async def News_list(ctx, number_of_articles, as_message):    
    try:
        number_of_articles = int(number_of_articles)
    except:
        if as_message == ("-m"):
            await ctx.author.create_dm()
            await ctx.author.send("Please use a numeral for the number of articles.")
        else:
            await ctx.send("Please use a numeral for the number of articles.")
    for feed in RSS_URLS:
        print(feed.get("URL"))
        URL_list = feed.get("URL")
        await ctx.author.create_dm()
        await ctx.author.send(URL_list)
    for URL in URL_list:                                                   
        feeds.append(feedparser.parse(URL))                                
        await ctx.author.create_dm()
        await ctx.author.send(feeds)
        for feed in feeds:
            #await ctx.author.create_dm()
            #await ctx.author.send(feed)
            counter = 0                                                      
            for post in feed.entries:
                print("\\")                             
                print("post title: " + post.title)             
                print("post date: " + post.published)                      
                print("post link: " + post.link)               
                if as_message == "-m":
                    await ctx.author.create_dm()
                    await ctx.author.send(post.published)
                    await ctx.author.send(post.link)
                else:
                    await ctx.send(post.published)
                    await ctx.send(post.link)
                counter += 1 
                if counter == number_of_articles:
                    break                      

@bot.command(name="Advice")
async def Advice_alert(ctx, disaster_type):
    if disaster_type == "flood":
        await ctx.send("Flood warnings can be found here: http://www.bom.gov.au/qld/warnings/flood/index.shtml.")
    elif disaster_type == "fire":
        await ctx.send("Bushfire warnings can be found here: https://www.ruralfire.qld.gov.au/map/Pages/default.aspx")
    elif disaster_type == "all":
        await ctx.send("Flood warnings can be found here: http://www.bom.gov.au/qld/warnings/flood/index.shtml.")
        await ctx.send("Bushfire warnings can be found here: https://www.ruralfire.qld.gov.au/map/Pages/default.aspx")
        await ctx.send("Stay home, wash your hands, and prepare for a long period of isolation, possibly up to the end of 2020.")
    else:
        await ctx.send("Stay home, wash your hands, and prepare for a long period of isolation, possibly up to the end of 2020.")              

@bot.command(name="AddFeed")
async def Add_Rss_Feed(ctx, name, new_url, topic):
    new_dict_name = name
    new_dict_topic = topic
    feed_check = feedparser.parse(new_url)
    xml_flag = 0
    checker = []
    for check in feed_check.entries:
        print(check.title)
        checker.append(check.title)
        print("+")
        if len(checker) == 0:
            continue
        else:
            xml_flag = 1
            break
    if xml_flag == 1:
        new_dict_url = new_url
        await ctx.send("Thanks, I've added that feed to my moderation.")
    else:
        await ctx.send("I'm sorry, I think there's something wrong with the feed you tried to give me. Please validate the feed with https://validator.w3.org/feed/ first.")
        print(f'{ctx.author} passed in a bad RSS URL')
    new_dict = {"name": new_dict_name, "url": new_dict_url, "topic": new_dict_topic}
    RSS_Mod_Q.append(new_dict)
    mod_q = open("RSS_ModQ.txt", "a")
    mod_q.write(new_dict)
    mod_q.close
    
@bot.command(name="AddFeed_help")
async def Add_feed_help(ctx):
    await ctx.author.create_dm()
    await ctx.author.send("Hi, here are some extra tips on using the AddFeed command and making sure your feed is approved.")
    await ctx.author.send("The AddFeed command takes 3 arguments, a name, a url, and a topic.")
    await ctx.author.send("If the name you've given the feed includes a space, make sure you've wrapped it in quotation marks, or only the first word will appear.")
    await ctx.author.send("Also keep in mind that the feeds are human-moderated, so decency is a factor in the approval process.")
    await ctx.author.send("Most importantly, the url you're trying to use must point to a properly-formed RSS feed, and those can be rare.")
    await ctx.author.send("For your best chance of succeeding, run your url through the w3schools RSS validation service at https://validator.w3.org/feed/ before adding it here.")
    await ctx.author.send("You may find very few RSS feeds are put together properly, especially those from Wordpress sites. Sadly, I just can't work with them � I'm a bot.")
    await ctx.author.send("The topic is open to your discretion, but if it is more than one word long, again, please wrap it in quotation marks.")
    await ctx.author.send("Please make the topic descriptive and, if possible, attractive to those looking for something to read. For instance 'Trivia' instead of 'Generic'.")
    await ctx.author.send("When adding feeds for emergency or health services, please send the Group Editor a DM with supporting documents to aid in moderation.")

@bot.command(name="YourShiftIsOver")
@is_me()
async def Sleep_Now_Brook(ctx):
    await bot.remove_command(help)
    await ctx.author.create_dm()
    await ctx.author.send("I'll see you back at the terminal, bye!")
    await bot.logout()

@bot.command(name="Poetry")
async def Guild_Poet(ctx):
    await ctx.send("Oh, I'm no poet, you'd have to ask the master, <@482011749818564628> for that.")
    
@bot.command(name="clear")
async def clear_bot_messages(ctx, messages):
    print(type(messages))
    flush = int(messages)
    print(type(flush))
    if flush <= 100 and flush > 0:
        await ctx.channel.purge(limit=flush)
        print("messages deleted")
    else:
        await ctx.send("Please enter a number from 1 to 100 inclusive.")
        print("messages were not deleted")

@bot.command(name="Users")
@is_me()
async def Dump_User_List(ctx, verbosity):
    for member in ctx.guild.members:
        if member != client.user:
            member_id = str(member.id)
            await ctx.author.create_dm()
            if verbosity == "-c":
                await ctx.author.send(f'user_id: ' + member_id)
                continue
            elif verbosity == "-v":
                await ctx.author.send(f'date_observed: ' + today)
                await ctx.author.send(f'user.name: ' + member.name)
                await ctx.author.send(f'user.display_name: ' + member.display_name)
                try:
                    await ctx.author.send(f'user.role: ' + str(member.top_role))  
                except:
                    continue
                try:
                    for activity in member.activities:
                        await ctx.author.send(f'user.activity: ' + member.activity) 
                except:
                    continue
                await ctx.author.send(f'user.avatar_url: ' + str(member.avatar_url))
                await ctx.author.send(f'Is the user a bot? ' + str(member.bot))   

@bot.command(name="Economy")
async def Economic_reading_list(ctx, verbosity, destination):
    econ_100 = "I know Kieran always keeps up to date with the daily St George morning update, found here: https://www.stgeorge.com.au/corporate-business/economic-reports/morning-report"
    econ_101 = "The following links will be updated with feeds at a later date. The analysis in these reports are considered trusted but optimistic by the Group Editor."
    econ_102 = "Morning reports: >> https://www.stgeorge.com.au/corporate-business/economic-reports/morning-report"
    econ_103 = "2019 Key Indicator Snapshots: >> https://www.stgeorge.com.au/corporate-business/economic-reports/data-snapshots"
    econ_104 = "Interest Rate Outlook: >> https://www.stgeorge.com.au/corporate-business/economic-reports/interest-rate-outlook"
    econ_105 = "Australian Dollar Outlook: >> https://www.stgeorge.com.au/corporate-business/economic-reports/australian-dollar-outlook"
    econ_106 = "Quarterly Economic Outlook: >> https://www.stgeorge.com.au/corporate-business/economic-reports/economic-outlook"
    econ_107 = "State Economic Reports: >> https://www.stgeorge.com.au/corporate-business/economic-reports/state-economic-reports"
    econ_108 = "Economic Calendar: >> https://www.stgeorge.com.au/corporate-business/economic-reports/economic-calendar"
    econ_109 = "Budget Snapshot: >> https://www.stgeorge.com.au/corporate-business/economic-reports/budget-snapshot"
    econ_110 = "Weekly Economic Outlook: >> https://www.stgeorge.com.au/corporate-business/economic-reports/weekly-economic-outlook"
    econ_111 = "Speeches by the RBA: >> https://www.rba.gov.au/speeches/"
    econ_112 = "SportsBet Politics section: >> https://www.sportsbet.com.au/betting/politics"
    econ_113 = "SportsBet Futures section: >> https://www.sportsbet.com.au/betting/politics/outrights"
    econ_114 = "Bet365 Australian Politics section: >> https://www.bet365.com.au/#/AS/B136/"
    econ_115 = "I caution against disregarding the final 3 links when making decisions about macroeconomic predictions. They've proven to be accurate leading indicators in the past."
    reading_list = [econ_100, econ_101, econ_102, econ_103, econ_104, econ_105, econ_106, econ_107, econ_108, econ_109, econ_110, econ_111, econ_112, econ_113, econ_114, econ_115]
    if verbosity == "-c":
        if destination == "channel":
            await ctx.send(econ_100)
        else:
            await ctx.author.create_dm()
            await ctx.author.send(econ_100)
    if verbosity == "-v":
        if destination == "channel":
            for item in reading_list:
                await ctx.send(item)
        else:
            for item in reading_list:
                await ctx.author.create_dm()
                await ctx.author.send(item)



alert = [] 
@bot.command(name="Fires")   
async def update_fire_news(ctx):
    NEWS_URL = "https://www.qfes.qld.gov.au/data/alerts/bushfireAlert.xml"
    lockout = []
    with open("Brook\code\\fire_alerts.json", "r") as dedupe:
        fire_alerts = json.load(dedupe)    
    events = fire_alerts.get("alerts")
    for event in events:
        for pair in event:
            print("Pair:")
            print(type(pair))
            print(pair)
            #index = len(pair)
            for value in pair:    
                if value[:2] == "QF":
                    lockout.append(value)
                    print(lockout)
    parse_xml_url = urlopen(NEWS_URL)
    xml_page = parse_xml_url.read()
    soup_page = BeautifulSoup(xml_page, "lxml")
    news_list = soup_page.findAll("entry")
    print(news_list)
    for getfeed in news_list:
        if getfeed.id.text in lockout:
            print("prevented duplicate ID")
            break
        else:
            category = getfeed.category['term']
            fire_title = getfeed.title.text
            fire_category = str(category)
            fire_content = getfeed.content.text
            fire_published = getfeed.published.text
            fire_updated = getfeed.updated.text
            fire_id = getfeed.id.text
            for line in getfeed:
                test_for_geo = str(line)
                if test_for_geo.startswith("<geo"):
                    for_geo = test_for_geo[14:]
                    geolocation = for_geo[:-15]
            alert = ({"alert_id": fire_id, "category": fire_category, "content": fire_content, "published": fire_published, "title": fire_title, "updated": fire_updated, "location": geolocation})
    fire_alerts.get("alerts").append(alert)
    with open("fire_alerts.json", "w") as data:
        json.dump(fire_alerts, data, indent=2)


klaxon = []

@bot.command(name="BOM")
async def update_bom_news(ctx):
    bom_alerts = dict()
    # with open("bom_alerts.json") as container:
    #     bom_alerts = json.load(container)
    bom_req = urllib.request.Request("http://www.bom.gov.au/fwo/IDZ00056.warnings_qld.xml", data=None, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0"}, origin_req_host="123.211.133.33", unverifiable="True", method="GET")
    with urllib.request.urlopen(bom_req) as response:
        bom_page = response.read()
    print(bom_page)
    bom_page = BeautifulSoup(bom_page, 'lxml')
    print(bom_page)
    bom_warnings = bom_page.find_all("item")    
    print("bom_page")
    print(bom_page)
    for item in bom_warnings:
        title_tags = item.find("title")
        date_tag = item.find("pubdate")
        link_tags = item.find("link")
        title = title_tags.get_text()
        date = date_tag.get_text()
        link = link_tags.next
        klaxon.append({"title":title, "date": date, "link": link.rstrip()})
        print(klaxon)
    for alert in klaxon:
        bom_alerts["alerts"].append(alert)
    with open("bom_alerts.json", "w") as data:
        json.dump(bom_alerts, data, indent=2) 
    
@bot.command(name="MoveOn")
async def move_apartment(ctx):
    await ctx.send("Terminating epistomolgical fields, unbinding existing contacts. Mind seal broken.")       

@bot.command(name="playlist_me")
async def need_tunes_bro(ctx):
    await ctx.send("I've got you, sending you some Rhythm bot commands in a DM now!")
    ctx.author.create_dm
    await ctx.author.send("Here are the commands for this year's Triple J Hottest 100. I hope it helps.")
    with open("TripleJ-Hot100-2020.txt", "r") as tunes:
        for song in tunes:
            await ctx.author.send(song)
            
@bot.command(name="joke")
async def random_joke(ctx):
    url = "https://joke3.p.rapidapi.com/v1/joke"

    querystring = {"nsfw":"true"}

    headers = {
        'x-rapidapi-host': "joke3.p.rapidapi.com",
        'x-rapidapi-key': RAPID_API
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
     
    print(response.text)


@bot.command(name="valid_groups")
async def mono_list_groups(ctx):
    valid_groups = ["Purple", "Light-Blue", "Violet", "Orange", "Red", "Yellow", "Dark-Green", "Dark-Blue", "Utilities", "Railroads", "Corner", "tax", "Chance", "Commmunity Chest"]
    await ctx.send("""
        ```css
        # Property Groups
        [ Purple  ]
        [ Light-Blue  ]
        [ Violet  ]
        [ Orange  ]
        [ Red ]
        [ Yellow ]
        [ Dark-Green ]
        [ Dark-Blue ]
        < Utilities >
        < Railroads >
        < Corner >
        < Tax >
        < Chance > 
        < Commmunity Chest >
          ```
          """)
    return valid_groups

@bot.command(name="roll")
async def roll_dice(ctx, both: bool):
    results = []
    if both != True:
        outcome = random.randint(1, 6)
        await ctx.send("> :game_die: <@"+str(ctx.author.id)+"> rolled: **" + str(outcome) + "** \n> dice = " + str(outcome))
    else:
        outcome1 = random.randint(1, 6)
        outcome2 = random.randint(1, 6)
        total_outcome = outcome1 + outcome2
        await ctx.send("> :game_die: <@"+str(ctx.author.id)+"> rolled: **" + str(total_outcome) + "** \n> dice = " + str(outcome1) + ", " + str(outcome2))
        
def intake_dice(multiplier, polycount):
    results = []
    multiplier = int(multiplier.group(1))
    polycount = int(polycount.group(1))
    for roll in range(multiplier):
        print(r"rolling")
        results.append(random.randrange(1, polycount))
    return results

@bot.command(name="r")
#add ability to reroll 1's
#add ability to reroll misses, need to take parameters for that
#force reroll successes
#specify target number for rerolls etc
async def roll_polynomial(ctx, diceroll):
    results = []
    multiplier = re.search("(^\d*)", diceroll)
    if multiplier != None:
        print(multiplier.group(1))
        try:
            multiplier = int(multiplier.group(1))
        except ValueError:
            multiplier = 0 
    else:
        multiplier = 1      
    diceform = re.findall("\d*(d)", diceroll)
    if len(diceform) > 1:
        for group in diceform:
            print("diceform search: ")
            print(re.search("([+|-]\d*d\d)", diceroll))
            results.append(intake_dice(re.search("[+|-](\d*)d\d", diceroll), re.search("[+|-]\d*d(\d*)", diceroll)))
    elif len(diceform) == 1:
        diceform = str(re.search("\d*(d)", diceroll))
    else:
        await ctx.send("Sorry, rolls need to be formatted #**d**#+/-# where # is a number and the first, last and plus sign are optional.")    
    polycount = re.search("[d](\d*)", diceroll)
    if polycount != None:
        print("polycount search: ")
        print(polycount.group(1))
        try:
            polycount = int(polycount.group(1))
        except ValueError:
            polycount = 20  
    add_sign = re.search("[d](?:\d*)([+|-])", diceroll)
    bonus_text = "no bonuses, just "
    if add_sign != None:
        add_sign = add_sign.group(1)
        if add_sign == "+":
            bonus_text = "a bonus of "
        else:
            bonus_text = "a debuff of "
    else:
        add_sign = ""
    modifier = 0
    bonus = re.search("[+|-](\d*)(?![d])", diceroll)
    if bonus != None or "":
        print("bonus group 1: ")
        print(bonus.group(1))
        bonus = bonus.group(1)
        bonuses = re.findall("([+|-]\d*)(?![d])", diceroll)
        if len(list(bonuses)) > 1:
            print("bonus list length:")
            print(len(list(bonuses)))
            print(bonuses)
            bonus = 0
            for mod in bonuses:
                print("mod: ", mod)
                sign = mod[:1]
                if mod[1:] == "":
                    size = 0
                else:
                    size = int(mod[1:])
                if sign == "+":
                    modifier = modifier + size
                elif sign =="-":
                    modifier = modifier - size
        print("bonus: ", bonus, " modifier: ", modifier)
        bonus = bonus + modifier
        print("bonus: ", bonus, "modifier: ", modifier)
    else:
        print("bonus == none condition triggered")
        bonus = 0
    print("The variables are: ")
    print(multiplier)
    print(polycount)
    print(add_sign)
    print(bonus)
    score = 0
    if results != "":
        results = list(itertools.chain.from_iterable(results))
        print(results)
    for roll in range(multiplier):
        print("rolling")
        results.append(random.randrange(1, polycount))
        print(results)
    if add_sign == "+":
        score = sum(results) + bonus
        print("score: ", score)
    elif add_sign == "-":
        score = sum(results) - bonus
        print("score:", score)
    else:
        score = sum(results)
        print("score: ", score)
    await ctx.send("> :game_die: <@"+str(ctx.author.id)+"> rolled: **" + str(score) + "** \n> " + str(results) + " \n> :muscle: With " + bonus_text  + add_sign + str(bonus))



@bot.command(name="groups_verbose")
async def group_list_verbose(ctx):
    await ctx.send("""
        ```css
        #Property-Groups
        [ Purple  ]
            *  Mediterranean Ave
            *  Baltic Ave
        [ Light-Blue ]
            * Oriental Ave
            * Vermont Ave
            * Connecticut Ave
        [ Violet  ]
            * St Charles Place
            * States Ave
            * Virginia Ave
        [ Orange  ]
            * St James Place
            * Tennessee Ave
            * New York Ave
        [ Red ]
            * Kentucky Ave
            * Indiana Ave
            * Illinois Ave
        [ Yellow ]
            * Atlantic Ave
            * Ventnor Ave
            * Marvin Gardens
        [ Dark-Green ]
            * Pacific Ave
            * North Carolina Ave
            * Pennsylvania Ave
        [ Dark-Blue ]
            * Park Place
            * Boardwalk
        [ Utilities ]
            * Electric Company
            * Water Works
        [ Railroads ]
            * Reading Railroad
            * Pennsylvania Railroad
            * B & O Railroad
            * Short Line Railroad
        [ Corner ]
            * Go!
            * Jail
            * Free Parking
            * Go To Jail
        [ Tax ]
            * Income Tax
            * Luxury Tax
        [ Chance ] 
            * Chance Card
        [ Commmunity Chest ]
            * Commmunity Chest Card
          ```
          """)

@bot.command(name="group_list")
async def mono_list_properties(ctx, group):
    valid_groups = ["Purple", "Light-Blue", "Violet", "Orange", "Red", "Yellow", "Dark-Green", "Dark-Blue", "Utilities", "Railroads", "Corner", "tax", "Chance", "Commmunity Chest"]
    if group not in valid_groups:
        print("That's not a valid Monopoly Group, please invoke the valid_groups command.")
    print("Displaying all properties in the ", group, "group/s.")
    with open("monopoly_props.json") as source:
        mono_data = json.load(source)
    prop_lists = mono_data["Properties"]
    for prop, estate in prop_lists.items():
        print(estate["Group"])
        print(group)
        if estate['Group'] == group:
                embeded = discord.Embed(title=estate["Name"], description=["Name"], color=discord.Colour.gold)
                embeded.add_field(name="Price", value=estate["Price"], inline=False)
                embeded.add_field(name="Rent", value=["Rent"], inline=True)
                embeded.add_field(name="Position:", value=estate["Position"], inline=True)                
                if estate["Group"] == "Railroad":
                    embeded.add_field(name="2 owned:", value=estate["2 owned"], inline=True)
                    embeded.add_field(name="2 owned:", value=estate["3 owned"], inline=True)
                    embeded.add_field(name="2 owned:", value=estate["4 owned"], inline=True)
                elif estate["Group"] == "Railroad":
                    embeded.add_field(name="Both owned:", value=estate["Both owned"], inline=True)
                else:
                    embeded.add_field(name="1 House:", value=estate["2 owned"], inline=True)
                    embeded.add_field(name="2 Houses:", value=estate["3 owned"], inline=True)
                    embeded.add_field(name="3 Houses:", value=estate["4 owned"], inline=True)
                    embeded.add_field(name="4 Houses:", value=estate["4 owned"], inline=True)
                    embeded.add_field(name="Hotel:", value=estate["Hotel"], inline=True)
                await ctx.send(embed=embeded)


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
logger.addHandler(handler)


bot.run(TOKEN)