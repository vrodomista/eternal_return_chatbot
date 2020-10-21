import os
from twitchio.ext import commands
from bs4 import BeautifulSoup
import requests




def tableDataText(table):   
    def rowgetDataText(tr, coltag='td'): # td (data) or th (header)       
        return [td.get_text(strip=True) for td in tr.find_all(coltag)]  
    rows = []
    trs = table.find_all('tr')
    headerow = rowgetDataText(trs[0], 'th')
    if headerow: # if there is a header row include first
        rows.append(headerow)
        trs = trs[1:]
    for tr in trs: # for every table row
        rows.append(rowgetDataText(tr, 'td') ) # data row       
    return rows


def getSoloRank(lobby):
    solopage = requests.get('https://www.playeternalreturn.com/ranking/solo/' )
    solosoup = BeautifulSoup(solopage.text, 'html.parser')
    solo_list_table = tableDataText(solosoup.find('table'))
    item_dict = {}
    for item in solo_list_table:
        if item[1] == lobby:
            item_dict={"rank": item[0], "LP": item[2]}
    if "rank" not in item_dict: 
        return ("%s isn't even on the leaderboards, get good!" % lobby)
    return ("%s solo Rank: %s | LP: %s" % (lobby, item_dict["rank"], item_dict["LP"]))

def getDuoRank(lobby):
    duopage = requests.get('https://www.playeternalreturn.com/ranking/duo/' )
    duosoup = BeautifulSoup(duopage.text, 'html.parser')
    duo_list_table = tableDataText(duosoup.find('table'))
    item_dict = {}
    for item in duo_list_table:
        if item[1] == lobby:
            item_dict={"rank": item[0], "LP": item[2]}
    if "rank" not in item_dict: 
        return ("%s isn't even on the leaderboards, get good!" % lobby)
    return ("%s duo Rank: %s | LP: %s" % (lobby, item_dict["rank"], item_dict["LP"]))

def getSquadRank(lobby):
    squadpage = requests.get('https://www.playeternalreturn.com/ranking/squad/' )
    squadsoup = BeautifulSoup(squadpage.text, 'html.parser')
    squad_list_table = tableDataText(squadsoup.find('table'))
    item_dict = {}
    for item in squad_list_table:
        if item[1] == lobby:
            item_dict={"rank": item[0], "LP": item[2]}
    if "rank" not in item_dict: 
        return ("%s isn't even on the leaderboards, get good!" % lobby)
    return ("%s squad Rank: %s | LP: %s" % (lobby, item_dict["rank"], item_dict["LP"]))


bot = commands.Bot(
    irc_token='IRC_PLACEHOLDER',
    api_token='IRC_PLACEHOLDER',
    nick='vinnie',
    prefix='!',
    initial_channels=['Channel_Name']
)

@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print("Vinnie is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg("Channel_Name", f"/me has landed!")

@bot.command(name='solo')
async def solo(ctx):
    print(ctx.message.raw_data)
    await ctx.send(getSoloRank(ctx.message.raw_data.split()[-1]))

@bot.command(name='duo')
async def duo(ctx):
    await ctx.send(getDuoRank(ctx.message.raw_data.split()[-1]))

@bot.command(name='squad')
async def squad(ctx):
    await ctx.send(getSquadRank(ctx.message.raw_data.split()[-1]))



# @bot.event
# async def event_message(ctx):
#     'Runs every time a message is sent in chat.'

#     # make sure the bot ignores itself and the streamer
#     if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
#         return

#     await bot.handle_commands(ctx)

#     # await ctx.channel.send(ctx.content)

#     if 'hello' in ctx.content.lower():
#         await ctx.channel.send(f"Hi, @{ctx.author.name}!")


@bot.command(name='test')
async def test(ctx):
    await ctx.send('test passed!')


if __name__ == "__main__":
    bot.run()
