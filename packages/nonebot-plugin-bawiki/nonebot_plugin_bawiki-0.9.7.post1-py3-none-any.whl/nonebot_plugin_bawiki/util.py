import asyncio
import datetime
import json
from dataclasses import dataclass
from io import BytesIO
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    TypeVar,
    Union,
    overload,
)

from httpx import AsyncClient
from nonebot import logger
from nonebot.adapters.onebot.v11 import Message
from nonebot_plugin_apscheduler import scheduler
from PIL import Image, ImageOps

from .config import config

T = TypeVar("T")
NestedIterable = Iterable[Union[T, Iterable["NestedIterable[T]"]]]

req_cache: List["RequestCache"] = []


@dataclass
class RequestCache:
    url: str
    method: str
    raw: bool
    json: bool
    params: str
    content: Union[Any, None]


async def get_req_cache(
    url: str,
    method: Optional[str] = None,
    raw: Optional[bool] = None,
    json: Optional[bool] = None,
    params: Optional[str] = None,
) -> Optional[Any]:
    cache = next(
        (
            c
            for c in req_cache
            if (
                c.url == url
                and c.method == method
                and c.raw == raw
                and c.json == json
                and c.params == params
            )
        ),
        None,
    )
    if cache:
        while cache.content is None:
            logger.debug(f"Waiting for cache {url}")
            await asyncio.sleep(0.1)
        if isinstance(cache.content, Exception):
            logger.debug(f"Cache for {url} got exception: {cache.content!r}")
            return None
        # if cache.content is not None:
        return cache.content
    return None


def clear_req_cache() -> int:
    count = len(req_cache)
    req_cache.clear()
    return count


if config.ba_clear_req_cache_interval > 0:

    @scheduler.scheduled_job("interval", hours=config.ba_clear_req_cache_interval)
    async def _():
        clear_req_cache()


@overload
async def async_req(
    url,
    *,
    is_json: Literal[True] = True,
    raw: Literal[False] = False,
    ignore_cache: bool = False,
    proxy: Optional[str] = config.ba_proxy,
    method: str = "GET",
    params: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> Any:
    ...


@overload
async def async_req(
    url,
    *,
    is_json: Literal[False] = False,
    raw: Literal[True] = True,
    ignore_cache: bool = False,
    proxy: Optional[str] = config.ba_proxy,
    method: str = "GET",
    params: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> bytes:
    ...


@overload
async def async_req(
    url,
    *,
    is_json: Literal[False] = False,
    raw: Literal[False] = False,
    ignore_cache: bool = False,
    proxy: Optional[str] = config.ba_proxy,
    method: str = "GET",
    params: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> str:
    ...


async def async_req(
    url,
    is_json=True,
    raw=False,
    ignore_cache=False,
    proxy=config.ba_proxy,
    method="GET",
    params=None,
    **kwargs,
):
    param_json = json.dumps(params) if params else "{}"

    if (not ignore_cache) and (
        c := await get_req_cache(url, method, raw, is_json, param_json)
    ):
        return c

    cache_obj = RequestCache(url, method, raw, is_json, param_json, None)
    req_cache.append(cache_obj)

    logger.debug(f"Requesting {url}")
    try:
        async with AsyncClient(proxies=proxy) as cli:
            resp = await cli.request(method, url, params=params, **kwargs)
            resp.raise_for_status()

            if (not raw) and is_json:
                ret = resp.json()
            elif raw:
                ret = resp.content
            else:
                ret = resp.text

            cache_obj.content = ret
            return ret

    except Exception as e:
        cache_obj.content = e
        req_cache.remove(cache_obj)
        raise


def format_timestamp(t: int):
    return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S")


def recover_alia(origin: str, alia_dict: Dict[str, List[str]]):
    origin = replace_brackets(origin).strip()
    origin_ = origin.lower()

    # 精确匹配
    for k, li in alia_dict.items():
        if origin_ in li or origin_ == k:
            return k

    # 没找到，模糊匹配
    origin_ = origin.replace(" ", "")
    for k, li in alia_dict.items():
        li = [x.replace(" ", "") for x in ([k, *li])]
        for v in li:
            if origin_ in v:
                return k

    return origin


def parse_time_delta(t: datetime.timedelta):
    mm, ss = divmod(t.seconds, 60)
    hh, mm = divmod(mm, 60)
    dd = t.days or 0
    return dd, hh, mm, ss


def img_invert_rgba(im: Image.Image):
    # https://stackoverflow.com/questions/2498875/how-to-invert-colors-of-image-with-pil-python-imaging
    r, g, b, a = im.split()
    rgb_image = Image.merge("RGB", (r, g, b))
    inverted_image = ImageOps.invert(rgb_image)
    r2, g2, b2 = inverted_image.split()
    return Image.merge("RGBA", (r2, g2, b2, a))


def replace_brackets(original: str):
    return original.replace("（", "(").replace("）", "(")


def splice_msg(msgs: list) -> Message:
    im = Message()
    for i, v in enumerate(msgs):
        if isinstance(v, str) and (i != 0):
            v = f"\n{v}"
        im += v
    return im


def split_list(li: Iterable[T], length: int) -> List[List[T]]:
    latest = []
    tmp = []
    for n, i in enumerate(li):
        tmp.append(i)
        if (n + 1) % length == 0:
            latest.append(tmp)
            tmp = []
    if tmp:
        latest.append(tmp)
    return latest


def split_pic(pic: Image.Image, max_height: int = 4096) -> List[Image.Image]:
    pw, ph = pic.size
    if ph <= max_height:
        return [pic]

    ret = []
    need_merge_last = ph % max_height < max_height // 2
    iter_times = ph // max_height

    now_h = 0
    for i in range(iter_times):
        if i == iter_times - 1 and need_merge_last:
            ret.append(pic.crop((0, now_h, pw, ph)))
            break

        ret.append(pic.crop((0, now_h, pw, now_h + max_height)))
        now_h += max_height

    return ret


def i2b(image: Image.Image, img_format: str = "JPEG") -> BytesIO:
    buf = BytesIO()
    image.save(buf, img_format)
    buf.seek(0)
    return buf
