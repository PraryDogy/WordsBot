from . import clipboard, re, types

__all__ = (
    "msg_file_id"
    )


def get_file_id(message):
    reg = r'"file_id": "\S*"'
    res = re.findall(reg, str(message))
    file_id = res[-1].split(' ')[-1].strip('"')
    clipboard.copy(file_id)
    return file_id


async def msg_file_id(message: types.Message):
    try:
        print(get_file_id(message))
    except Exception:
        print('no file id')