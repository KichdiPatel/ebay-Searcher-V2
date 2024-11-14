import signal
import time

# API KEY:
# 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

from openai import OpenAI

client = OpenAI(api_key="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")


# Uses the title and description of a given listing to determine if it is a good product, where
# it willl return the main keywords of all the products in the listing( some listings have more than 1 item)
# If, it is not a good product, it will return 'None'
def get_products_basic(_title, _description):
    # print("start gptcheck()")
    prompt = (
        "Please provide the main product name for each of the products mentioned in the listing. I need "
        "the product name to do a search on eBay. If no specific company is mentioned, return 'None'. If "
        "there is not a clear product mentioned and just generic terms are used, return 'None'. If multiple "
        "products are included, tell me the product names for each of the products. If the product is a lens, "
        "add the company of the camera to the end of the product name that is outputted. If the product is a "
        "lens, include the aperture in the product name. Only provide a list of the product(s) name(s). Either "
        "return the product names or 'None'. Do not write any context This is the product information:\n\nTitle:\n"
    )

    # title = "Sony 4k24 FHD120 Creator Bundle a6600"
    title = _title

    # description = (
    #     "a6600 Body With Lens Cap - Very Low Shutter Count. Used for Video."
    #     "Tamron 17-28mm Diii"
    #     "Saramonic Wireless Lav Kit 2 Transmitters 1 Receiver"
    #     "Smallrig a6600 Cage"
    #     "Pelican Travel Case"
    #     "Sony Shooting Grip with Case - GP- VPT2BT"
    #     "Lumecube Panel GO"
    #     "SunPak Tripod"
    #     "Peak Design Camera Strap"
    # )
    description = _description

    total_prompt = prompt + title + "\n\nDescription:\n" + description

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": total_prompt},
        ],
    )

    items = completion.choices[0].message.content

    my_array = items.splitlines()
    # print("finished gptcheck()")
    return my_array


# handler
def handler(signum, frame):
    # Raise an exception if the function takes too long
    raise TimeoutError("Function timed out")


# tries to check with ChatGPT multiple times if it does not initially work
def get_products(_title, _description):
    while True:
        try:
            # Set a timeout for the check() function
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(90)
            result = get_products_basic(_title, _description)
            return result
            # If check() succeeds, break out of the loop
            # break
        except TimeoutError:
            print("Function timed out. Retrying...")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Reset the alarm
            signal.alarm(0)

    # Optionally, you can reset the alarm outside the loop to ensure it's cleared
    signal.alarm(0)


# Example Call

# title = """Sony Playstation 4 Pro / PS4 Pro (Star Wars Edition) 1tb Model bundle"""

# description = """Sony Playstation 4 Pro / PS4 Pro (Star Wars Edition) 1tb Model

# Includes power cord, hdmi, 1 dualshock 4 controller, 1 turtle beach stealth pro wireless headset w/ charging cable and usb receiver"""

# print(get_products(title, description))
