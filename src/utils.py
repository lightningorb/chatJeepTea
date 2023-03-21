def split_message(msg, limit=4096):
    words, chunks, curr = msg.split(), [], []
    for w in words:
        if len(" ".join(curr) + " " + w) > limit:
            chunks.append(" ".join(curr))
            curr = [w]
        else:
            curr.append(w)
    chunks.append(" ".join(curr))
    return chunks


async def reply_text(message, text):
    for chunk in split_message(text):
        await message.reply_text(chunk)
