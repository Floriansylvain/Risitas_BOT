from discord.ext import commands

errors = {commands.MissingRequiredArgument:"A required argument is missing !",
          commands.TooManyArguments:"You entered too many arguments !",
          commands.NotOwner:"Only the owner of the bot can use this command... *Where did you get it ?*",
          commands.BotMissingPermissions:"I'm missing some permissions to execute this command !"}
