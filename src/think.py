import aiohttp
import keys

from conf import prompt_max_tokens, response_max_tokens
from conversation import Speaker


async def think(convo):
    await convo.remove_in_excess(prompt_max_tokens)
    await convo.save()
    print("Getting completion")
    prompt = convo.as_prompt()
    print("=========")
    print(prompt)
    print("=========")
    print(f"Num tokens according to us: {convo.num_tokens}")
    print("=========")

    while True:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {keys.API_KEY}"},
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": prompt,
                    "max_tokens": response_max_tokens,
                    "n": 1,
                    "stop": None,
                    "temperature": 0.7,
                },
            ) as resp:
                response = await resp.json()
                print("response:")
                print(response)
                r = response["choices"][0]["message"]["content"]
                if r:
                    convo.add_entry(r, Speaker.openai)
                    await convo.save()
                    break
                else:
                    print("Did not get a response. Try again?")
                    if input("y/n: ").strip() == "y":
                        pass
                    else:
                        break
