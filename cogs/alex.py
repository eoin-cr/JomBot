# import matplotlib.pyplot as plt
import discord
from discord.ext import commands
import numpy as np
import os
# import PIL
import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers
# from tensorflow.keras.models import Sequential
import pathlib
import aiohttp


new_model = tf.keras.models.load_model('models/alex')
print(new_model.summary())


def valid_image_url(url: str):
    image_extensions = ['png', 'jpg', 'jpeg', 'gif']
    for image_extension in image_extensions:
        if url.endswith('.' + image_extension):
            return True
    return False


async def download_image(url: str, images_path: str = ""):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                image_name = os.path.basename(url)
                with open(os.path.join(images_path, image_name), "wb") as f:
                    f.write(await resp.read())


class Alex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.filename = None
        print("Alex initialised")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # if valid_image_url(message.content):
        #     print("dl1")
        #     await download_image(message.content, "images")

        for attachment in message.attachments:
            if valid_image_url(attachment.url):
                # print("dl2")
                await attachment.save(os.path.join("images", attachment.filename))
                self.filename = "images/" + attachment.filename

                # print("running test")

                img_height = 180
                img_width = 180
                img = tf.keras.utils.load_img(
                    self.filename, target_size=(img_height, img_width)
                )
                img_array = tf.keras.utils.img_to_array(img)
                img_array = tf.expand_dims(img_array, 0)  # Create a batch

                predictions = new_model.predict(img_array)
                score = tf.nn.softmax(predictions[0])

                # print(np.argmax(score))
                # print(np.max(score))

                print(
                    "This image most likely belongs to {} with a {:.2f} percent confidence."
                    .format(np.argmax(score), 100 * np.max(score))
                )

                if np.argmax(score) == 0 and np.max(score) * 100 > 65:
                    return await message.channel.send("<@361130857013968907>")
                    # I'm so sorry alex


def setup(bot):
    bot.add_cog(Alex(bot))
