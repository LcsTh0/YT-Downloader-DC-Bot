import asyncio
import discord
import pytube
import datetime
from os import system
import urllib.parse
import moviepy.editor

datetime_ = datetime.datetime.now()
timedate = datetime_.strftime('%d.%m.%Y-%H.%M.%S' + ": ")

http = "https://"
ip_domain = "lcsth.de"
token = ""
command = "$yt"
audio_command = "$audio"
path = "http-data"
dc_invite = "https://discord.gg/PQwPRDj"
server_id = "570967338946527262"
channel_id = "823996526966734849"
server_log = "server_log.txt"
msg_log = "msg_log.txt"
log = "log.txt"
purged_log = "purged_log.txt"
del_vids_script = "/home/ec2-user/del_vids.sh"
reload_scirpt = "/home/ec2-user/reload.sh"
purge_time = "03:00"
bot_name = "LcsTh's YT Downloader"
falscher_discord_nachricht = "Dieser Bot kann momentan nur auf dem ApfelPlayer Discord verwendet werdent. Wenn ein anderer Server den Bot benutzen will, kann der Besitzer mir (LcsTh#9195) gerne eine Nachricht schreiben."
keine_rechte_nachricht = "Dazu hast du keine Rechte"
help_command = "$help"
help_command2 = "$hilfe"
purge_command = "$purge"

client = discord.Client()


async def dc_purge():
    channel = client.get_channel(int(channel_id))
    while True:
        zeit = datetime.datetime.now()
        dt = zeit.strftime('%H:%M')
        if str(dt) == purge_time:
            await channel.purge()
            system("bash " + del_vids_script)

            with open(purged_log, "a") as f:
                f.write(f"{timedate} Auto Purge\n")

            print(timedate + "Auto Purge!\n")
            await asyncio.sleep(500)
        else:
            await asyncio.sleep(50)


@client.event
async def on_ready():
    print("'{0.user}' has logged in!".format(client))
    await dc_purge()


@client.event
async def on_message(msg):
    if msg.author != client.user:
        if isinstance(msg.channel, discord.channel.DMChannel):

            embed = discord.Embed(
                title=falscher_discord_nachricht,
                url=dc_invite, color=0x00ff26)
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
                    deleted = await msg.channel.purge()
                    system("bash " + del_vids_script)
                else:
                    delete = await msg.channel.purge(limit=1)
                    await msg.channel.send(keine_rechte_nachricht + "{}".format(msg.author.mention))
                    with open(log, "a") as f:
                        f.write(
                            f"{timedate}{msg.author.name} # {msg.author.discriminator} hat versucht {purge_command} auszuführen!\n")
                    print(
                        timedate + msg.author.name + "#" + msg.author.discriminator + " hat versucht " + purge_command + " auszuführen!\n")
                    await asyncio.sleep(5)
                    delete = await msg.channel.purge(limit=1)
            else:
                if str(msg.channel.id) != channel_id:
                    return
                if msg.author == client.user:
                    return

                if str(msg.content).lower().startswith(help_command) or str(msg.content).lower().startswith(
                        help_command2):
                    await msg.channel.send(command + " <URL>")
                    await msg.channel.send

                if str(msg.content).lower().startswith(audio_command):
                    if str(msg.content).lower() == audio_command:
                        await msg.channel.send(audio_command + " <URL>")

                    else:
                        system("bash /home/ec2-user/reload")

                        url = msg.content.split(' ')[1]
                        yt = pytube.YouTube(url)

                        with open(log, "a") as f:
                            f.write(f"{timedate}Downloading: {yt.title} (Requested by {msg.author.name})\n")

                        print(timedate + "Downloading: " + yt.title + " (Requested by " + str(msg.author.name) + ")\n")

                        await msg.channel.send("Starte Herunterladen {}".format(msg.author.mention))
                        title_patched = urllib.parse.quote(yt.title).replace("%", "_")
                        for numbers in title_patched:
                            if numbers.isdigit():
                                title_patched = title_patched.replace(numbers, "")
                        title_patched = title_patched.replace("/", "_")
                        title_patched = title_patched.replace("\\", "_")
                        yt.streams.filter(progressive=True).get_highest_resolution().download(output_path=path,
                                                                                              filename=title_patched)
                        print(title_patched)
                        video = moviepy.editor.VideoFileClip(path + "/" + title_patched + ".mp4")
                        video.audio.write_audiofile(path + "/" + title_patched + ".mp3")
                        with open(log, "a") as f:
                            f.write(f"{timedate}Done with: {yt.title} (Audio))\n")

                        print(timedate + "Done with: " + yt.title + " (Audio)")

                        link = http + ip_domain + "/" + title_patched + ".mp3"

                        delete = await msg.channel.purge(limit=1, check=is_me)

                        embed = discord.Embed(
                            title="Audio „" + yt.title + "“ von „" + yt.author + "“ fertig heruntergeladen", url=link,
                            color=0x00ff26)
                        embed.set_footer(text=bot_name)
                        await msg.channel.send(embed=embed)
                        await msg.channel.send("{}".format(msg.author.mention))

                        delete = await msg.channel.purge(limit=1, check=is_me)

                elif str(msg.content).lower().startswith(command):
                    if str(msg.content).lower() == command:
                        await msg.channel.send(command + " <URL>")

                    else:
                        system("bash " + reload_scirpt)

                        url = msg.content.split(' ')[1]
                        yt = pytube.YouTube(url)

                        with open(log, "a") as f:
                            f.write(f"{timedate}Downloading: {yt.title} (Requested by {msg.author.name})\n")

                        print(timedate + "Downloading: " + yt.title + " (Requested by " + str(msg.author.name) + ")\n")

                        await msg.channel.send("Starte Herunterladen {}".format(msg.author.mention))
                        title_patched = urllib.parse.quote(yt.title).replace("%", "_")
                        for numbers in title_patched:
                            if numbers.isdigit():
                                title_patched = title_patched.replace(numbers, "")
                        title_patched = title_patched.replace("/", "_")
                        title_patched = title_patched.replace("\\", "_")
                        yt.streams.filter(progressive=True).get_highest_resolution().download(output_path=path,
                                                                                              filename=title_patched)

                        with open(log, "a") as f:
                            f.write(f"{timedate}Done with: {yt.title}\n")

                        print(timedate + "Done with: " + yt.title)

                        link = http + ip_domain + "/" + title_patched + ".mp4"

                        delete = await msg.channel.purge(limit=1, check=is_me)

                        embed = discord.Embed(
                            title="Video „" + yt.title + "“ von „" + yt.author + "“ fertig heruntergeladen", url=link,
                            color=0x00ff26)
                        embed.set_footer(text=bot_name)
                        await msg.channel.send(embed=embed)
                        await msg.channel.send("{}".format(msg.author.mention))

                        delete = await msg.channel.purge(limit=1, check=is_me)

                else:
                    return

    else:
        return


client.run(token)
