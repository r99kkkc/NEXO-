import discord
from discord.ext import commands
import asyncio
from msp import invoke_method, get_session_id, ticket_header

bot = commands.Bot(command_prefix='')

@bot.event
async def on_ready():
    await set_blue_presence()
    print(f'Logged in as {bot.user.name}')

async def set_blue_presence():
    activity = discord.Game(name="MovieStarPlanet")
    await bot.change_presence(activity=activity, status=discord.Status.online)

@bot.slash_command()
async def old_boonie(ctx, username: str, password: str, server: str, id: str):

    thumbs_up_emoji = bot.get_emoji(1208840708908130374)
    thumbs_down_emoji = bot.get_emoji(1200175539609145464)
    response_message = await ctx.respond(f"{thumbs_down_emoji}")

    await asyncio.sleep(5)
    
    USERNAME = username
    PASSWORD = password
    SERVER = server

    code, resp = invoke_method(
        SERVER,
        "MovieStarPlanet.WebService.User.AMFUserServiceWeb.Login", 
        [USERNAME, PASSWORD, [], None, None, "MSP1-Standalone:XXXXXX"],
        get_session_id()
    )

    status = resp.get('loginStatus', {}).get('status')
    if status != "Success":
        await ctx.send(f"Login failed,{status}")
        return


    ticket = resp['loginStatus']['ticket']
    actor_id = resp['loginStatus']['actor']['ActorId']

    try:
        clickItemId = int(id)
    except ValueError:
        await ctx.send("Failed")
        return


    code, resp = invoke_method(
        SERVER,
        "MovieStarPlanet.WebService.Pets.AMFPetService.BuyClickItem",
        [
            ticket_header(ticket),
            actor_id,
            clickItemId
        ],
        get_session_id()
    )


    edit_message = await ctx.send(f"# Done `{clickItemId}` {thumbs_up_emoji}")

@bot.slash_command()
async def eye(ctx, username: str, password: str, server: str, id: int, color: str):

     
    thumbs_up_emoji = bot.get_emoji(1208840708908130374)
    thumbs_down_emoji = bot.get_emoji(1200175539609145464)
    response_message = await ctx.respond(f"{thumbs_down_emoji}")


    USERNAME = username 
    PASSWORD = password
    SERVER = server 


    code, resp = invoke_method(
        SERVER,
        "MovieStarPlanet.WebService.User.AMFUserServiceWeb.Login", 
        [USERNAME, PASSWORD, [], None, None, "MSP1-Standalone:XXXXXX"],
        get_session_id()
    )


    status = resp.get('loginStatus', {}).get('status')
    if status != "Success":
        print(f"Login failed, status: {status}")
        return


    ticket = resp['loginStatus']['ticket']
    actor_id = resp['loginStatus']['actor']['ActorId']


    code, resp = invoke_method(
        SERVER,
        "MovieStarPlanet.WebService.BeautyClinic.AMFBeautyClinicService.BuyManyBeautyClinicItems",
        [
            ticket_header(ticket),
            actor_id,
            [
                {
                    "Colors": color,
                    "Type": 1,
                    "IsWearing": True,
                    "InventoryId": 0,
                    "IsOwned": False,
                    "ItemId": id,    
                },
            ],
        ],
        get_session_id()
    )


    edit_message = await ctx.send(f"# Done {thumbs_up_emoji}")
    
@bot.slash_command()
async def login(ctx, username: str, password: str, server: str):



    USERNAME = username 
    PASSWORD = password
    SERVER = server 

    try:
       
        code, resp = invoke_method(
            SERVER,
            "MovieStarPlanet.WebService.User.AMFUserServiceWeb.Login", 
            [USERNAME, PASSWORD, [], None, None, "MSP1-Standalone:XXXXXX"],
            get_session_id()
        )

        
        status = resp.get('loginStatus', {}).get('status')
        if status != "Success":
            print(f"Login failed, status: {status}")
            raise Exception("Login failed")


        edit_message = await ctx.send("This password fits!")

    except Exception as e:

        print(f"An error occurred: {e}")

        await ctx.send("An error occurred during login.")
@bot.slash_command()
async def login_v2(ctx, username1: str, username2: str, username3: str, username4: str, username5: str, username6: str, username7: str, username8: str, username9: str, username10: str, password: str, server: str):

    async def attempt_login(username: str):
        try:
            code, resp = invoke_method(
                server,
                "MovieStarPlanet.WebService.User.AMFUserServiceWeb.Login", 
                [username, password, [], None, None, "MSP1-Standalone:XXXXXX"],
                get_session_id()
            )

            status = resp.get('loginStatus', {}).get('status')
            if status != "Success":
                print(f"Login failed, status: {status}")
                raise Exception("Login failed")

            await ctx.send(f"This password fits! {username}")
        except Exception as e:
            print(f"An error occurred: {e}")
            await ctx.send(f"An error occurred during login. {username}")

    usernames = [username1, username2, username3, username4, username5, username6, username7, username8, username9, username10]

    for username in usernames:
        await attempt_login(username)



