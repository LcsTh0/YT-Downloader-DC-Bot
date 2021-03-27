import asyncio
import discord
import pytube
import datetime
import os
import urllib.parse
import moviepy.editor

datetime_ = datetime.datetime.now()
timedate = datetime_.strftime('%d.%m.%Y-%H.%M.%S' + ": ")

bot_name = "LcsTh's YT Downloader"

github = "https://github.com/LcsTh0/YT-Downloader-DC-Bot"
dc_invite = "https://discord.gg/PQwPRDj"

http = "https://"
ip_domain = "lcsth.de"

server_id = "570967338946527262"
channel_id = "823996526966734849"

path = "/home/ec2-user/http-data"
token_path = "/home/ec2-user/dc-token.txt"
server_log = "server_log.txt"
msg_log = "msg_log.txt"
log = "log.txt"
purged_log = "purged_log.txt"

purge_time = "03:00"

falscher_discord_nachricht = "Dieser Bot kann momentan nur auf dem ApfelPlayer Discord verwendet werdent. Wenn ein anderer Server den Bot benutzen will, kann der Besitzer mir (LcsTh#9195) gerne eine Nachricht schreiben."
keine_rechte_nachricht = "Dazu hast du keine Rechte"

command = "$yt"
audio_command = "$audio"
purge_command = "$purge"
help_command = "$help"
help_command2 = "$hilfe"

client = discord.Client()


async def dc_purge():
    channel = client.get_channel(int(channel_id))
    while True:
        zeit = datetime.datetime.now()
        stundeminute = zeit.strftime('%H:%M')
        
        if str(stundeminute) == purge_time:
            await channel.purge()
            for file in os.listdir(path):
              if file.endswith(".mp4") or file.endswith(".mp3"):
                   os.remove(path + "/" + file)
            with open(purged_log, "a") as f:
                f.write(f"{timedate} Auto Purge\n")
            print(timedate + "Auto Purge!")
            await asyncio.sleep(500)
        
        else:
            await asyncio.sleep(50)
            


with open(token_path, "r") as f:
    token = f.readline()


@client.event
async def on_ready():
    print("'{0.user}' has logged in!".format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=command))
    await dc_purge()


@client.event
async def on_message(msg):
    if msg.author != client.user:
        if isinstance(msg.channel, discord.channel.DMChannel):

            embed = discord.Embed(
                title=falscher_discord_nachricht,
                description="[ApfelPlayer Discord](" + dc_invite + ") | [GitHub](" + github + ")", color=0x00ff26)
            embed.set_footer(text=bot_name)
            await msg.channel.send(embed=embed)
            with open(msg_log, "a") as f:
                f.write(f"{timedate + str(msg.channel)} \n")
            print(timedate + str(msg.channel))

        elif str(msg.guild.id) != server_id:
            embed = discord.Embed(
                title=falscher_discord_nachricht,
                url=dc_invite, color=0x00ff26)
            embed.set_footer(text=bot_name)
            await msg.channel.send(embed=embed)

            logged = "Channel: " + msg.channel.name + "\nBenutzer: " + msg.author.name + "#" + str(
                msg.author.discriminator) + " (" + str(
                msg.author.id) + ")\nServer Name: " + msg.guild.name + "\nID: " + str(
                msg.guild.id) + "\nMitglieder: " + str(msg.guild.member_count) + "\n\n"
            with open(server_log, "a") as f:
                f.write(f"{logged}\n")

        else:
            def is_me(m):
                return m.author == client.user

            if str(msg.content).lower() == purge_command:
                if msg.author.guild_permissions.administrator:
                    await msg.channel.purge()
                    for file in os.listdir(path):
                       if file.endswith(".mp4") or file.endswith(".mp3"):
                          os.remove(path + "/" + file)
                    with open(log, "a") as f:
                        f.write(
                            f"{timedate}{msg.author.name} # {msg.author.discriminator} hat {purge_command} ausgeführt!\n")

                        print(
                        timedate + msg.author.name + "#" + msg.author.discriminator + " hat " + purge_command + " ausgeführt!")

                else:
                    await msg.channel.purge(limit=1)
                    await msg.channel.send(keine_rechte_nachricht + "{}".format(msg.author.mention))
                    with open(log, "a") as f:
                        f.write(
                            f"{timedate}{msg.author.name} # {msg.author.discriminator} hat versucht {purge_command} auszuführen!\n")
                    print(
                        timedate + msg.author.name + "#" + msg.author.discriminator + " hat versucht " + purge_command + " auszuführen!")
                    await asyncio.sleep(5)
                    await msg.channel.purge(limit=1)
            else:
                if str(msg.channel.id) != channel_id:
                    return
                if msg.author == client.user:
                    return

                if str(msg.content).lower().startswith(help_command) or str(msg.content).lower().startswith(
                        help_command2):
                    await msg.channel.send(command + " <URL>")
                    await msg.channel.send

            
                elif str(msg.content).lower().startswith(command) or str(msg.content).lower().startswith(audio_command):
                    if str(msg.content).lower() == command:
                        await msg.channel.send(command + " <URL>")

                    else:
                        os.system("docker restart httpd")

                        url = msg.content.split(' ')[1]
                        yt = pytube.YouTube(url)

                        with open(log, "a") as f:
                            f.write(f"{timedate}Downloading: {yt.title} (Requested by {msg.author.name})\n")

                        print(timedate + "Downloading: " + yt.title + " (Requested by " + str(msg.author.name) + ")")

                        await msg.channel.send("Starte Herunterladen {}".format(msg.author.mention))
                        title_patched = urllib.parse.quote(yt.title).replace("%", "_")
                        for numbers in title_patched:
                            if numbers.isdigit():
                                title_patched = title_patched.replace(numbers, "")
                        title_patched = title_patched.replace("/", "_")
                        title_patched = title_patched.replace("\\", "_")
                        yt.streams.filter(progressive=True).get_highest_resolution().download(output_path=path,
                                                                                              filename=title_patched)

                        video = moviepy.editor.VideoFileClip(path + "/" + title_patched + ".mp4")
                        video.audio.write_audiofile(path + "/" + title_patched + ".mp3")

                        with open(log, "a") as f:
                            f.write(f"{timedate}Done with: {yt.title}\n")

                        print(timedate + "Done with: " + yt.title)

                        link = http + ip_domain + "/" + title_patched

                        await msg.channel.purge(limit=1, check=is_me)
                        
                        auflösung = yt.streams.filter(progressive=True).get_highest_resolution().resolution
                        embed = discord.Embed(
                            title="Video „" + yt.title + "“ von „" + yt.author + "“ heruntergeladen",
                            description="[Video](" + link + ".mp4) (" + auflösung + ") | [Audio](" + link + ".mp3) | [GitHub](" + github + ")", color=0x00ff26)
                        embed.set_footer(text=bot_name)
                        await msg.channel.send(embed=embed)
                        await msg.channel.send("{}".format(msg.author.mention))

                        await msg.channel.purge(limit=1, check=is_me)

                else:
                    return

    else:
        return


client.run(token)
