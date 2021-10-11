'''
Inferbot ©2021 Infernaught
Created by Nathan Boehm
If the code outputs an error on startup, type this into the shell:
pip install discord-together
'''
import discord
import re
import os
from PIL import Image, ImageFont, ImageDraw
import math
import requests
import emoji
from discordTogether import DiscordTogether
from keep_alive import keep_alive
client = discord.Client()

@client.event
async def on_ready():
  print("{0.user} is ready to rock!".format(client))
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=str("some cool music. !help")))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content == "!help":
    embedVar = discord.Embed(title="Help Menu", description="Le epic command list:", color=0x00ff00)
    embedVar.add_field(name="!help [command]", value="Gives information about a command.", inline=False)
    embedVar.add_field(name="!hottake [your hot take]", value="Sends an anonymous post in #hot-music-takes. Only works in DMs.", inline=False)
    embedVar.add_field(name="!album [text] [image]", value="Generates an album cover with the image and the title you send.", inline=False)
    embedVar.add_field(name="!party", value="Starts YouTube Together, letting you play music in the voice channel.", inline=False)
    embedVar.set_footer(text="Alan please add footer.")
    await message.channel.send(embed=embedVar)
  if message.content == "!help help":
    embedVar = discord.Embed(title="!help", description="Helps you with a helpful help menu.", color=0xffff00)
    embedVar.set_footer(text="For your help.")
    await message.channel.send(embed=embedVar)
  if message.content == "!help hottake" or message.content == "!hottake":
    embedVar = discord.Embed(title="!hottake [text]", description="DM exclusive command. Sends your hot take in #hot-music-takes anonymously.", color=0xffff00)
    embedVar.set_footer(text="For the takes that are too hot for TV.")
    await message.channel.send(embed=embedVar)
  if message.content.startswith("!hottake "):
    if message.channel.type is discord.ChannelType.private:
      embedVar = discord.Embed(title="Hot take", description=message.content[9:], color=0xff0000)
      embedVar.set_footer(text="From Anonymous.")
      hottakechannel = client.get_channel(887513461574230047)
      print("Hot take from " + str(message.author) + ": " + message.content[9:])#this is only here in case we have a sussy troll
      await hottakechannel.send(embed=embedVar)
    else:
      await message.delete()
      await message.author.send("This command only works in DMs. I've deleted your message so no one saw it (hopefully).")
  if message.content == ("!help album") or message.content == ("!album"):
    embedVar = discord.Embed(title="!album [text] [image]", description="Generates an album cover with the image you send and gives it the title of the text you give.", color=0xffff00)
    embedVar.set_footer(text="NEW INFERNAUGHT ALBUM CONFIRMED! (REAL) 2018 WORKING NO VIRUS")
    await message.channel.send(embed=embedVar)
  if message.content.startswith("!album "):
    custom_emojis = re.findall(r'<:\w*:\d*>', message.content)
    if len(custom_emojis) > 0 or emoji.demojize(message.content) != message.content:
      await message.channel.send("You can't have emojis in the command.")
      return
    text = message.content[7:]
    for mention in message.mentions:
      text = text.replace(str(mention.mention).replace("!", ""), mention.display_name)
    if len(message.attachments) == 0:
      await message.channel.send("Please send an image with the command.")
      return
    if message.attachments[0].url[-4:].lower() != ".png" and message.attachments[0].url[-4:].lower() != ".jpg" and message.attachments[0].url[-5:].lower() != ".jpeg" and message.attachments[0].url[-4:].lower() != ".gif":
      await message.channel.send("The file type you sent is invalid.")
      return
    logo = Image.open("blankalbum.png")
    response = requests.get(message.attachments[0].url)
    img = open("albumimg.png", "wb")
    img.write(response.content)
    img.close()
    image = Image.open("albumimg.png")
    final2 = Image.new("RGBA", image.size)
    final2 = Image.alpha_composite(final2, image.convert('RGBA'))
    if image.width <= image.height:
      final2 = Image.alpha_composite(final2, logo.resize((image.width, image.width)).crop((0, 0, image.width, image.height)).convert('RGBA'))
    else:
      #if image.width % 2 == 1:
      #print(str(((image.width - image.height) / 2) + image.height + ((image.width - image.height) / 2)))
      final2 = Image.alpha_composite(final2, logo.resize((image.height, image.height)).crop((math.floor(0 - ((image.width - image.height) / 2)), 0, math.floor(image.height + ((image.width - image.height) / 2)), image.height)).convert('RGBA'))
    #image.paste(logo.resize((image.width, image.width)), (0, 0))
    fontsize = 1
    draw = ImageDraw.Draw(final2)
    font = ImageFont.truetype("timesnewroman.ttf", 1)
    textw, texth = draw.textsize(text, font=font)
    #while font.getsize(text)[0] < image.width * 0.9 and font.getsize(text)[1] < image.height / 2:
    while textw < image.width * 0.9 and texth < image.height / 2:
      fontsize += 1
      textw, texth = draw.textsize(text, font=font)
      font = ImageFont.truetype("timesnewroman.ttf", fontsize)
    draw.text(((image.width - textw) / 2, image.height * 0.75 - texth / 2), text, (255, 0, 0), font=font)
    final2.save("album.png")
    if os.path.getsize("album.png") >= 8000000:
      final2 = final2.resize((math.floor(final2.width / 2), math.floor(final2.height / 2)))
      final2.save("album.png")
    await message.channel.send(file=discord.File("album.png"))
  if message.content == "!help party":
    embedVar = discord.Embed(title="!party", description="Starts YouTube Together, letting you play music in the voice channel. You have to be in a voice channel to use this command.", color=0xffff00)
    embedVar.set_footer(text="Moosic")
  if message.content == "!party":
    if message.author.voice is None:
      await message.channel.send("You need to be in a voice channel to use this command.")
    else:
      togetherControl = DiscordTogether(client)
      link = await togetherControl.create_link(message.author.voice.channel.id, 'youtube')
      await message.channel.send(f"Click the blue link!\n{link}")
keep_alive()
client.run(os.getenv("TOKEN"))