# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1lll1_opy_ = 2048
bstack11l1111_opy_ = 7
def bstack11ll11_opy_ (bstack1l11_opy_):
    global bstack11lll1l_opy_
    bstack1l1ll1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11_opy_ [:-1]
    bstack11l1lll_opy_ = bstack1l1ll1_opy_ % len (bstack111l1ll_opy_)
    bstack111lll1_opy_ = bstack111l1ll_opy_ [:bstack11l1lll_opy_] + bstack111l1ll_opy_ [bstack11l1lll_opy_:]
    if bstack1l1l11l_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1_opy_ - (bstack11lll1_opy_ + bstack1l1ll1_opy_) % bstack11l1111_opy_) for bstack11lll1_opy_, char in enumerate (bstack111lll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1lll1_opy_ - (bstack11lll1_opy_ + bstack1l1ll1_opy_) % bstack11l1111_opy_) for bstack11lll1_opy_, char in enumerate (bstack111lll1_opy_)])
    return eval (bstack111l111_opy_)
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from bstack_utils.constants import *
import time
import requests
def bstack1ll1ll11l1_opy_():
  global CONFIG
  headers = {
        bstack11ll11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡵ"): bstack11ll11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡶ"),
      }
  proxies = bstack11ll1l111_opy_(CONFIG, bstack1l1ll1l1l_opy_)
  try:
    response = requests.get(bstack1l1ll1l1l_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l1l11ll1_opy_ = response.json()[bstack11ll11_opy_ (u"ࠫ࡭ࡻࡢࡴࠩࡷ")]
      logger.debug(bstack111ll111_opy_.format(response.json()))
      return bstack1l1l11ll1_opy_
    else:
      logger.debug(bstack1l111lll_opy_.format(bstack11ll11_opy_ (u"ࠧࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡋࡕࡒࡒࠥࡶࡡࡳࡵࡨࠤࡪࡸࡲࡰࡴࠣࠦࡸ")))
  except Exception as e:
    logger.debug(bstack1l111lll_opy_.format(e))
def bstack111lllll1_opy_(hub_url):
  global CONFIG
  url = bstack11ll11_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣࡹ")+  hub_url + bstack11ll11_opy_ (u"ࠢ࠰ࡥ࡫ࡩࡨࡱࠢࡺ")
  headers = {
        bstack11ll11_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧࡻ"): bstack11ll11_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬࡼ"),
      }
  proxies = bstack11ll1l111_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1llll1ll1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack111lll11_opy_.format(hub_url, e))
def bstack1l1lll11_opy_():
  try:
    global bstack1llll1l11l_opy_
    bstack1l1l11ll1_opy_ = bstack1ll1ll11l1_opy_()
    bstack1ll11111_opy_ = []
    results = []
    for bstack111l1l1l_opy_ in bstack1l1l11ll1_opy_:
      bstack1ll11111_opy_.append(bstack111lllll_opy_(target=bstack111lllll1_opy_,args=(bstack111l1l1l_opy_,)))
    for t in bstack1ll11111_opy_:
      t.start()
    for t in bstack1ll11111_opy_:
      results.append(t.join())
    bstack11lll11ll_opy_ = {}
    for item in results:
      hub_url = item[bstack11ll11_opy_ (u"ࠪ࡬ࡺࡨ࡟ࡶࡴ࡯ࠫࡽ")]
      latency = item[bstack11ll11_opy_ (u"ࠫࡱࡧࡴࡦࡰࡦࡽࠬࡾ")]
      bstack11lll11ll_opy_[hub_url] = latency
    bstack111lll111_opy_ = min(bstack11lll11ll_opy_, key= lambda x: bstack11lll11ll_opy_[x])
    bstack1llll1l11l_opy_ = bstack111lll111_opy_
    logger.debug(bstack11l1l111l_opy_.format(bstack111lll111_opy_))
  except Exception as e:
    logger.debug(bstack1llll11l_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils.config import Config
from bstack_utils.helper import bstack1l1l1ll1_opy_, bstack11lll1ll1_opy_, bstack1l1ll1l1_opy_, Notset, bstack1ll11ll11_opy_, \
  bstack1ll1ll111_opy_, bstack1l1l111l1_opy_, bstack11l1111l1_opy_, bstack111l11l1l_opy_, bstack1l1lllll1_opy_
from bstack_utils.bstack1lllll111l_opy_ import bstack1llll1111_opy_
from bstack_utils.proxy import bstack1ll1lll1ll_opy_, bstack11ll1l111_opy_, bstack111l11111_opy_, bstack1l1llll11_opy_
from browserstack_sdk.bstack1111llll1_opy_ import *
from browserstack_sdk.bstack1111l1l11_opy_ import *
bstack1l1ll111l_opy_ = bstack11ll11_opy_ (u"ࠬࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠥࠦࡩࡧࠪࡳࡥ࡬࡫ࠠ࠾࠿ࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠥࢁ࡜࡯ࠢࠣࠤࡹࡸࡹࡼ࡞ࡱࠤࡨࡵ࡮ࡴࡶࠣࡪࡸࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪ࡟ࠫ࡫ࡹ࡜ࠨࠫ࠾ࡠࡳࠦࠠࠡࠢࠣࡪࡸ࠴ࡡࡱࡲࡨࡲࡩࡌࡩ࡭ࡧࡖࡽࡳࡩࠨࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷ࡬࠱ࠦࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡱࡡ࡬ࡲࡩ࡫ࡸࠪࠢ࠮ࠤࠧࡀࠢࠡ࠭ࠣࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࠪࡤࡻࡦ࡯ࡴࠡࡰࡨࡻࡕࡧࡧࡦ࠴࠱ࡩࡻࡧ࡬ࡶࡣࡷࡩ࠭ࠨࠨࠪࠢࡀࡂࠥࢁࡽࠣ࠮ࠣࡠࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠤࢀࡠࠬ࠯ࠩࠪ࡝ࠥ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩࠨ࡝ࠪࠢ࠮ࠤࠧ࠲࡜࡝ࡰࠥ࠭ࡡࡴࠠࠡࠢࠣࢁࡨࡧࡴࡤࡪࠫࡩࡽ࠯ࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࢂࡢ࡮ࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠬࡿ")
bstack111l111l1_opy_ = bstack11ll11_opy_ (u"࠭࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸ࡣ࡜࡯ࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࡟ࡲࡨࡵ࡮ࡴࡶࠣࡴࡤ࡯࡮ࡥࡧࡻࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠲࡞࡞ࡱࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳ࠪ࡞ࡱࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࡠࡳ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬ࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨ࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࡢ࡮࡭ࡧࡷࠤࡨࡧࡰࡴ࠽࡟ࡲࡹࡸࡹࠡࡽ࡟ࡲࡨࡧࡰࡴࠢࡀࠤࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸ࠯࡜࡯ࠢࠣࢁࠥࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࠡࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻ࡝ࡰࠣࠤࠥࠦࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ࠽ࠤࡥࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠤࡼࡧࡱࡧࡴࡪࡥࡖࡔࡌࡇࡴࡳࡰࡰࡰࡨࡲࡹ࠮ࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡤࡣࡳࡷ࠮࠯ࡽࡡ࠮࡟ࡲࠥࠦࠠࠡ࠰࠱࠲ࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶࡠࡳࠦࠠࡾࠫ࡟ࡲࢂࡢ࡮࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠬࢀ")
from ._version import __version__
bstack1lllll11ll_opy_ = None
CONFIG = {}
bstack1ll1lll1_opy_ = {}
bstack1ll11ll1l_opy_ = {}
bstack1l11ll1l_opy_ = None
bstack1ll1l1l11l_opy_ = None
bstack1l11lll11_opy_ = None
bstack1lll1111ll_opy_ = -1
bstack1llll1ll_opy_ = bstack11l11l111_opy_
bstack1ll1l1lll_opy_ = 1
bstack1ll111ll_opy_ = False
bstack1l111111_opy_ = False
bstack1llll1111l_opy_ = bstack11ll11_opy_ (u"ࠧࠨࢁ")
bstack11l1l11ll_opy_ = bstack11ll11_opy_ (u"ࠨࠩࢂ")
bstack1l11111l1_opy_ = False
bstack1llllll11l_opy_ = True
bstack1ll1l11l1l_opy_ = bstack11ll11_opy_ (u"ࠩࠪࢃ")
bstack1llll11l1_opy_ = []
bstack1llll1l11l_opy_ = bstack11ll11_opy_ (u"ࠪࠫࢄ")
bstack1l1l1ll1l_opy_ = False
bstack1llllll1l1_opy_ = None
bstack1lll111l1_opy_ = None
bstack1lll1ll11_opy_ = -1
bstack1lll1l1l11_opy_ = os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"ࠫࢃ࠭ࢅ")), bstack11ll11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬࢆ"), bstack11ll11_opy_ (u"࠭࠮ࡳࡱࡥࡳࡹ࠳ࡲࡦࡲࡲࡶࡹ࠳ࡨࡦ࡮ࡳࡩࡷ࠴ࡪࡴࡱࡱࠫࢇ"))
bstack1llll11ll_opy_ = []
bstack1lllllll11_opy_ = []
bstack11l111lll_opy_ = False
bstack11ll11111_opy_ = False
bstack111l1ll11_opy_ = None
bstack11ll11l1_opy_ = None
bstack1lll1l1111_opy_ = None
bstack1lll11ll_opy_ = None
bstack1lll1ll111_opy_ = None
bstack11ll1l1ll_opy_ = None
bstack11l1l1lll_opy_ = None
bstack11lllll1l_opy_ = None
bstack1ll11l1l1_opy_ = None
bstack1l1ll1l11_opy_ = None
bstack11ll111l1_opy_ = None
bstack11l111ll1_opy_ = None
bstack11111ll1l_opy_ = None
bstack11llll1ll_opy_ = None
bstack1l1111lll_opy_ = None
bstack111llll11_opy_ = None
bstack1l1lll1ll_opy_ = None
bstack1l1ll111_opy_ = None
bstack1lll111l_opy_ = bstack11ll11_opy_ (u"ࠢࠣ࢈")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1llll1ll_opy_,
                    format=bstack11ll11_opy_ (u"ࠨ࡞ࡱࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ࢉ"),
                    datefmt=bstack11ll11_opy_ (u"ࠩࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫࢊ"),
                    stream=sys.stdout)
bstack1ll1l1lll1_opy_ = Config.get_instance()
def bstack1l1llllll_opy_():
  global CONFIG
  global bstack1llll1ll_opy_
  if bstack11ll11_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬࢋ") in CONFIG:
    bstack1llll1ll_opy_ = bstack1l1111l11_opy_[CONFIG[bstack11ll11_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ࢌ")]]
    logging.getLogger().setLevel(bstack1llll1ll_opy_)
def bstack1ll11l1ll_opy_():
  global CONFIG
  global bstack11l111lll_opy_
  bstack11l1l1ll1_opy_ = bstack1l11l1111_opy_(CONFIG)
  if (bstack11ll11_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࢍ") in bstack11l1l1ll1_opy_ and str(bstack11l1l1ll1_opy_[bstack11ll11_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࢎ")]).lower() == bstack11ll11_opy_ (u"ࠧࡵࡴࡸࡩࠬ࢏")):
    bstack11l111lll_opy_ = True
def bstack1111l11l1_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack11l1llll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1l11111_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack11ll11_opy_ (u"ࠣ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡥࡲࡲ࡫࡯ࡧࡧ࡫࡯ࡩࠧ࢐") == args[i].lower() or bstack11ll11_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡦࡪࡩࠥ࢑") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1ll1l11l1l_opy_
      bstack1ll1l11l1l_opy_ += bstack11ll11_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠠࠨ࢒") + path
      return path
  return None
bstack1lll1l11ll_opy_ = re.compile(bstack11ll11_opy_ (u"ࡶࠧ࠴ࠪࡀ࡞ࠧࡿ࠭࠴ࠪࡀࠫࢀ࠲࠯ࡅࠢ࢓"))
def bstack111ll1lll_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1lll1l11ll_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack11ll11_opy_ (u"ࠧࠪࡻࠣ࢔") + group + bstack11ll11_opy_ (u"ࠨࡽࠣ࢕"), os.environ.get(group))
  return value
def bstack1111llll_opy_():
  bstack11l11111l_opy_ = bstack1l1l11111_opy_()
  if bstack11l11111l_opy_ and os.path.exists(os.path.abspath(bstack11l11111l_opy_)):
    fileName = bstack11l11111l_opy_
  if bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢖") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࢗ")])) and not bstack11ll11_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫ࢘") in locals():
    fileName = os.environ[bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋ࢙ࠧ")]
  if bstack11ll11_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࢚࠭") in locals():
    bstack11l1l1l_opy_ = os.path.abspath(fileName)
  else:
    bstack11l1l1l_opy_ = bstack11ll11_opy_ (u"࢛ࠬ࠭")
  bstack1ll1ll1l1l_opy_ = os.getcwd()
  bstack1lll11111_opy_ = bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ࢜")
  bstack1llll1l1_opy_ = bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹࡢ࡯࡯ࠫ࢝")
  while (not os.path.exists(bstack11l1l1l_opy_)) and bstack1ll1ll1l1l_opy_ != bstack11ll11_opy_ (u"ࠣࠤ࢞"):
    bstack11l1l1l_opy_ = os.path.join(bstack1ll1ll1l1l_opy_, bstack1lll11111_opy_)
    if not os.path.exists(bstack11l1l1l_opy_):
      bstack11l1l1l_opy_ = os.path.join(bstack1ll1ll1l1l_opy_, bstack1llll1l1_opy_)
    if bstack1ll1ll1l1l_opy_ != os.path.dirname(bstack1ll1ll1l1l_opy_):
      bstack1ll1ll1l1l_opy_ = os.path.dirname(bstack1ll1ll1l1l_opy_)
    else:
      bstack1ll1ll1l1l_opy_ = bstack11ll11_opy_ (u"ࠤࠥ࢟")
  if not os.path.exists(bstack11l1l1l_opy_):
    bstack11ll11ll_opy_(
      bstack11l11l11_opy_.format(os.getcwd()))
  try:
    with open(bstack11l1l1l_opy_, bstack11ll11_opy_ (u"ࠪࡶࠬࢠ")) as stream:
      yaml.add_implicit_resolver(bstack11ll11_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࢡ"), bstack1lll1l11ll_opy_)
      yaml.add_constructor(bstack11ll11_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࢢ"), bstack111ll1lll_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack11l1l1l_opy_, bstack11ll11_opy_ (u"࠭ࡲࠨࢣ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack11ll11ll_opy_(bstack1llll1l111_opy_.format(str(exc)))
def bstack1llllllll1_opy_(config):
  bstack11l1lll1l_opy_ = bstack1lll1llll1_opy_(config)
  for option in list(bstack11l1lll1l_opy_):
    if option.lower() in bstack1ll11lll1_opy_ and option != bstack1ll11lll1_opy_[option.lower()]:
      bstack11l1lll1l_opy_[bstack1ll11lll1_opy_[option.lower()]] = bstack11l1lll1l_opy_[option]
      del bstack11l1lll1l_opy_[option]
  return config
def bstack1l1l1111_opy_():
  global bstack1ll11ll1l_opy_
  for key, bstack111l1111l_opy_ in bstack11l111l11_opy_.items():
    if isinstance(bstack111l1111l_opy_, list):
      for var in bstack111l1111l_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1ll11ll1l_opy_[key] = os.environ[var]
          break
    elif bstack111l1111l_opy_ in os.environ and os.environ[bstack111l1111l_opy_] and str(os.environ[bstack111l1111l_opy_]).strip():
      bstack1ll11ll1l_opy_[key] = os.environ[bstack111l1111l_opy_]
  if bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩࢤ") in os.environ:
    bstack1ll11ll1l_opy_[bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢥ")] = {}
    bstack1ll11ll1l_opy_[bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")][bstack11ll11_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢧ")] = os.environ[bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ")]
def bstack11ll1ll1l_opy_():
  global bstack1ll1lll1_opy_
  global bstack1ll1l11l1l_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack11ll11_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࢩ").lower() == val.lower():
      bstack1ll1lll1_opy_[bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")] = {}
      bstack1ll1lll1_opy_[bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢫ")][bstack11ll11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢬ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1ll1l1ll11_opy_ in bstack111l1l111_opy_.items():
    if isinstance(bstack1ll1l1ll11_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1ll1l1ll11_opy_:
          if idx < len(sys.argv) and bstack11ll11_opy_ (u"ࠩ࠰࠱ࠬࢭ") + var.lower() == val.lower() and not key in bstack1ll1lll1_opy_:
            bstack1ll1lll1_opy_[key] = sys.argv[idx + 1]
            bstack1ll1l11l1l_opy_ += bstack11ll11_opy_ (u"ࠪࠤ࠲࠳ࠧࢮ") + var + bstack11ll11_opy_ (u"ࠫࠥ࠭ࢯ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack11ll11_opy_ (u"ࠬ࠳࠭ࠨࢰ") + bstack1ll1l1ll11_opy_.lower() == val.lower() and not key in bstack1ll1lll1_opy_:
          bstack1ll1lll1_opy_[key] = sys.argv[idx + 1]
          bstack1ll1l11l1l_opy_ += bstack11ll11_opy_ (u"࠭ࠠ࠮࠯ࠪࢱ") + bstack1ll1l1ll11_opy_ + bstack11ll11_opy_ (u"ࠧࠡࠩࢲ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1llll111_opy_(config):
  bstack1llll11l11_opy_ = config.keys()
  for bstack1111l1l1_opy_, bstack1lllll11l1_opy_ in bstack111lll1l1_opy_.items():
    if bstack1lllll11l1_opy_ in bstack1llll11l11_opy_:
      config[bstack1111l1l1_opy_] = config[bstack1lllll11l1_opy_]
      del config[bstack1lllll11l1_opy_]
  for bstack1111l1l1_opy_, bstack1lllll11l1_opy_ in bstack111111l11_opy_.items():
    if isinstance(bstack1lllll11l1_opy_, list):
      for bstack1lllll1lll_opy_ in bstack1lllll11l1_opy_:
        if bstack1lllll1lll_opy_ in bstack1llll11l11_opy_:
          config[bstack1111l1l1_opy_] = config[bstack1lllll1lll_opy_]
          del config[bstack1lllll1lll_opy_]
          break
    elif bstack1lllll11l1_opy_ in bstack1llll11l11_opy_:
      config[bstack1111l1l1_opy_] = config[bstack1lllll11l1_opy_]
      del config[bstack1lllll11l1_opy_]
  for bstack1lllll1lll_opy_ in list(config):
    for bstack111l1lll_opy_ in bstack1l1ll1111_opy_:
      if bstack1lllll1lll_opy_.lower() == bstack111l1lll_opy_.lower() and bstack1lllll1lll_opy_ != bstack111l1lll_opy_:
        config[bstack111l1lll_opy_] = config[bstack1lllll1lll_opy_]
        del config[bstack1lllll1lll_opy_]
  bstack1ll11ll1_opy_ = []
  if bstack11ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫࢳ") in config:
    bstack1ll11ll1_opy_ = config[bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢴ")]
  for platform in bstack1ll11ll1_opy_:
    for bstack1lllll1lll_opy_ in list(platform):
      for bstack111l1lll_opy_ in bstack1l1ll1111_opy_:
        if bstack1lllll1lll_opy_.lower() == bstack111l1lll_opy_.lower() and bstack1lllll1lll_opy_ != bstack111l1lll_opy_:
          platform[bstack111l1lll_opy_] = platform[bstack1lllll1lll_opy_]
          del platform[bstack1lllll1lll_opy_]
  for bstack1111l1l1_opy_, bstack1lllll11l1_opy_ in bstack111111l11_opy_.items():
    for platform in bstack1ll11ll1_opy_:
      if isinstance(bstack1lllll11l1_opy_, list):
        for bstack1lllll1lll_opy_ in bstack1lllll11l1_opy_:
          if bstack1lllll1lll_opy_ in platform:
            platform[bstack1111l1l1_opy_] = platform[bstack1lllll1lll_opy_]
            del platform[bstack1lllll1lll_opy_]
            break
      elif bstack1lllll11l1_opy_ in platform:
        platform[bstack1111l1l1_opy_] = platform[bstack1lllll11l1_opy_]
        del platform[bstack1lllll11l1_opy_]
  for bstack1lll11l1l_opy_ in bstack1l1lll1l_opy_:
    if bstack1lll11l1l_opy_ in config:
      if not bstack1l1lll1l_opy_[bstack1lll11l1l_opy_] in config:
        config[bstack1l1lll1l_opy_[bstack1lll11l1l_opy_]] = {}
      config[bstack1l1lll1l_opy_[bstack1lll11l1l_opy_]].update(config[bstack1lll11l1l_opy_])
      del config[bstack1lll11l1l_opy_]
  for platform in bstack1ll11ll1_opy_:
    for bstack1lll11l1l_opy_ in bstack1l1lll1l_opy_:
      if bstack1lll11l1l_opy_ in list(platform):
        if not bstack1l1lll1l_opy_[bstack1lll11l1l_opy_] in platform:
          platform[bstack1l1lll1l_opy_[bstack1lll11l1l_opy_]] = {}
        platform[bstack1l1lll1l_opy_[bstack1lll11l1l_opy_]].update(platform[bstack1lll11l1l_opy_])
        del platform[bstack1lll11l1l_opy_]
  config = bstack1llllllll1_opy_(config)
  return config
def bstack1ll1llll1l_opy_(config):
  global bstack11l1l11ll_opy_
  if bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࢵ") in config and str(config[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࢶ")]).lower() != bstack11ll11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫࢷ"):
    if not bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢸ") in config:
      config[bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢹ")] = {}
    if not bstack11ll11_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢺ") in config[bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢻ")]:
      bstack1l111l1l1_opy_ = datetime.datetime.now()
      bstack1l1l11l1_opy_ = bstack1l111l1l1_opy_.strftime(bstack11ll11_opy_ (u"ࠪࠩࡩࡥࠥࡣࡡࠨࡌࠪࡓࠧࢼ"))
      hostname = socket.gethostname()
      bstack1llll1ll11_opy_ = bstack11ll11_opy_ (u"ࠫࠬࢽ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11ll11_opy_ (u"ࠬࢁࡽࡠࡽࢀࡣࢀࢃࠧࢾ").format(bstack1l1l11l1_opy_, hostname, bstack1llll1ll11_opy_)
      config[bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢿ")][bstack11ll11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣀ")] = identifier
    bstack11l1l11ll_opy_ = config[bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࣁ")][bstack11ll11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣂ")]
  return config
def bstack1lll1l1ll_opy_():
  bstack1lll111ll_opy_ =  bstack111l11l1l_opy_()[bstack11ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠩࣃ")]
  return bstack1lll111ll_opy_ if bstack1lll111ll_opy_ else -1
def bstack11l1l1ll_opy_(bstack1lll111ll_opy_):
  global CONFIG
  if not bstack11ll11_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣄ") in CONFIG[bstack11ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣅ")]:
    return
  CONFIG[bstack11ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣆ")] = CONFIG[bstack11ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣇ")].replace(
    bstack11ll11_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣈ"),
    str(bstack1lll111ll_opy_)
  )
def bstack1l1l1llll_opy_():
  global CONFIG
  if not bstack11ll11_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨࣉ") in CONFIG[bstack11ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")]:
    return
  bstack1l111l1l1_opy_ = datetime.datetime.now()
  bstack1l1l11l1_opy_ = bstack1l111l1l1_opy_.strftime(bstack11ll11_opy_ (u"ࠫࠪࡪ࠭ࠦࡤ࠰ࠩࡍࡀࠥࡎࠩ࣋"))
  CONFIG[bstack11ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ࣌")] = CONFIG[bstack11ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣍")].replace(
    bstack11ll11_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭࣎"),
    bstack1l1l11l1_opy_
  )
def bstack11l1l111_opy_():
  global CONFIG
  if bstack11ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ࣏ࠪ") in CONFIG and not bool(CONFIG[bstack11ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")]):
    del CONFIG[bstack11ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣑ࠬ")]
    return
  if not bstack11ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࣒࠭") in CONFIG:
    CONFIG[bstack11ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ")] = bstack11ll11_opy_ (u"࠭ࠣࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣔ")
  if bstack11ll11_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭ࣕ") in CONFIG[bstack11ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ")]:
    bstack1l1l1llll_opy_()
    os.environ[bstack11ll11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ࣗ")] = CONFIG[bstack11ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣘ")]
  if not bstack11ll11_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣙ") in CONFIG[bstack11ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣚ")]:
    return
  bstack1lll111ll_opy_ = bstack11ll11_opy_ (u"࠭ࠧࣛ")
  bstack1ll1llllll_opy_ = bstack1lll1l1ll_opy_()
  if bstack1ll1llllll_opy_ != -1:
    bstack1lll111ll_opy_ = bstack11ll11_opy_ (u"ࠧࡄࡋࠣࠫࣜ") + str(bstack1ll1llllll_opy_)
  if bstack1lll111ll_opy_ == bstack11ll11_opy_ (u"ࠨࠩࣝ"):
    bstack11ll11l11_opy_ = bstack111ll1ll1_opy_(CONFIG[bstack11ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬࣞ")])
    if bstack11ll11l11_opy_ != -1:
      bstack1lll111ll_opy_ = str(bstack11ll11l11_opy_)
  if bstack1lll111ll_opy_:
    bstack11l1l1ll_opy_(bstack1lll111ll_opy_)
    os.environ[bstack11ll11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧࣟ")] = CONFIG[bstack11ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣠")]
def bstack11l11l1l1_opy_(bstack11llll1l_opy_, bstack1lll1ll11l_opy_, path):
  bstack1l1llll1_opy_ = {
    bstack11ll11_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣡"): bstack1lll1ll11l_opy_
  }
  if os.path.exists(path):
    bstack1111l111l_opy_ = json.load(open(path, bstack11ll11_opy_ (u"࠭ࡲࡣࠩ࣢")))
  else:
    bstack1111l111l_opy_ = {}
  bstack1111l111l_opy_[bstack11llll1l_opy_] = bstack1l1llll1_opy_
  with open(path, bstack11ll11_opy_ (u"ࠢࡸࣣ࠭ࠥ")) as outfile:
    json.dump(bstack1111l111l_opy_, outfile)
def bstack111ll1ll1_opy_(bstack11llll1l_opy_):
  bstack11llll1l_opy_ = str(bstack11llll1l_opy_)
  bstack1llll1l1ll_opy_ = os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"ࠨࢀࠪࣤ")), bstack11ll11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩࣥ"))
  try:
    if not os.path.exists(bstack1llll1l1ll_opy_):
      os.makedirs(bstack1llll1l1ll_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"ࠪࢂࣦࠬ")), bstack11ll11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫࣧ"), bstack11ll11_opy_ (u"ࠬ࠴ࡢࡶ࡫࡯ࡨ࠲ࡴࡡ࡮ࡧ࠰ࡧࡦࡩࡨࡦ࠰࡭ࡷࡴࡴࠧࣨ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11ll11_opy_ (u"࠭ࡷࠨࣩ")):
        pass
      with open(file_path, bstack11ll11_opy_ (u"ࠢࡸ࠭ࠥ࣪")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11ll11_opy_ (u"ࠨࡴࠪ࣫")) as bstack1l1l11lll_opy_:
      bstack111l1l1l1_opy_ = json.load(bstack1l1l11lll_opy_)
    if bstack11llll1l_opy_ in bstack111l1l1l1_opy_:
      bstack11111111_opy_ = bstack111l1l1l1_opy_[bstack11llll1l_opy_][bstack11ll11_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣬")]
      bstack1l1111111_opy_ = int(bstack11111111_opy_) + 1
      bstack11l11l1l1_opy_(bstack11llll1l_opy_, bstack1l1111111_opy_, file_path)
      return bstack1l1111111_opy_
    else:
      bstack11l11l1l1_opy_(bstack11llll1l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack11l1l1111_opy_.format(str(e)))
    return -1
def bstack11l1ll1ll_opy_(config):
  if not config[bstack11ll11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩ࣭ࠬ")] or not config[bstack11ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿ࣮ࠧ")]:
    return True
  else:
    return False
def bstack11l1l1l1_opy_(config, index=0):
  global bstack1l11111l1_opy_
  bstack111l1llll_opy_ = {}
  caps = bstack1lll1111l1_opy_ + bstack11ll11lll_opy_
  if bstack1l11111l1_opy_:
    caps += bstack1111ll11_opy_
  for key in config:
    if key in caps + [bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ࣯")]:
      continue
    bstack111l1llll_opy_[key] = config[key]
  if bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࣰࠩ") in config:
    for bstack1llll11111_opy_ in config[bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࣱࠪ")][index]:
      if bstack1llll11111_opy_ in caps + [bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࣲ࠭"), bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪࣳ")]:
        continue
      bstack111l1llll_opy_[bstack1llll11111_opy_] = config[bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ")][index][bstack1llll11111_opy_]
  bstack111l1llll_opy_[bstack11ll11_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ࣵ")] = socket.gethostname()
  if bstack11ll11_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࣶ࠭") in bstack111l1llll_opy_:
    del (bstack111l1llll_opy_[bstack11ll11_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧࣷ")])
  return bstack111l1llll_opy_
def bstack1llll1l1l_opy_(config):
  global bstack1l11111l1_opy_
  bstack111ll1ll_opy_ = {}
  caps = bstack11ll11lll_opy_
  if bstack1l11111l1_opy_:
    caps += bstack1111ll11_opy_
  for key in caps:
    if key in config:
      bstack111ll1ll_opy_[key] = config[key]
  return bstack111ll1ll_opy_
def bstack1ll1111l_opy_(bstack111l1llll_opy_, bstack111ll1ll_opy_):
  bstack1l11l1ll1_opy_ = {}
  for key in bstack111l1llll_opy_.keys():
    if key in bstack111lll1l1_opy_:
      bstack1l11l1ll1_opy_[bstack111lll1l1_opy_[key]] = bstack111l1llll_opy_[key]
    else:
      bstack1l11l1ll1_opy_[key] = bstack111l1llll_opy_[key]
  for key in bstack111ll1ll_opy_:
    if key in bstack111lll1l1_opy_:
      bstack1l11l1ll1_opy_[bstack111lll1l1_opy_[key]] = bstack111ll1ll_opy_[key]
    else:
      bstack1l11l1ll1_opy_[key] = bstack111ll1ll_opy_[key]
  return bstack1l11l1ll1_opy_
def bstack1ll11llll_opy_(config, index=0):
  global bstack1l11111l1_opy_
  config = copy.deepcopy(config)
  caps = {}
  bstack111ll1ll_opy_ = bstack1llll1l1l_opy_(config)
  bstack1l11ll11l_opy_ = bstack11ll11lll_opy_
  bstack1l11ll11l_opy_ += bstack1l1l1l1ll_opy_
  if bstack1l11111l1_opy_:
    bstack1l11ll11l_opy_ += bstack1111ll11_opy_
  if bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣸ") in config:
    if bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࣹ࠭") in config[bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࣺࠬ")][index]:
      caps[bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࣻ")] = config[bstack11ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ")][index][bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪࣽ")]
    if bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧࣾ") in config[bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣿ")][index]:
      caps[bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩऀ")] = str(config[bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬँ")][index][bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫं")])
    bstack11l1ll11_opy_ = {}
    for bstack1lll111ll1_opy_ in bstack1l11ll11l_opy_:
      if bstack1lll111ll1_opy_ in config[bstack11ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧः")][index]:
        if bstack1lll111ll1_opy_ == bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧऄ"):
          try:
            bstack11l1ll11_opy_[bstack1lll111ll1_opy_] = str(config[bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩअ")][index][bstack1lll111ll1_opy_] * 1.0)
          except:
            bstack11l1ll11_opy_[bstack1lll111ll1_opy_] = str(config[bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪआ")][index][bstack1lll111ll1_opy_])
        else:
          bstack11l1ll11_opy_[bstack1lll111ll1_opy_] = config[bstack11ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index][bstack1lll111ll1_opy_]
        del (config[bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬई")][index][bstack1lll111ll1_opy_])
    bstack111ll1ll_opy_ = update(bstack111ll1ll_opy_, bstack11l1ll11_opy_)
  bstack111l1llll_opy_ = bstack11l1l1l1_opy_(config, index)
  for bstack1lllll1lll_opy_ in bstack11ll11lll_opy_ + [bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨउ"), bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬऊ")]:
    if bstack1lllll1lll_opy_ in bstack111l1llll_opy_:
      bstack111ll1ll_opy_[bstack1lllll1lll_opy_] = bstack111l1llll_opy_[bstack1lllll1lll_opy_]
      del (bstack111l1llll_opy_[bstack1lllll1lll_opy_])
  if bstack1ll11ll11_opy_(config):
    bstack111l1llll_opy_[bstack11ll11_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬऋ")] = True
    caps.update(bstack111ll1ll_opy_)
    caps[bstack11ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧऌ")] = bstack111l1llll_opy_
  else:
    bstack111l1llll_opy_[bstack11ll11_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧऍ")] = False
    caps.update(bstack1ll1111l_opy_(bstack111l1llll_opy_, bstack111ll1ll_opy_))
    if bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ऎ") in caps:
      caps[bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪए")] = caps[bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨऐ")]
      del (caps[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩऑ")])
    if bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऒ") in caps:
      caps[bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨओ")] = caps[bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨऔ")]
      del (caps[bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩक")])
  return caps
def bstack1lllllll1_opy_():
  global bstack1llll1l11l_opy_
  if bstack11l1llll_opy_() <= version.parse(bstack11ll11_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩख")):
    if bstack1llll1l11l_opy_ != bstack11ll11_opy_ (u"ࠪࠫग"):
      return bstack11ll11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧघ") + bstack1llll1l11l_opy_ + bstack11ll11_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤङ")
    return bstack1lll11llll_opy_
  if bstack1llll1l11l_opy_ != bstack11ll11_opy_ (u"࠭ࠧच"):
    return bstack11ll11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤछ") + bstack1llll1l11l_opy_ + bstack11ll11_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤज")
  return bstack11llll11_opy_
def bstack11ll1111l_opy_(options):
  return hasattr(options, bstack11ll11_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪझ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1111lllll_opy_(options, bstack1ll1ll1l11_opy_):
  for bstack11lll11l1_opy_ in bstack1ll1ll1l11_opy_:
    if bstack11lll11l1_opy_ in [bstack11ll11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨञ"), bstack11ll11_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨट")]:
      continue
    if bstack11lll11l1_opy_ in options._experimental_options:
      options._experimental_options[bstack11lll11l1_opy_] = update(options._experimental_options[bstack11lll11l1_opy_],
                                                         bstack1ll1ll1l11_opy_[bstack11lll11l1_opy_])
    else:
      options.add_experimental_option(bstack11lll11l1_opy_, bstack1ll1ll1l11_opy_[bstack11lll11l1_opy_])
  if bstack11ll11_opy_ (u"ࠬࡧࡲࡨࡵࠪठ") in bstack1ll1ll1l11_opy_:
    for arg in bstack1ll1ll1l11_opy_[bstack11ll11_opy_ (u"࠭ࡡࡳࡩࡶࠫड")]:
      options.add_argument(arg)
    del (bstack1ll1ll1l11_opy_[bstack11ll11_opy_ (u"ࠧࡢࡴࡪࡷࠬढ")])
  if bstack11ll11_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬण") in bstack1ll1ll1l11_opy_:
    for ext in bstack1ll1ll1l11_opy_[bstack11ll11_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭त")]:
      options.add_extension(ext)
    del (bstack1ll1ll1l11_opy_[bstack11ll11_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧथ")])
def bstack1111ll11l_opy_(options, bstack11l1ll11l_opy_):
  if bstack11ll11_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪद") in bstack11l1ll11l_opy_:
    for bstack1l1l1l1l1_opy_ in bstack11l1ll11l_opy_[bstack11ll11_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫध")]:
      if bstack1l1l1l1l1_opy_ in options._preferences:
        options._preferences[bstack1l1l1l1l1_opy_] = update(options._preferences[bstack1l1l1l1l1_opy_], bstack11l1ll11l_opy_[bstack11ll11_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬन")][bstack1l1l1l1l1_opy_])
      else:
        options.set_preference(bstack1l1l1l1l1_opy_, bstack11l1ll11l_opy_[bstack11ll11_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ऩ")][bstack1l1l1l1l1_opy_])
  if bstack11ll11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭प") in bstack11l1ll11l_opy_:
    for arg in bstack11l1ll11l_opy_[bstack11ll11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧफ")]:
      options.add_argument(arg)
def bstack1llll111l_opy_(options, bstack1l1111l1_opy_):
  if bstack11ll11_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫब") in bstack1l1111l1_opy_:
    options.use_webview(bool(bstack1l1111l1_opy_[bstack11ll11_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬभ")]))
  bstack1111lllll_opy_(options, bstack1l1111l1_opy_)
def bstack11l1lll11_opy_(options, bstack1111l1ll_opy_):
  for bstack11111llll_opy_ in bstack1111l1ll_opy_:
    if bstack11111llll_opy_ in [bstack11ll11_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩम"), bstack11ll11_opy_ (u"࠭ࡡࡳࡩࡶࠫय")]:
      continue
    options.set_capability(bstack11111llll_opy_, bstack1111l1ll_opy_[bstack11111llll_opy_])
  if bstack11ll11_opy_ (u"ࠧࡢࡴࡪࡷࠬर") in bstack1111l1ll_opy_:
    for arg in bstack1111l1ll_opy_[bstack11ll11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ऱ")]:
      options.add_argument(arg)
  if bstack11ll11_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ल") in bstack1111l1ll_opy_:
    options.bstack1ll1l1l1ll_opy_(bool(bstack1111l1ll_opy_[bstack11ll11_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧळ")]))
def bstack1lll1l11l1_opy_(options, bstack111l11l11_opy_):
  for bstack1l1lll111_opy_ in bstack111l11l11_opy_:
    if bstack1l1lll111_opy_ in [bstack11ll11_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऴ"), bstack11ll11_opy_ (u"ࠬࡧࡲࡨࡵࠪव")]:
      continue
    options._options[bstack1l1lll111_opy_] = bstack111l11l11_opy_[bstack1l1lll111_opy_]
  if bstack11ll11_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪश") in bstack111l11l11_opy_:
    for bstack11l11llll_opy_ in bstack111l11l11_opy_[bstack11ll11_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫष")]:
      options.bstack1ll11l11l_opy_(
        bstack11l11llll_opy_, bstack111l11l11_opy_[bstack11ll11_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस")][bstack11l11llll_opy_])
  if bstack11ll11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧह") in bstack111l11l11_opy_:
    for arg in bstack111l11l11_opy_[bstack11ll11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨऺ")]:
      options.add_argument(arg)
def bstack11lll1l11_opy_(options, caps):
  if not hasattr(options, bstack11ll11_opy_ (u"ࠫࡐࡋ࡙ࠨऻ")):
    return
  if options.KEY == bstack11ll11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵ़ࠪ") and options.KEY in caps:
    bstack1111lllll_opy_(options, caps[bstack11ll11_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫऽ")])
  elif options.KEY == bstack11ll11_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬा") and options.KEY in caps:
    bstack1111ll11l_opy_(options, caps[bstack11ll11_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ि")])
  elif options.KEY == bstack11ll11_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪी") and options.KEY in caps:
    bstack11l1lll11_opy_(options, caps[bstack11ll11_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫु")])
  elif options.KEY == bstack11ll11_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬू") and options.KEY in caps:
    bstack1llll111l_opy_(options, caps[bstack11ll11_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ृ")])
  elif options.KEY == bstack11ll11_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬॄ") and options.KEY in caps:
    bstack1lll1l11l1_opy_(options, caps[bstack11ll11_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ॅ")])
def bstack1lll11l1_opy_(caps):
  global bstack1l11111l1_opy_
  if isinstance(os.environ.get(bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩॆ")), str):
    bstack1l11111l1_opy_ = eval(os.getenv(bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪे")))
  if bstack1l11111l1_opy_:
    if bstack1111l11l1_opy_() < version.parse(bstack11ll11_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩै")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11ll11_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫॉ")
    if bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪॊ") in caps:
      browser = caps[bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो")]
    elif bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨौ") in caps:
      browser = caps[bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳ्ࠩ")]
    browser = str(browser).lower()
    if browser == bstack11ll11_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩॎ") or browser == bstack11ll11_opy_ (u"ࠪ࡭ࡵࡧࡤࠨॏ"):
      browser = bstack11ll11_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫॐ")
    if browser == bstack11ll11_opy_ (u"ࠬࡹࡡ࡮ࡵࡸࡲ࡬࠭॑"):
      browser = bstack11ll11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ॒࠭")
    if browser not in [bstack11ll11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ॓"), bstack11ll11_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭॔"), bstack11ll11_opy_ (u"ࠩ࡬ࡩࠬॕ"), bstack11ll11_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪॖ"), bstack11ll11_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬॗ")]:
      return None
    try:
      package = bstack11ll11_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࢂ࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧक़").format(browser)
      name = bstack11ll11_opy_ (u"࠭ࡏࡱࡶ࡬ࡳࡳࡹࠧख़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11ll1111l_opy_(options):
        return None
      for bstack1lllll1lll_opy_ in caps.keys():
        options.set_capability(bstack1lllll1lll_opy_, caps[bstack1lllll1lll_opy_])
      bstack11lll1l11_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l11l111_opy_(options, bstack11111ll1_opy_):
  if not bstack11ll1111l_opy_(options):
    return
  for bstack1lllll1lll_opy_ in bstack11111ll1_opy_.keys():
    if bstack1lllll1lll_opy_ in bstack1l1l1l1ll_opy_:
      continue
    if bstack1lllll1lll_opy_ in options._caps and type(options._caps[bstack1lllll1lll_opy_]) in [dict, list]:
      options._caps[bstack1lllll1lll_opy_] = update(options._caps[bstack1lllll1lll_opy_], bstack11111ll1_opy_[bstack1lllll1lll_opy_])
    else:
      options.set_capability(bstack1lllll1lll_opy_, bstack11111ll1_opy_[bstack1lllll1lll_opy_])
  bstack11lll1l11_opy_(options, bstack11111ll1_opy_)
  if bstack11ll11_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ग़") in options._caps:
    if options._caps[bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ज़")] and options._caps[bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧड़")].lower() != bstack11ll11_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫढ़"):
      del options._caps[bstack11ll11_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪफ़")]
def bstack1l1l1l1l_opy_(proxy_config):
  if bstack11ll11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩय़") in proxy_config:
    proxy_config[bstack11ll11_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨॠ")] = proxy_config[bstack11ll11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫॡ")]
    del (proxy_config[bstack11ll11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬॢ")])
  if bstack11ll11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬॣ") in proxy_config and proxy_config[bstack11ll11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭।")].lower() != bstack11ll11_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫ॥"):
    proxy_config[bstack11ll11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ०")] = bstack11ll11_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭१")
  if bstack11ll11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬ२") in proxy_config:
    proxy_config[bstack11ll11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ३")] = bstack11ll11_opy_ (u"ࠩࡳࡥࡨ࠭४")
  return proxy_config
def bstack1llll11ll1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11ll11_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ५") in config:
    return proxy
  config[bstack11ll11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ६")] = bstack1l1l1l1l_opy_(config[bstack11ll11_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ७")])
  if proxy == None:
    proxy = Proxy(config[bstack11ll11_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ८")])
  return proxy
def bstack11l1111l_opy_(self):
  global CONFIG
  global bstack11ll111l1_opy_
  try:
    proxy = bstack111l11111_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11ll11_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ९")):
        proxies = bstack1ll1lll1ll_opy_(proxy, bstack1lllllll1_opy_())
        if len(proxies) > 0:
          protocol, bstack11111lll_opy_ = proxies.popitem()
          if bstack11ll11_opy_ (u"ࠣ࠼࠲࠳ࠧ॰") in bstack11111lll_opy_:
            return bstack11111lll_opy_
          else:
            return bstack11ll11_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥॱ") + bstack11111lll_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11ll11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢॲ").format(str(e)))
  return bstack11ll111l1_opy_(self)
def bstack1lll1lll1l_opy_():
  global CONFIG
  return bstack1l1llll11_opy_(CONFIG) and bstack11l1llll_opy_() >= version.parse(bstack11111lll1_opy_)
def bstack1lll1llll1_opy_(config):
  bstack11l1lll1l_opy_ = {}
  if bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨॳ") in config:
    bstack11l1lll1l_opy_ = config[bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩॴ")]
  if bstack11ll11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬॵ") in config:
    bstack11l1lll1l_opy_ = config[bstack11ll11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ॶ")]
  proxy = bstack111l11111_opy_(config)
  if proxy:
    if proxy.endswith(bstack11ll11_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭ॷ")) and os.path.isfile(proxy):
      bstack11l1lll1l_opy_[bstack11ll11_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬॸ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11ll11_opy_ (u"ࠪ࠲ࡵࡧࡣࠨॹ")):
        proxies = bstack11ll1l111_opy_(config, bstack1lllllll1_opy_())
        if len(proxies) > 0:
          protocol, bstack11111lll_opy_ = proxies.popitem()
          if bstack11ll11_opy_ (u"ࠦ࠿࠵࠯ࠣॺ") in bstack11111lll_opy_:
            parsed_url = urlparse(bstack11111lll_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11ll11_opy_ (u"ࠧࡀ࠯࠰ࠤॻ") + bstack11111lll_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack11l1lll1l_opy_[bstack11ll11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡍࡵࡳࡵࠩॼ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack11l1lll1l_opy_[bstack11ll11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪॽ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack11l1lll1l_opy_[bstack11ll11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫॾ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack11l1lll1l_opy_[bstack11ll11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬॿ")] = str(parsed_url.password)
  return bstack11l1lll1l_opy_
def bstack1l11l1111_opy_(config):
  if bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨঀ") in config:
    return config[bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩঁ")]
  return {}
def bstack1llll1lll1_opy_(caps):
  global bstack11l1l11ll_opy_
  if bstack11ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ং") in caps:
    caps[bstack11ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧঃ")][bstack11ll11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭঄")] = True
    if bstack11l1l11ll_opy_:
      caps[bstack11ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩঅ")][bstack11ll11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫআ")] = bstack11l1l11ll_opy_
  else:
    caps[bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨই")] = True
    if bstack11l1l11ll_opy_:
      caps[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬঈ")] = bstack11l1l11ll_opy_
def bstack1ll1l111l_opy_():
  global CONFIG
  if bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩউ") in CONFIG and CONFIG[bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪঊ")]:
    bstack11l1lll1l_opy_ = bstack1lll1llll1_opy_(CONFIG)
    bstack1lllll1l1_opy_(CONFIG[bstack11ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪঋ")], bstack11l1lll1l_opy_)
def bstack1lllll1l1_opy_(key, bstack11l1lll1l_opy_):
  global bstack1lllll11ll_opy_
  logger.info(bstack111l1l11l_opy_)
  try:
    bstack1lllll11ll_opy_ = Local()
    bstack1ll1lll1l_opy_ = {bstack11ll11_opy_ (u"ࠨ࡭ࡨࡽࠬঌ"): key}
    bstack1ll1lll1l_opy_.update(bstack11l1lll1l_opy_)
    logger.debug(bstack1111lll11_opy_.format(str(bstack1ll1lll1l_opy_)))
    bstack1lllll11ll_opy_.start(**bstack1ll1lll1l_opy_)
    if bstack1lllll11ll_opy_.isRunning():
      logger.info(bstack1l11l1l1l_opy_)
  except Exception as e:
    bstack11ll11ll_opy_(bstack1ll1ll1l1_opy_.format(str(e)))
def bstack11111l111_opy_():
  global bstack1lllll11ll_opy_
  if bstack1lllll11ll_opy_.isRunning():
    logger.info(bstack11ll111l_opy_)
    bstack1lllll11ll_opy_.stop()
  bstack1lllll11ll_opy_ = None
def bstack111l1ll1_opy_(bstack11ll1l1l_opy_=[]):
  global CONFIG
  bstack1lll1l1l1l_opy_ = []
  bstack1ll1lll1l1_opy_ = [bstack11ll11_opy_ (u"ࠩࡲࡷࠬ঍"), bstack11ll11_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭঎"), bstack11ll11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨএ"), bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧঐ"), bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ঑"), bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ঒")]
  try:
    for err in bstack11ll1l1l_opy_:
      bstack1ll11l111_opy_ = {}
      for k in bstack1ll1lll1l1_opy_:
        val = CONFIG[bstack11ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫও")][int(err[bstack11ll11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨঔ")])].get(k)
        if val:
          bstack1ll11l111_opy_[k] = val
      bstack1ll11l111_opy_[bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡴࠩক")] = {
        err[bstack11ll11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩখ")]: err[bstack11ll11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫগ")]
      }
      bstack1lll1l1l1l_opy_.append(bstack1ll11l111_opy_)
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨࡲࡶࡲࡧࡴࡵ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡀࠠࠨঘ") + str(e))
  finally:
    return bstack1lll1l1l1l_opy_
def bstack111ll11ll_opy_():
  global bstack1lll111l_opy_
  global bstack1llll11l1_opy_
  global bstack1llll11ll_opy_
  if bstack1lll111l_opy_:
    logger.warning(bstack1lll1l11l_opy_.format(str(bstack1lll111l_opy_)))
  else:
    try:
      bstack1111l111l_opy_ = bstack1ll1ll111_opy_(bstack11ll11_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ঙ"), logger)
      if bstack1111l111l_opy_.get(bstack11ll11_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭চ")) and bstack1111l111l_opy_.get(bstack11ll11_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧছ")).get(bstack11ll11_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬজ")):
        logger.warning(bstack1lll1l11l_opy_.format(str(bstack1111l111l_opy_[bstack11ll11_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩঝ")][bstack11ll11_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧঞ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack11ll1111_opy_)
  global bstack1lllll11ll_opy_
  if bstack1lllll11ll_opy_:
    bstack11111l111_opy_()
  try:
    for driver in bstack1llll11l1_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1lllll1ll_opy_)
  bstack111lll1ll_opy_()
  if len(bstack1llll11ll_opy_) > 0:
    message = bstack111l1ll1_opy_(bstack1llll11ll_opy_)
    bstack111lll1ll_opy_(message)
  else:
    bstack111lll1ll_opy_()
  bstack1l1l111l1_opy_(bstack11l11ll1l_opy_, logger)
def bstack11l1ll111_opy_(self, *args):
  logger.error(bstack1ll111lll_opy_)
  bstack111ll11ll_opy_()
  sys.exit(1)
def bstack11ll11ll_opy_(err):
  logger.critical(bstack11l111l1_opy_.format(str(err)))
  bstack111lll1ll_opy_(bstack11l111l1_opy_.format(str(err)))
  atexit.unregister(bstack111ll11ll_opy_)
  sys.exit(1)
def bstack11lll1111_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack111lll1ll_opy_(message)
  atexit.unregister(bstack111ll11ll_opy_)
  sys.exit(1)
def bstack11l1llll1_opy_():
  global CONFIG
  global bstack1ll1lll1_opy_
  global bstack1ll11ll1l_opy_
  global bstack1llllll11l_opy_
  CONFIG = bstack1111llll_opy_()
  bstack1l1l1111_opy_()
  bstack11ll1ll1l_opy_()
  CONFIG = bstack1llll111_opy_(CONFIG)
  update(CONFIG, bstack1ll11ll1l_opy_)
  update(CONFIG, bstack1ll1lll1_opy_)
  CONFIG = bstack1ll1llll1l_opy_(CONFIG)
  bstack1llllll11l_opy_ = bstack1l1ll1l1_opy_(CONFIG)
  bstack1ll1l1lll1_opy_.bstack11ll111ll_opy_(bstack11ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧট"), bstack1llllll11l_opy_)
  if (bstack11ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪঠ") in CONFIG and bstack11ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫড") in bstack1ll1lll1_opy_) or (
          bstack11ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬঢ") in CONFIG and bstack11ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ণ") not in bstack1ll11ll1l_opy_):
    if os.getenv(bstack11ll11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨত")):
      CONFIG[bstack11ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧথ")] = os.getenv(bstack11ll11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪদ"))
    else:
      bstack11l1l111_opy_()
  elif (bstack11ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪধ") not in CONFIG and bstack11ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪন") in CONFIG) or (
          bstack11ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ঩") in bstack1ll11ll1l_opy_ and bstack11ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭প") not in bstack1ll1lll1_opy_):
    del (CONFIG[bstack11ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ফ")])
  if bstack11l1ll1ll_opy_(CONFIG):
    bstack11ll11ll_opy_(bstack1l1111ll1_opy_)
  bstack111ll1111_opy_()
  bstack1ll11l1l_opy_()
  if bstack1l11111l1_opy_:
    CONFIG[bstack11ll11_opy_ (u"ࠬࡧࡰࡱࠩব")] = bstack1111l11l_opy_(CONFIG)
    logger.info(bstack111111l1_opy_.format(CONFIG[bstack11ll11_opy_ (u"࠭ࡡࡱࡲࠪভ")]))
def bstack1ll1lll11_opy_(config, bstack1lll1l111_opy_):
  global CONFIG
  global bstack1l11111l1_opy_
  CONFIG = config
  bstack1l11111l1_opy_ = bstack1lll1l111_opy_
def bstack1ll11l1l_opy_():
  global CONFIG
  global bstack1l11111l1_opy_
  if bstack11ll11_opy_ (u"ࠧࡢࡲࡳࠫম") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11lll1111_opy_(e, bstack111ll1l1l_opy_)
    bstack1l11111l1_opy_ = True
    bstack1ll1l1lll1_opy_.bstack11ll111ll_opy_(bstack11ll11_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧয"), True)
def bstack1111l11l_opy_(config):
  bstack1ll1l11l_opy_ = bstack11ll11_opy_ (u"ࠩࠪর")
  app = config[bstack11ll11_opy_ (u"ࠪࡥࡵࡶࠧ঱")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1llllll1ll_opy_:
      if os.path.exists(app):
        bstack1ll1l11l_opy_ = bstack1l111l1ll_opy_(config, app)
      elif bstack1l1ll11l_opy_(app):
        bstack1ll1l11l_opy_ = app
      else:
        bstack11ll11ll_opy_(bstack1l111lll1_opy_.format(app))
    else:
      if bstack1l1ll11l_opy_(app):
        bstack1ll1l11l_opy_ = app
      elif os.path.exists(app):
        bstack1ll1l11l_opy_ = bstack1l111l1ll_opy_(app)
      else:
        bstack11ll11ll_opy_(bstack1111ll1ll_opy_)
  else:
    if len(app) > 2:
      bstack11ll11ll_opy_(bstack1l1l111l_opy_)
    elif len(app) == 2:
      if bstack11ll11_opy_ (u"ࠫࡵࡧࡴࡩࠩল") in app and bstack11ll11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ঳") in app:
        if os.path.exists(app[bstack11ll11_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ঴")]):
          bstack1ll1l11l_opy_ = bstack1l111l1ll_opy_(config, app[bstack11ll11_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ঵")], app[bstack11ll11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫশ")])
        else:
          bstack11ll11ll_opy_(bstack1l111lll1_opy_.format(app))
      else:
        bstack11ll11ll_opy_(bstack1l1l111l_opy_)
    else:
      for key in app:
        if key in bstack1111l1l1l_opy_:
          if key == bstack11ll11_opy_ (u"ࠩࡳࡥࡹ࡮ࠧষ"):
            if os.path.exists(app[key]):
              bstack1ll1l11l_opy_ = bstack1l111l1ll_opy_(config, app[key])
            else:
              bstack11ll11ll_opy_(bstack1l111lll1_opy_.format(app))
          else:
            bstack1ll1l11l_opy_ = app[key]
        else:
          bstack11ll11ll_opy_(bstack11111l1l1_opy_)
  return bstack1ll1l11l_opy_
def bstack1l1ll11l_opy_(bstack1ll1l11l_opy_):
  import re
  bstack1111111l_opy_ = re.compile(bstack11ll11_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥস"))
  bstack1l11l1lll_opy_ = re.compile(bstack11ll11_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬ࠲࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣহ"))
  if bstack11ll11_opy_ (u"ࠬࡨࡳ࠻࠱࠲ࠫ঺") in bstack1ll1l11l_opy_ or re.fullmatch(bstack1111111l_opy_, bstack1ll1l11l_opy_) or re.fullmatch(bstack1l11l1lll_opy_, bstack1ll1l11l_opy_):
    return True
  else:
    return False
def bstack1l111l1ll_opy_(config, path, bstack1ll1ll11l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11ll11_opy_ (u"࠭ࡲࡣࠩ঻")).read()).hexdigest()
  bstack1lllll1ll1_opy_ = bstack1ll1l11l11_opy_(md5_hash)
  bstack1ll1l11l_opy_ = None
  if bstack1lllll1ll1_opy_:
    logger.info(bstack1ll1111ll_opy_.format(bstack1lllll1ll1_opy_, md5_hash))
    return bstack1lllll1ll1_opy_
  bstack11l1ll1l1_opy_ = MultipartEncoder(
    fields={
      bstack11ll11_opy_ (u"ࠧࡧ࡫࡯ࡩ়ࠬ"): (os.path.basename(path), open(os.path.abspath(path), bstack11ll11_opy_ (u"ࠨࡴࡥࠫঽ")), bstack11ll11_opy_ (u"ࠩࡷࡩࡽࡺ࠯ࡱ࡮ࡤ࡭ࡳ࠭া")),
      bstack11ll11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ি"): bstack1ll1ll11l_opy_
    }
  )
  response = requests.post(bstack11l111l1l_opy_, data=bstack11l1ll1l1_opy_,
                           headers={bstack11ll11_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪী"): bstack11l1ll1l1_opy_.content_type},
                           auth=(config[bstack11ll11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧু")], config[bstack11ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩূ")]))
  try:
    res = json.loads(response.text)
    bstack1ll1l11l_opy_ = res[bstack11ll11_opy_ (u"ࠧࡢࡲࡳࡣࡺࡸ࡬ࠨৃ")]
    logger.info(bstack111llllll_opy_.format(bstack1ll1l11l_opy_))
    bstack111l1l11_opy_(md5_hash, bstack1ll1l11l_opy_)
  except ValueError as err:
    bstack11ll11ll_opy_(bstack1l111111l_opy_.format(str(err)))
  return bstack1ll1l11l_opy_
def bstack111ll1111_opy_():
  global CONFIG
  global bstack1ll1l1lll_opy_
  bstack111111lll_opy_ = 0
  bstack11111111l_opy_ = 1
  if bstack11ll11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨৄ") in CONFIG:
    bstack11111111l_opy_ = CONFIG[bstack11ll11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ৅")]
  if bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭৆") in CONFIG:
    bstack111111lll_opy_ = len(CONFIG[bstack11ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧে")])
  bstack1ll1l1lll_opy_ = int(bstack11111111l_opy_) * int(bstack111111lll_opy_)
def bstack1ll1l11l11_opy_(md5_hash):
  bstack11111l1l_opy_ = os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"ࠬࢄࠧৈ")), bstack11ll11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭৉"), bstack11ll11_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ৊"))
  if os.path.exists(bstack11111l1l_opy_):
    bstack1111111ll_opy_ = json.load(open(bstack11111l1l_opy_, bstack11ll11_opy_ (u"ࠨࡴࡥࠫো")))
    if md5_hash in bstack1111111ll_opy_:
      bstack11l111111_opy_ = bstack1111111ll_opy_[md5_hash]
      bstack111ll111l_opy_ = datetime.datetime.now()
      bstack1l1l11l1l_opy_ = datetime.datetime.strptime(bstack11l111111_opy_[bstack11ll11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬৌ")], bstack11ll11_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾্࡙ࠪࠧ"))
      if (bstack111ll111l_opy_ - bstack1l1l11l1l_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack11l111111_opy_[bstack11ll11_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩৎ")]):
        return None
      return bstack11l111111_opy_[bstack11ll11_opy_ (u"ࠬ࡯ࡤࠨ৏")]
  else:
    return None
def bstack111l1l11_opy_(md5_hash, bstack1ll1l11l_opy_):
  bstack1llll1l1ll_opy_ = os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"࠭ࡾࠨ৐")), bstack11ll11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ৑"))
  if not os.path.exists(bstack1llll1l1ll_opy_):
    os.makedirs(bstack1llll1l1ll_opy_)
  bstack11111l1l_opy_ = os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"ࠨࢀࠪ৒")), bstack11ll11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ৓"), bstack11ll11_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫ৔"))
  bstack11l11111_opy_ = {
    bstack11ll11_opy_ (u"ࠫ࡮ࡪࠧ৕"): bstack1ll1l11l_opy_,
    bstack11ll11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ৖"): datetime.datetime.strftime(datetime.datetime.now(), bstack11ll11_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪৗ")),
    bstack11ll11_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ৘"): str(__version__)
  }
  if os.path.exists(bstack11111l1l_opy_):
    bstack1111111ll_opy_ = json.load(open(bstack11111l1l_opy_, bstack11ll11_opy_ (u"ࠨࡴࡥࠫ৙")))
  else:
    bstack1111111ll_opy_ = {}
  bstack1111111ll_opy_[md5_hash] = bstack11l11111_opy_
  with open(bstack11111l1l_opy_, bstack11ll11_opy_ (u"ࠤࡺ࠯ࠧ৚")) as outfile:
    json.dump(bstack1111111ll_opy_, outfile)
def bstack111l1lll1_opy_(self):
  return
def bstack11ll1l11l_opy_(self):
  return
def bstack11ll1l11_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1ll1lll11l_opy_(self):
  global bstack1llll1111l_opy_
  global bstack1l11ll1l_opy_
  global bstack11ll11l1_opy_
  try:
    if bstack11ll11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ৛") in bstack1llll1111l_opy_ and self.session_id != None:
      bstack1llll1llll_opy_ = bstack11ll11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫড়") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬঢ়")
      bstack11llll11l_opy_ = bstack1l1ll11ll_opy_(bstack11ll11_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩ৞"), bstack11ll11_opy_ (u"ࠧࠨয়"), bstack1llll1llll_opy_, bstack11ll11_opy_ (u"ࠨ࠮ࠣࠫৠ").join(
        threading.current_thread().bstackTestErrorMessages), bstack11ll11_opy_ (u"ࠩࠪৡ"), bstack11ll11_opy_ (u"ࠪࠫৢ"))
      if self != None:
        self.execute_script(bstack11llll11l_opy_)
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧৣ") + str(e))
  bstack11ll11l1_opy_(self)
  self.session_id = None
def bstack1ll1lllll1_opy_(self, *args, **kwargs):
  bstack111111ll1_opy_ = bstack111l1ll11_opy_(self, *args, **kwargs)
  bstack1llll1111_opy_.bstack1l111ll1_opy_(self)
  return bstack111111ll1_opy_
def bstack11lll1l1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1l11ll1l_opy_
  global bstack1lll1111ll_opy_
  global bstack1l11lll11_opy_
  global bstack1ll111ll_opy_
  global bstack1l111111_opy_
  global bstack1llll1111l_opy_
  global bstack111l1ll11_opy_
  global bstack1llll11l1_opy_
  global bstack1lll1ll11_opy_
  CONFIG[bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ৤")] = str(bstack1llll1111l_opy_) + str(__version__)
  command_executor = bstack1lllllll1_opy_()
  logger.debug(bstack1ll11lll_opy_.format(command_executor))
  proxy = bstack1llll11ll1_opy_(CONFIG, proxy)
  bstack111l111l_opy_ = 0 if bstack1lll1111ll_opy_ < 0 else bstack1lll1111ll_opy_
  try:
    if bstack1ll111ll_opy_ is True:
      bstack111l111l_opy_ = int(multiprocessing.current_process().name)
    elif bstack1l111111_opy_ is True:
      bstack111l111l_opy_ = int(threading.current_thread().name)
  except:
    bstack111l111l_opy_ = 0
  bstack11111ll1_opy_ = bstack1ll11llll_opy_(CONFIG, bstack111l111l_opy_)
  logger.debug(bstack111111l1l_opy_.format(str(bstack11111ll1_opy_)))
  if bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ৥") in CONFIG and CONFIG[bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ০")]:
    bstack1llll1lll1_opy_(bstack11111ll1_opy_)
  if desired_capabilities:
    bstack111l11ll_opy_ = bstack1llll111_opy_(desired_capabilities)
    bstack111l11ll_opy_[bstack11ll11_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ১")] = bstack1ll11ll11_opy_(CONFIG)
    bstack1ll1l1l111_opy_ = bstack1ll11llll_opy_(bstack111l11ll_opy_)
    if bstack1ll1l1l111_opy_:
      bstack11111ll1_opy_ = update(bstack1ll1l1l111_opy_, bstack11111ll1_opy_)
    desired_capabilities = None
  if options:
    bstack1l11l111_opy_(options, bstack11111ll1_opy_)
  if not options:
    options = bstack1lll11l1_opy_(bstack11111ll1_opy_)
  if proxy and bstack11l1llll_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩ২")):
    options.proxy(proxy)
  if options and bstack11l1llll_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ৩")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack11l1llll_opy_() < version.parse(bstack11ll11_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ৪")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11111ll1_opy_)
  logger.info(bstack1ll1ll1ll1_opy_)
  if bstack11l1llll_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ৫")):
    bstack111l1ll11_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack11l1llll_opy_() >= version.parse(bstack11ll11_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ৬")):
    bstack111l1ll11_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack11l1llll_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧ৭")):
    bstack111l1ll11_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack111l1ll11_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack111l111ll_opy_ = bstack11ll11_opy_ (u"ࠨࠩ৮")
    if bstack11l1llll_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࡣ࠳ࠪ৯")):
      bstack111l111ll_opy_ = self.caps.get(bstack11ll11_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥৰ"))
    else:
      bstack111l111ll_opy_ = self.capabilities.get(bstack11ll11_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦৱ"))
    if bstack111l111ll_opy_:
      if bstack11l1llll_opy_() <= version.parse(bstack11ll11_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬ৲")):
        self.command_executor._url = bstack11ll11_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ৳") + bstack1llll1l11l_opy_ + bstack11ll11_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ৴")
      else:
        self.command_executor._url = bstack11ll11_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥ৵") + bstack111l111ll_opy_ + bstack11ll11_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥ৶")
      logger.debug(bstack1l11111l_opy_.format(bstack111l111ll_opy_))
    else:
      logger.debug(bstack11llll1l1_opy_.format(bstack11ll11_opy_ (u"ࠥࡓࡵࡺࡩ࡮ࡣ࡯ࠤࡍࡻࡢࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠦ৷")))
  except Exception as e:
    logger.debug(bstack11llll1l1_opy_.format(e))
  if bstack11ll11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ৸") in bstack1llll1111l_opy_:
    bstack1ll1ll1l_opy_(bstack1lll1111ll_opy_, bstack1lll1ll11_opy_)
  bstack1l11ll1l_opy_ = self.session_id
  if bstack11ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ৹") in bstack1llll1111l_opy_ or bstack11ll11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭৺") in bstack1llll1111l_opy_:
    threading.current_thread().bstack11l1ll1l_opy_ = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1llll1111_opy_.bstack1l111ll1_opy_(self)
  bstack1llll11l1_opy_.append(self)
  if bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৻") in CONFIG and bstack11ll11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ৼ") in CONFIG[bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ৽")][bstack111l111l_opy_]:
    bstack1l11lll11_opy_ = CONFIG[bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭৾")][bstack111l111l_opy_][bstack11ll11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ৿")]
  logger.debug(bstack1l11llll1_opy_.format(bstack1l11ll1l_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1ll1l11ll_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1l1l1ll1l_opy_
      if(bstack11ll11_opy_ (u"ࠧ࡯࡮ࡥࡧࡻ࠲࡯ࡹࠢ਀") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"࠭ࡾࠨਁ")), bstack11ll11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧਂ"), bstack11ll11_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪਃ")), bstack11ll11_opy_ (u"ࠩࡺࠫ਄")) as fp:
          fp.write(bstack11ll11_opy_ (u"ࠥࠦਅ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11ll11_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨਆ")))):
          with open(args[1], bstack11ll11_opy_ (u"ࠬࡸࠧਇ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11ll11_opy_ (u"࠭ࡡࡴࡻࡱࡧࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡠࡰࡨࡻࡕࡧࡧࡦࠪࡦࡳࡳࡺࡥࡹࡶ࠯ࠤࡵࡧࡧࡦࠢࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠬਈ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l1ll111l_opy_)
            lines.insert(1, bstack111l111l1_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11ll11_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤਉ")), bstack11ll11_opy_ (u"ࠨࡹࠪਊ")) as bstack1l1111ll_opy_:
              bstack1l1111ll_opy_.writelines(lines)
        CONFIG[bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ਋")] = str(bstack1llll1111l_opy_) + str(__version__)
        bstack111l111l_opy_ = 0 if bstack1lll1111ll_opy_ < 0 else bstack1lll1111ll_opy_
        try:
          if bstack1ll111ll_opy_ is True:
            bstack111l111l_opy_ = int(multiprocessing.current_process().name)
          elif bstack1l111111_opy_ is True:
            bstack111l111l_opy_ = int(threading.current_thread().name)
        except:
          bstack111l111l_opy_ = 0
        CONFIG[bstack11ll11_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥ਌")] = False
        CONFIG[bstack11ll11_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ਍")] = True
        bstack11111ll1_opy_ = bstack1ll11llll_opy_(CONFIG, bstack111l111l_opy_)
        logger.debug(bstack111111l1l_opy_.format(str(bstack11111ll1_opy_)))
        if CONFIG[bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ਎")]:
          bstack1llll1lll1_opy_(bstack11111ll1_opy_)
        if bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਏ") in CONFIG and bstack11ll11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬਐ") in CONFIG[bstack11ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ਑")][bstack111l111l_opy_]:
          bstack1l11lll11_opy_ = CONFIG[bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ਒")][bstack111l111l_opy_][bstack11ll11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨਓ")]
        args.append(os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"ࠫࢃ࠭ਔ")), bstack11ll11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬਕ"), bstack11ll11_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨਖ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11111ll1_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11ll11_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤਗ"))
      bstack1l1l1ll1l_opy_ = True
      return bstack11llll1ll_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1l11ll1l1_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1lll1111ll_opy_
    global bstack1l11lll11_opy_
    global bstack1ll111ll_opy_
    global bstack1l111111_opy_
    global bstack1llll1111l_opy_
    CONFIG[bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪਘ")] = str(bstack1llll1111l_opy_) + str(__version__)
    bstack111l111l_opy_ = 0 if bstack1lll1111ll_opy_ < 0 else bstack1lll1111ll_opy_
    try:
      if bstack1ll111ll_opy_ is True:
        bstack111l111l_opy_ = int(multiprocessing.current_process().name)
      elif bstack1l111111_opy_ is True:
        bstack111l111l_opy_ = int(threading.current_thread().name)
    except:
      bstack111l111l_opy_ = 0
    CONFIG[bstack11ll11_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣਙ")] = True
    bstack11111ll1_opy_ = bstack1ll11llll_opy_(CONFIG, bstack111l111l_opy_)
    logger.debug(bstack111111l1l_opy_.format(str(bstack11111ll1_opy_)))
    if CONFIG[bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧਚ")]:
      bstack1llll1lll1_opy_(bstack11111ll1_opy_)
    if bstack11ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਛ") in CONFIG and bstack11ll11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪਜ") in CONFIG[bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਝ")][bstack111l111l_opy_]:
      bstack1l11lll11_opy_ = CONFIG[bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪਞ")][bstack111l111l_opy_][bstack11ll11_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ਟ")]
    import urllib
    import json
    bstack1ll1l111ll_opy_ = bstack11ll11_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫਠ") + urllib.parse.quote(json.dumps(bstack11111ll1_opy_))
    browser = self.connect(bstack1ll1l111ll_opy_)
    return browser
except Exception as e:
    pass
def bstack11lll111l_opy_():
    global bstack1l1l1ll1l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1l11ll1l1_opy_
        bstack1l1l1ll1l_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1ll1l11ll_opy_
      bstack1l1l1ll1l_opy_ = True
    except Exception as e:
      pass
def bstack1lll1l1lll_opy_(context, bstack1lll1ll1_opy_):
  try:
    context.page.evaluate(bstack11ll11_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦਡ"), bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨਢ")+ json.dumps(bstack1lll1ll1_opy_) + bstack11ll11_opy_ (u"ࠧࢃࡽࠣਣ"))
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀࠦਤ"), e)
def bstack1lll11l1ll_opy_(context, message, level):
  try:
    context.page.evaluate(bstack11ll11_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣਥ"), bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ਦ") + json.dumps(message) + bstack11ll11_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬਧ") + json.dumps(level) + bstack11ll11_opy_ (u"ࠪࢁࢂ࠭ਨ"))
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃࠢ਩"), e)
def bstack1l111llll_opy_(context, status, message = bstack11ll11_opy_ (u"ࠧࠨਪ")):
  try:
    if(status == bstack11ll11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨਫ")):
      context.page.evaluate(bstack11ll11_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣਬ"), bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡳࡧࡤࡷࡴࡴࠢ࠻ࠩਭ") + json.dumps(bstack11ll11_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࠦਮ") + str(message)) + bstack11ll11_opy_ (u"ࠪ࠰ࠧࡹࡴࡢࡶࡸࡷࠧࡀࠧਯ") + json.dumps(status) + bstack11ll11_opy_ (u"ࠦࢂࢃࠢਰ"))
    else:
      context.page.evaluate(bstack11ll11_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ਱"), bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠧਲ") + json.dumps(status) + bstack11ll11_opy_ (u"ࠢࡾࡿࠥਲ਼"))
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢࡾࢁࠧ਴"), e)
def bstack111ll1l1_opy_(self, url):
  global bstack11111ll1l_opy_
  try:
    bstack1lll1l11_opy_(url)
  except Exception as err:
    logger.debug(bstack1lll11lll1_opy_.format(str(err)))
  try:
    bstack11111ll1l_opy_(self, url)
  except Exception as e:
    try:
      bstack11l11l11l_opy_ = str(e)
      if any(err_msg in bstack11l11l11l_opy_ for err_msg in bstack111ll11l1_opy_):
        bstack1lll1l11_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1lll11lll1_opy_.format(str(err)))
    raise e
def bstack1l1lll11l_opy_(self):
  global bstack1lll111l1_opy_
  bstack1lll111l1_opy_ = self
  return
def bstack11l1lllll_opy_(self):
  global bstack1llllll1l1_opy_
  bstack1llllll1l1_opy_ = self
  return
def bstack11lll1ll_opy_(self, test):
  global CONFIG
  global bstack1llllll1l1_opy_
  global bstack1lll111l1_opy_
  global bstack1l11ll1l_opy_
  global bstack1ll1l1l11l_opy_
  global bstack1l11lll11_opy_
  global bstack1lll1l1111_opy_
  global bstack1lll11ll_opy_
  global bstack1lll1ll111_opy_
  global bstack1llll11l1_opy_
  try:
    if not bstack1l11ll1l_opy_:
      with open(os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"ࠩࢁࠫਵ")), bstack11ll11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪਸ਼"), bstack11ll11_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭਷"))) as f:
        bstack111111ll_opy_ = json.loads(bstack11ll11_opy_ (u"ࠧࢁࠢਸ") + f.read().strip() + bstack11ll11_opy_ (u"࠭ࠢࡹࠤ࠽ࠤࠧࡿࠢࠨਹ") + bstack11ll11_opy_ (u"ࠢࡾࠤ਺"))
        bstack1l11ll1l_opy_ = bstack111111ll_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1llll11l1_opy_:
    for driver in bstack1llll11l1_opy_:
      if bstack1l11ll1l_opy_ == driver.session_id:
        if test:
          bstack1ll111l1_opy_ = str(test.data)
        if not bstack11l111lll_opy_ and bstack1ll111l1_opy_:
          bstack1ll11l11_opy_ = {
            bstack11ll11_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ਻"): bstack11ll11_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧ਼ࠪ"),
            bstack11ll11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭਽"): {
              bstack11ll11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩਾ"): bstack1ll111l1_opy_
            }
          }
          bstack1l111ll1l_opy_ = bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪਿ").format(json.dumps(bstack1ll11l11_opy_))
          driver.execute_script(bstack1l111ll1l_opy_)
        if bstack1ll1l1l11l_opy_:
          bstack1l11111ll_opy_ = {
            bstack11ll11_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ੀ"): bstack11ll11_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩੁ"),
            bstack11ll11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫੂ"): {
              bstack11ll11_opy_ (u"ࠩࡧࡥࡹࡧࠧ੃"): bstack1ll111l1_opy_ + bstack11ll11_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬ੄"),
              bstack11ll11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ੅"): bstack11ll11_opy_ (u"ࠬ࡯࡮ࡧࡱࠪ੆")
            }
          }
          bstack1ll11l11_opy_ = {
            bstack11ll11_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ੇ"): bstack11ll11_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪੈ"),
            bstack11ll11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ੉"): {
              bstack11ll11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ੊"): bstack11ll11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪੋ")
            }
          }
          if bstack1ll1l1l11l_opy_.status == bstack11ll11_opy_ (u"ࠫࡕࡇࡓࡔࠩੌ"):
            bstack1lllllll1l_opy_ = bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿ੍ࠪ").format(json.dumps(bstack1l11111ll_opy_))
            driver.execute_script(bstack1lllllll1l_opy_)
            bstack1l111ll1l_opy_ = bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ੎").format(json.dumps(bstack1ll11l11_opy_))
            driver.execute_script(bstack1l111ll1l_opy_)
          elif bstack1ll1l1l11l_opy_.status == bstack11ll11_opy_ (u"ࠧࡇࡃࡌࡐࠬ੏"):
            reason = bstack11ll11_opy_ (u"ࠣࠤ੐")
            bstack1lll11111l_opy_ = bstack1ll111l1_opy_ + bstack11ll11_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠪੑ")
            if bstack1ll1l1l11l_opy_.message:
              reason = str(bstack1ll1l1l11l_opy_.message)
              bstack1lll11111l_opy_ = bstack1lll11111l_opy_ + bstack11ll11_opy_ (u"ࠪࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࠪ੒") + reason
            bstack1l11111ll_opy_[bstack11ll11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ੓")] = {
              bstack11ll11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ੔"): bstack11ll11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ੕"),
              bstack11ll11_opy_ (u"ࠧࡥࡣࡷࡥࠬ੖"): bstack1lll11111l_opy_
            }
            bstack1ll11l11_opy_[bstack11ll11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ੗")] = {
              bstack11ll11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ੘"): bstack11ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪਖ਼"),
              bstack11ll11_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫਗ਼"): reason
            }
            bstack1lllllll1l_opy_ = bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪਜ਼").format(json.dumps(bstack1l11111ll_opy_))
            driver.execute_script(bstack1lllllll1l_opy_)
            bstack1l111ll1l_opy_ = bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫੜ").format(json.dumps(bstack1ll11l11_opy_))
            driver.execute_script(bstack1l111ll1l_opy_)
  elif bstack1l11ll1l_opy_:
    try:
      data = {}
      bstack1ll111l1_opy_ = None
      if test:
        bstack1ll111l1_opy_ = str(test.data)
      if not bstack11l111lll_opy_ and bstack1ll111l1_opy_:
        data[bstack11ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ੝")] = bstack1ll111l1_opy_
      if bstack1ll1l1l11l_opy_:
        if bstack1ll1l1l11l_opy_.status == bstack11ll11_opy_ (u"ࠨࡒࡄࡗࡘ࠭ਫ਼"):
          data[bstack11ll11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ੟")] = bstack11ll11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ੠")
        elif bstack1ll1l1l11l_opy_.status == bstack11ll11_opy_ (u"ࠫࡋࡇࡉࡍࠩ੡"):
          data[bstack11ll11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ੢")] = bstack11ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭੣")
          if bstack1ll1l1l11l_opy_.message:
            data[bstack11ll11_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ੤")] = str(bstack1ll1l1l11l_opy_.message)
      user = CONFIG[bstack11ll11_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ੥")]
      key = CONFIG[bstack11ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ੦")]
      url = bstack11ll11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡹࡥࡴࡵ࡬ࡳࡳࡹ࠯ࡼࡿ࠱࡮ࡸࡵ࡮ࠨ੧").format(user, key, bstack1l11ll1l_opy_)
      headers = {
        bstack11ll11_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪ੨"): bstack11ll11_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ੩"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1l111ll11_opy_.format(str(e)))
  if bstack1llllll1l1_opy_:
    bstack1lll11ll_opy_(bstack1llllll1l1_opy_)
  if bstack1lll111l1_opy_:
    bstack1lll1ll111_opy_(bstack1lll111l1_opy_)
  bstack1lll1l1111_opy_(self, test)
def bstack1ll111111_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack11ll1l1ll_opy_
  bstack11ll1l1ll_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1ll1l1l11l_opy_
  bstack1ll1l1l11l_opy_ = self._test
def bstack11llll111_opy_():
  global bstack1lll1l1l11_opy_
  try:
    if os.path.exists(bstack1lll1l1l11_opy_):
      os.remove(bstack1lll1l1l11_opy_)
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩ੪") + str(e))
def bstack1l1ll11l1_opy_():
  global bstack1lll1l1l11_opy_
  bstack1111l111l_opy_ = {}
  try:
    if not os.path.isfile(bstack1lll1l1l11_opy_):
      with open(bstack1lll1l1l11_opy_, bstack11ll11_opy_ (u"ࠧࡸࠩ੫")):
        pass
      with open(bstack1lll1l1l11_opy_, bstack11ll11_opy_ (u"ࠣࡹ࠮ࠦ੬")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1lll1l1l11_opy_):
      bstack1111l111l_opy_ = json.load(open(bstack1lll1l1l11_opy_, bstack11ll11_opy_ (u"ࠩࡵࡦࠬ੭")))
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡸࡥࡢࡦ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬ੮") + str(e))
  finally:
    return bstack1111l111l_opy_
def bstack1ll1ll1l_opy_(platform_index, item_index):
  global bstack1lll1l1l11_opy_
  try:
    bstack1111l111l_opy_ = bstack1l1ll11l1_opy_()
    bstack1111l111l_opy_[item_index] = platform_index
    with open(bstack1lll1l1l11_opy_, bstack11ll11_opy_ (u"ࠦࡼ࠱ࠢ੯")) as outfile:
      json.dump(bstack1111l111l_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡸࡴ࡬ࡸ࡮ࡴࡧࠡࡶࡲࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪੰ") + str(e))
def bstack1111l1111_opy_(bstack11ll1ll11_opy_):
  global CONFIG
  bstack1ll1l111_opy_ = bstack11ll11_opy_ (u"࠭ࠧੱ")
  if not bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪੲ") in CONFIG:
    logger.info(bstack11ll11_opy_ (u"ࠨࡐࡲࠤࡵࡲࡡࡵࡨࡲࡶࡲࡹࠠࡱࡣࡶࡷࡪࡪࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡸࡥࡱࡱࡵࡸࠥ࡬࡯ࡳࠢࡕࡳࡧࡵࡴࠡࡴࡸࡲࠬੳ"))
  try:
    platform = CONFIG[bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬੴ")][bstack11ll1ll11_opy_]
    if bstack11ll11_opy_ (u"ࠪࡳࡸ࠭ੵ") in platform:
      bstack1ll1l111_opy_ += str(platform[bstack11ll11_opy_ (u"ࠫࡴࡹࠧ੶")]) + bstack11ll11_opy_ (u"ࠬ࠲ࠠࠨ੷")
    if bstack11ll11_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ੸") in platform:
      bstack1ll1l111_opy_ += str(platform[bstack11ll11_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ੹")]) + bstack11ll11_opy_ (u"ࠨ࠮ࠣࠫ੺")
    if bstack11ll11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭੻") in platform:
      bstack1ll1l111_opy_ += str(platform[bstack11ll11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ੼")]) + bstack11ll11_opy_ (u"ࠫ࠱ࠦࠧ੽")
    if bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ੾") in platform:
      bstack1ll1l111_opy_ += str(platform[bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ੿")]) + bstack11ll11_opy_ (u"ࠧ࠭ࠢࠪ઀")
    if bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ઁ") in platform:
      bstack1ll1l111_opy_ += str(platform[bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧં")]) + bstack11ll11_opy_ (u"ࠪ࠰ࠥ࠭ઃ")
    if bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ઄") in platform:
      bstack1ll1l111_opy_ += str(platform[bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭અ")]) + bstack11ll11_opy_ (u"࠭ࠬࠡࠩઆ")
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"ࠧࡔࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡳࡵࡴ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡶࡪࡶ࡯ࡳࡶࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡴࡴࠧઇ") + str(e))
  finally:
    if bstack1ll1l111_opy_[len(bstack1ll1l111_opy_) - 2:] == bstack11ll11_opy_ (u"ࠨ࠮ࠣࠫઈ"):
      bstack1ll1l111_opy_ = bstack1ll1l111_opy_[:-2]
    return bstack1ll1l111_opy_
def bstack1lllll11_opy_(path, bstack1ll1l111_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack11lllll11_opy_ = ET.parse(path)
    bstack111l11l1_opy_ = bstack11lllll11_opy_.getroot()
    bstack1llllll11_opy_ = None
    for suite in bstack111l11l1_opy_.iter(bstack11ll11_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨઉ")):
      if bstack11ll11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪઊ") in suite.attrib:
        suite.attrib[bstack11ll11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩઋ")] += bstack11ll11_opy_ (u"ࠬࠦࠧઌ") + bstack1ll1l111_opy_
        bstack1llllll11_opy_ = suite
    bstack1111l11ll_opy_ = None
    for robot in bstack111l11l1_opy_.iter(bstack11ll11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬઍ")):
      bstack1111l11ll_opy_ = robot
    bstack1llll1ll1l_opy_ = len(bstack1111l11ll_opy_.findall(bstack11ll11_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭઎")))
    if bstack1llll1ll1l_opy_ == 1:
      bstack1111l11ll_opy_.remove(bstack1111l11ll_opy_.findall(bstack11ll11_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧએ"))[0])
      bstack1lll1ll1l1_opy_ = ET.Element(bstack11ll11_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨઐ"), attrib={bstack11ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨઑ"): bstack11ll11_opy_ (u"ࠫࡘࡻࡩࡵࡧࡶࠫ઒"), bstack11ll11_opy_ (u"ࠬ࡯ࡤࠨઓ"): bstack11ll11_opy_ (u"࠭ࡳ࠱ࠩઔ")})
      bstack1111l11ll_opy_.insert(1, bstack1lll1ll1l1_opy_)
      bstack1l1l1ll11_opy_ = None
      for suite in bstack1111l11ll_opy_.iter(bstack11ll11_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭ક")):
        bstack1l1l1ll11_opy_ = suite
      bstack1l1l1ll11_opy_.append(bstack1llllll11_opy_)
      bstack1lll11l111_opy_ = None
      for status in bstack1llllll11_opy_.iter(bstack11ll11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨખ")):
        bstack1lll11l111_opy_ = status
      bstack1l1l1ll11_opy_.append(bstack1lll11l111_opy_)
    bstack11lllll11_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠧગ") + str(e))
def bstack11l1111ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l1lll1ll_opy_
  global CONFIG
  if bstack11ll11_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢઘ") in options:
    del options[bstack11ll11_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣઙ")]
  bstack1l1llll1_opy_ = bstack1l1ll11l1_opy_()
  for bstack1ll1lll111_opy_ in bstack1l1llll1_opy_.keys():
    path = os.path.join(os.getcwd(), bstack11ll11_opy_ (u"ࠬࡶࡡࡣࡱࡷࡣࡷ࡫ࡳࡶ࡮ࡷࡷࠬચ"), str(bstack1ll1lll111_opy_), bstack11ll11_opy_ (u"࠭࡯ࡶࡶࡳࡹࡹ࠴ࡸ࡮࡮ࠪછ"))
    bstack1lllll11_opy_(path, bstack1111l1111_opy_(bstack1l1llll1_opy_[bstack1ll1lll111_opy_]))
  bstack11llll111_opy_()
  return bstack1l1lll1ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1l11l11l_opy_(self, ff_profile_dir):
  global bstack11l1l1lll_opy_
  if not ff_profile_dir:
    return None
  return bstack11l1l1lll_opy_(self, ff_profile_dir)
def bstack1l1111l1l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11l1l11ll_opy_
  bstack11l1l1l1l_opy_ = []
  if bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪજ") in CONFIG:
    bstack11l1l1l1l_opy_ = CONFIG[bstack11ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫઝ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11ll11_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࠥઞ")],
      pabot_args[bstack11ll11_opy_ (u"ࠥࡺࡪࡸࡢࡰࡵࡨࠦટ")],
      argfile,
      pabot_args.get(bstack11ll11_opy_ (u"ࠦ࡭࡯ࡶࡦࠤઠ")),
      pabot_args[bstack11ll11_opy_ (u"ࠧࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠣડ")],
      platform[0],
      bstack11l1l11ll_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11ll11_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡧ࡫࡯ࡩࡸࠨઢ")] or [(bstack11ll11_opy_ (u"ࠢࠣણ"), None)]
    for platform in enumerate(bstack11l1l1l1l_opy_)
  ]
def bstack1lll1111_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1lll111lll_opy_=bstack11ll11_opy_ (u"ࠨࠩત")):
  global bstack1ll11l1l1_opy_
  self.platform_index = platform_index
  self.bstack1l1l1lll1_opy_ = bstack1lll111lll_opy_
  bstack1ll11l1l1_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1ll1l1ll_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l1ll1l11_opy_
  global bstack1ll1l11l1l_opy_
  if not bstack11ll11_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫથ") in item.options:
    item.options[bstack11ll11_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬદ")] = []
  for v in item.options[bstack11ll11_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ધ")]:
    if bstack11ll11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛ࠫન") in v:
      item.options[bstack11ll11_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ઩")].remove(v)
    if bstack11ll11_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧપ") in v:
      item.options[bstack11ll11_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪફ")].remove(v)
  item.options[bstack11ll11_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫબ")].insert(0, bstack11ll11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙࠼ࡾࢁࠬભ").format(item.platform_index))
  item.options[bstack11ll11_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭મ")].insert(0, bstack11ll11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓ࠼ࡾࢁࠬય").format(item.bstack1l1l1lll1_opy_))
  if bstack1ll1l11l1l_opy_:
    item.options[bstack11ll11_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨર")].insert(0, bstack11ll11_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙࠺ࡼࡿࠪ઱").format(bstack1ll1l11l1l_opy_))
  return bstack1l1ll1l11_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack111llll1_opy_(command, item_index):
  global bstack1ll1l11l1l_opy_
  if bstack1ll1l11l1l_opy_:
    command[0] = command[0].replace(bstack11ll11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧલ"), bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡵࡧ࡯ࠥࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱࠦ࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠥ࠭ળ") + str(
      item_index) + bstack11ll11_opy_ (u"ࠪࠤࠬ઴") + bstack1ll1l11l1l_opy_, 1)
  else:
    command[0] = command[0].replace(bstack11ll11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪવ"),
                                    bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩશ") + str(item_index), 1)
def bstack11lllllll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11lllll1l_opy_
  bstack111llll1_opy_(command, item_index)
  return bstack11lllll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1lllll11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11lllll1l_opy_
  bstack111llll1_opy_(command, item_index)
  return bstack11lllll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack11ll1llll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11lllll1l_opy_
  bstack111llll1_opy_(command, item_index)
  return bstack11lllll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack11l11l1l_opy_(self, runner, quiet=False, capture=True):
  global bstack1111lll1_opy_
  bstack1lllll1l1l_opy_ = bstack1111lll1_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack11ll11_opy_ (u"࠭ࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࡡࡤࡶࡷ࠭ષ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11ll11_opy_ (u"ࠧࡦࡺࡦࡣࡹࡸࡡࡤࡧࡥࡥࡨࡱ࡟ࡢࡴࡵࠫસ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1lllll1l1l_opy_
def bstack11ll1lll1_opy_(self, name, context, *args):
  global bstack111lll1l_opy_
  if name == bstack11ll11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩહ"):
    bstack111lll1l_opy_(self, name, context, *args)
    try:
      if not bstack11l111lll_opy_:
        bstack1ll1l1l1l_opy_ = threading.current_thread().bstackSessionDriver if bstack1llll111l1_opy_(bstack11ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ઺")) else context.browser
        bstack1lll1ll1_opy_ = str(self.feature.name)
        bstack1lll1l1lll_opy_(context, bstack1lll1ll1_opy_)
        bstack1ll1l1l1l_opy_.execute_script(bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨ઻") + json.dumps(bstack1lll1ll1_opy_) + bstack11ll11_opy_ (u"ࠫࢂࢃ઼ࠧ"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack11ll11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤ࡮ࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬઽ").format(str(e)))
  elif name == bstack11ll11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨા"):
    bstack111lll1l_opy_(self, name, context, *args)
    try:
      if not hasattr(self, bstack11ll11_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩિ")):
        self.driver_before_scenario = True
      if (not bstack11l111lll_opy_):
        scenario_name = args[0].name
        feature_name = bstack1lll1ll1_opy_ = str(self.feature.name)
        bstack1lll1ll1_opy_ = feature_name + bstack11ll11_opy_ (u"ࠨࠢ࠰ࠤࠬી") + scenario_name
        bstack1ll1l1l1l_opy_ = threading.current_thread().bstackSessionDriver if bstack1llll111l1_opy_(bstack11ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨુ")) else context.browser
        if self.driver_before_scenario:
          bstack1lll1l1lll_opy_(context, bstack1lll1ll1_opy_)
          bstack1ll1l1l1l_opy_.execute_script(bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨૂ") + json.dumps(bstack1lll1ll1_opy_) + bstack11ll11_opy_ (u"ࠫࢂࢃࠧૃ"))
    except Exception as e:
      logger.debug(bstack11ll11_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤ࡮ࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭ૄ").format(str(e)))
  elif name == bstack11ll11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧૅ"):
    try:
      bstack11l11ll11_opy_ = args[0].status.name
      bstack1ll1l1l1l_opy_ = threading.current_thread().bstackSessionDriver if bstack11ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭૆") in threading.current_thread().__dict__.keys() else context.browser
      if str(bstack11l11ll11_opy_).lower() == bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨે"):
        bstack1l1l1111l_opy_ = bstack11ll11_opy_ (u"ࠩࠪૈ")
        bstack1llllll1l_opy_ = bstack11ll11_opy_ (u"ࠪࠫૉ")
        bstack11ll1l1l1_opy_ = bstack11ll11_opy_ (u"ࠫࠬ૊")
        try:
          import traceback
          bstack1l1l1111l_opy_ = self.exception.__class__.__name__
          bstack1ll1ll1lll_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1llllll1l_opy_ = bstack11ll11_opy_ (u"ࠬࠦࠧો").join(bstack1ll1ll1lll_opy_)
          bstack11ll1l1l1_opy_ = bstack1ll1ll1lll_opy_[-1]
        except Exception as e:
          logger.debug(bstack1ll1llll_opy_.format(str(e)))
        bstack1l1l1111l_opy_ += bstack11ll1l1l1_opy_
        bstack1lll11l1ll_opy_(context, json.dumps(str(args[0].name) + bstack11ll11_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧૌ") + str(bstack1llllll1l_opy_)),
                            bstack11ll11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ્"))
        if self.driver_before_scenario:
          bstack1l111llll_opy_(context, bstack11ll11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ૎"), bstack1l1l1111l_opy_)
          bstack1ll1l1l1l_opy_.execute_script(bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ૏") + json.dumps(str(args[0].name) + bstack11ll11_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤૐ") + str(bstack1llllll1l_opy_)) + bstack11ll11_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫ૑"))
        if self.driver_before_scenario:
          bstack1ll1l1l1l_opy_.execute_script(bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡸࡺࡡࡵࡷࡶࠦ࠿ࠨࡦࡢ࡫࡯ࡩࡩࠨࠬࠡࠤࡵࡩࡦࡹ࡯࡯ࠤ࠽ࠤࠬ૒") + json.dumps(bstack11ll11_opy_ (u"ࠨࡓࡤࡧࡱࡥࡷ࡯࡯ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥ૓") + str(bstack1l1l1111l_opy_)) + bstack11ll11_opy_ (u"ࠧࡾࡿࠪ૔"))
      else:
        bstack1lll11l1ll_opy_(context, bstack11ll11_opy_ (u"ࠣࡒࡤࡷࡸ࡫ࡤࠢࠤ૕"), bstack11ll11_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢ૖"))
        if self.driver_before_scenario:
          bstack1l111llll_opy_(context, bstack11ll11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ૗"))
        bstack1ll1l1l1l_opy_.execute_script(bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ૘") + json.dumps(str(args[0].name) + bstack11ll11_opy_ (u"ࠧࠦ࠭ࠡࡒࡤࡷࡸ࡫ࡤࠢࠤ૙")) + bstack11ll11_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬ૚"))
        if self.driver_before_scenario:
          bstack1ll1l1l1l_opy_.execute_script(bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠣࡲࡤࡷࡸ࡫ࡤࠣࡿࢀࠫ૛"))
    except Exception as e:
      logger.debug(bstack11ll11_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪ૜").format(str(e)))
  elif name == bstack11ll11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩ૝"):
    try:
      bstack1ll1l1l1l_opy_ = threading.current_thread().bstackSessionDriver if bstack1llll111l1_opy_(bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ૞")) else context.browser
      if context.failed is True:
        bstack1l1l1l111_opy_ = []
        bstack1llll111ll_opy_ = []
        bstack1l11l1l1_opy_ = []
        bstack1l1ll1ll1_opy_ = bstack11ll11_opy_ (u"ࠫࠬ૟")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1l1l1l111_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1ll1ll1lll_opy_ = traceback.format_tb(exc_tb)
            bstack1l1l1lll_opy_ = bstack11ll11_opy_ (u"ࠬࠦࠧૠ").join(bstack1ll1ll1lll_opy_)
            bstack1llll111ll_opy_.append(bstack1l1l1lll_opy_)
            bstack1l11l1l1_opy_.append(bstack1ll1ll1lll_opy_[-1])
        except Exception as e:
          logger.debug(bstack1ll1llll_opy_.format(str(e)))
        bstack1l1l1111l_opy_ = bstack11ll11_opy_ (u"࠭ࠧૡ")
        for i in range(len(bstack1l1l1l111_opy_)):
          bstack1l1l1111l_opy_ += bstack1l1l1l111_opy_[i] + bstack1l11l1l1_opy_[i] + bstack11ll11_opy_ (u"ࠧ࡝ࡰࠪૢ")
        bstack1l1ll1ll1_opy_ = bstack11ll11_opy_ (u"ࠨࠢࠪૣ").join(bstack1llll111ll_opy_)
        if not self.driver_before_scenario:
          bstack1lll11l1ll_opy_(context, bstack1l1ll1ll1_opy_, bstack11ll11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ૤"))
          bstack1l111llll_opy_(context, bstack11ll11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ૥"), bstack1l1l1111l_opy_)
          bstack1ll1l1l1l_opy_.execute_script(bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ૦") + json.dumps(bstack1l1ll1ll1_opy_) + bstack11ll11_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬ૧"))
          bstack1ll1l1l1l_opy_.execute_script(bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡧࡣ࡬ࡰࡪࡪࠢ࠭ࠢࠥࡶࡪࡧࡳࡰࡰࠥ࠾ࠥ࠭૨") + json.dumps(bstack11ll11_opy_ (u"ࠢࡔࡱࡰࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵࡳࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢ࡟ࡲࠧ૩") + str(bstack1l1l1111l_opy_)) + bstack11ll11_opy_ (u"ࠨࡿࢀࠫ૪"))
      else:
        if not self.driver_before_scenario:
          bstack1lll11l1ll_opy_(context, bstack11ll11_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧ࠽ࠤࠧ૫") + str(self.feature.name) + bstack11ll11_opy_ (u"ࠥࠤࡵࡧࡳࡴࡧࡧࠥࠧ૬"), bstack11ll11_opy_ (u"ࠦ࡮ࡴࡦࡰࠤ૭"))
          bstack1l111llll_opy_(context, bstack11ll11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ૮"))
          bstack1ll1l1l1l_opy_.execute_script(bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ૯") + json.dumps(bstack11ll11_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥ૰") + str(self.feature.name) + bstack11ll11_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥ૱")) + bstack11ll11_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨ૲"))
          bstack1ll1l1l1l_opy_.execute_script(bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡶࡸࡦࡺࡵࡴࠤ࠽ࠦࡵࡧࡳࡴࡧࡧࠦࢂࢃࠧ૳"))
    except Exception as e:
      logger.debug(bstack11ll11_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭૴").format(str(e)))
  else:
    bstack111lll1l_opy_(self, name, context, *args)
  if name in [bstack11ll11_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ૵"), bstack11ll11_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ૶")]:
    bstack111lll1l_opy_(self, name, context, *args)
    if (name == bstack11ll11_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ૷") and self.driver_before_scenario) or (
            name == bstack11ll11_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ૸") and not self.driver_before_scenario):
      try:
        bstack1ll1l1l1l_opy_ = threading.current_thread().bstackSessionDriver if bstack1llll111l1_opy_(bstack11ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨૹ")) else context.browser
        bstack1ll1l1l1l_opy_.quit()
      except Exception:
        pass
def bstack11llllll_opy_(config, startdir):
  return bstack11ll11_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀ࠶ࡽࠣૺ").format(bstack11ll11_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥૻ"))
notset = Notset()
def bstack1111l1lll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1l1111lll_opy_
  if str(name).lower() == bstack11ll11_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬૼ"):
    return bstack11ll11_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧ૽")
  else:
    return bstack1l1111lll_opy_(self, name, default, skip)
def bstack1l111l11_opy_(item, when):
  global bstack111llll11_opy_
  try:
    bstack111llll11_opy_(item, when)
  except Exception as e:
    pass
def bstack1l11lll1l_opy_():
  return
def bstack1l1ll11ll_opy_(type, name, status, reason, bstack1l11ll11_opy_, bstack1l1l1l11_opy_):
  bstack1ll11l11_opy_ = {
    bstack11ll11_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧ૾"): type,
    bstack11ll11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ૿"): {}
  }
  if type == bstack11ll11_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ଀"):
    bstack1ll11l11_opy_[bstack11ll11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ଁ")][bstack11ll11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪଂ")] = bstack1l11ll11_opy_
    bstack1ll11l11_opy_[bstack11ll11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨଃ")][bstack11ll11_opy_ (u"࠭ࡤࡢࡶࡤࠫ଄")] = json.dumps(str(bstack1l1l1l11_opy_))
  if type == bstack11ll11_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨଅ"):
    bstack1ll11l11_opy_[bstack11ll11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫଆ")][bstack11ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧଇ")] = name
  if type == bstack11ll11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ଈ"):
    bstack1ll11l11_opy_[bstack11ll11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧଉ")][bstack11ll11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬଊ")] = status
    if status == bstack11ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ଋ"):
      bstack1ll11l11_opy_[bstack11ll11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪଌ")][bstack11ll11_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ଍")] = json.dumps(str(reason))
  bstack1l111ll1l_opy_ = bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ଎").format(json.dumps(bstack1ll11l11_opy_))
  return bstack1l111ll1l_opy_
def bstack1llllllll_opy_(item, call, rep):
  global bstack1l1ll111_opy_
  global bstack1llll11l1_opy_
  global bstack11l111lll_opy_
  name = bstack11ll11_opy_ (u"ࠪࠫଏ")
  try:
    if rep.when == bstack11ll11_opy_ (u"ࠫࡨࡧ࡬࡭ࠩଐ"):
      bstack1l11ll1l_opy_ = threading.current_thread().bstack11l1ll1l_opy_
      try:
        if not bstack11l111lll_opy_:
          name = str(rep.nodeid)
          bstack11llll11l_opy_ = bstack1l1ll11ll_opy_(bstack11ll11_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭଑"), name, bstack11ll11_opy_ (u"࠭ࠧ଒"), bstack11ll11_opy_ (u"ࠧࠨଓ"), bstack11ll11_opy_ (u"ࠨࠩଔ"), bstack11ll11_opy_ (u"ࠩࠪକ"))
          for driver in bstack1llll11l1_opy_:
            if bstack1l11ll1l_opy_ == driver.session_id:
              driver.execute_script(bstack11llll11l_opy_)
      except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪଖ").format(str(e)))
      try:
        status = bstack11ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫଗ") if rep.outcome.lower() == bstack11ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬଘ") else bstack11ll11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ଙ")
        reason = bstack11ll11_opy_ (u"ࠧࠨଚ")
        if (reason != bstack11ll11_opy_ (u"ࠣࠤଛ")):
          try:
            if (threading.current_thread().bstackTestErrorMessages == None):
              threading.current_thread().bstackTestErrorMessages = []
          except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
          threading.current_thread().bstackTestErrorMessages.append(str(reason))
        if status == bstack11ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩଜ"):
          reason = rep.longrepr.reprcrash.message
          if (not threading.current_thread().bstackTestErrorMessages):
            threading.current_thread().bstackTestErrorMessages = []
          threading.current_thread().bstackTestErrorMessages.append(reason)
        level = bstack11ll11_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨଝ") if status == bstack11ll11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫଞ") else bstack11ll11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫଟ")
        data = name + bstack11ll11_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨଠ") if status == bstack11ll11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧଡ") else name + bstack11ll11_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠣࠣࠫଢ") + reason
        bstack1lll11ll1l_opy_ = bstack1l1ll11ll_opy_(bstack11ll11_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫଣ"), bstack11ll11_opy_ (u"ࠪࠫତ"), bstack11ll11_opy_ (u"ࠫࠬଥ"), bstack11ll11_opy_ (u"ࠬ࠭ଦ"), level, data)
        for driver in bstack1llll11l1_opy_:
          if bstack1l11ll1l_opy_ == driver.session_id:
            driver.execute_script(bstack1lll11ll1l_opy_)
      except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡴࡴࡴࡦࡺࡷࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪଧ").format(str(e)))
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡷࡹࡧࡴࡦࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽࢀࠫନ").format(str(e)))
  bstack1l1ll111_opy_(item, call, rep)
def bstack1l1lll1l1_opy_(framework_name):
  global bstack1llll1111l_opy_
  global bstack1l1l1ll1l_opy_
  global bstack11ll11111_opy_
  bstack1llll1111l_opy_ = framework_name
  logger.info(bstack11111l11l_opy_.format(bstack1llll1111l_opy_.split(bstack11ll11_opy_ (u"ࠨ࠯ࠪ଩"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1llllll11l_opy_:
      Service.start = bstack111l1lll1_opy_
      Service.stop = bstack11ll1l11l_opy_
      webdriver.Remote.get = bstack111ll1l1_opy_
      WebDriver.close = bstack11ll1l11_opy_
      WebDriver.quit = bstack1ll1lll11l_opy_
      webdriver.Remote.__init__ = bstack11lll1l1_opy_
    if not bstack1llllll11l_opy_ and bstack1llll1111_opy_.on():
      webdriver.Remote.__init__ = bstack1ll1lllll1_opy_
    bstack1l1l1ll1l_opy_ = True
  except Exception as e:
    pass
  bstack11lll111l_opy_()
  if not bstack1l1l1ll1l_opy_:
    bstack11lll1111_opy_(bstack11ll11_opy_ (u"ࠤࡓࡥࡨࡱࡡࡨࡧࡶࠤࡳࡵࡴࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠦପ"), bstack1lll1lll11_opy_)
  if bstack1lll1lll1l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack11l1111l_opy_
    except Exception as e:
      logger.error(bstack111l1111_opy_.format(str(e)))
  if (bstack11ll11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩଫ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1l11l11l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack11l1lllll_opy_
      except Exception as e:
        logger.warn(bstack1111ll1l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1l1lll11l_opy_
      except Exception as e:
        logger.debug(bstack1ll1l1111_opy_ + str(e))
    except Exception as e:
      bstack11lll1111_opy_(e, bstack1111ll1l_opy_)
    Output.end_test = bstack11lll1ll_opy_
    TestStatus.__init__ = bstack1ll111111_opy_
    QueueItem.__init__ = bstack1lll1111_opy_
    pabot._create_items = bstack1l1111l1l_opy_
    try:
      from pabot import __version__ as bstack11ll1ll1_opy_
      if version.parse(bstack11ll1ll1_opy_) >= version.parse(bstack11ll11_opy_ (u"ࠫ࠷࠴࠱࠶࠰࠳ࠫବ")):
        pabot._run = bstack11ll1llll_opy_
      elif version.parse(bstack11ll1ll1_opy_) >= version.parse(bstack11ll11_opy_ (u"ࠬ࠸࠮࠲࠵࠱࠴ࠬଭ")):
        pabot._run = bstack1lllll11l_opy_
      else:
        pabot._run = bstack11lllllll_opy_
    except Exception as e:
      pabot._run = bstack11lllllll_opy_
    pabot._create_command_for_execution = bstack1ll1l1ll_opy_
    pabot._report_results = bstack11l1111ll_opy_
  if bstack11ll11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ମ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11lll1111_opy_(e, bstack1111l111_opy_)
    Runner.run_hook = bstack11ll1lll1_opy_
    Step.run = bstack11l11l1l_opy_
  if bstack11ll11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧଯ") in str(framework_name).lower():
    if not bstack1llllll11l_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack11llllll_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1l11lll1l_opy_
      Config.getoption = bstack1111l1lll_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1llllllll_opy_
    except Exception as e:
      pass
def bstack11l1lll1_opy_():
  global CONFIG
  if bstack11ll11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨର") in CONFIG and int(CONFIG[bstack11ll11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ଱")]) > 1:
    logger.warn(bstack1lll11l11l_opy_)
def bstack1l11l1ll_opy_(arg, bstack1lll1llll_opy_):
  global CONFIG
  global bstack1llll1l11l_opy_
  global bstack1l11111l1_opy_
  global bstack1llllll11l_opy_
  global bstack1ll1l1lll1_opy_
  bstack1l1l1l11l_opy_ = bstack11ll11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪଲ")
  if bstack1lll1llll_opy_ and isinstance(bstack1lll1llll_opy_, str):
    bstack1lll1llll_opy_ = eval(bstack1lll1llll_opy_)
  CONFIG = bstack1lll1llll_opy_[bstack11ll11_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫଳ")]
  bstack1llll1l11l_opy_ = bstack1lll1llll_opy_[bstack11ll11_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭଴")]
  bstack1l11111l1_opy_ = bstack1lll1llll_opy_[bstack11ll11_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨଵ")]
  bstack1llllll11l_opy_ = bstack1lll1llll_opy_[bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪଶ")]
  bstack1ll1l1lll1_opy_.bstack11ll111ll_opy_(bstack11ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩଷ"), bstack1llllll11l_opy_)
  os.environ[bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫସ")] = bstack1l1l1l11l_opy_
  os.environ[bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩହ")] = json.dumps(CONFIG)
  os.environ[bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫ଺")] = bstack1llll1l11l_opy_
  os.environ[bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭଻")] = str(bstack1l11111l1_opy_)
  os.environ[bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡌࡖࡉࡌࡒ଼ࠬ")] = str(True)
  if bstack11l1111l1_opy_(arg, [bstack11ll11_opy_ (u"ࠧ࠮ࡰࠪଽ"), bstack11ll11_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩା")]) != -1:
    os.environ[bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡄࡖࡆࡒࡌࡆࡎࠪି")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1ll1l1l11_opy_)
    return
  bstack1ll11111l_opy_()
  global bstack1ll1l1lll_opy_
  global bstack1lll1111ll_opy_
  global bstack11l1l11ll_opy_
  global bstack1ll1l11l1l_opy_
  global bstack1lllllll11_opy_
  global bstack11ll11111_opy_
  global bstack1ll111ll_opy_
  arg.append(bstack11ll11_opy_ (u"ࠥ࠱࡜ࠨୀ"))
  arg.append(bstack11ll11_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨ࠾ࡒࡵࡤࡶ࡮ࡨࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡯࡭ࡱࡱࡵࡸࡪࡪ࠺ࡱࡻࡷࡩࡸࡺ࠮ࡑࡻࡷࡩࡸࡺࡗࡢࡴࡱ࡭ࡳ࡭ࠢୁ"))
  arg.append(bstack11ll11_opy_ (u"ࠧ࠳ࡗࠣୂ"))
  arg.append(bstack11ll11_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡀࡔࡩࡧࠣ࡬ࡴࡵ࡫ࡪ࡯ࡳࡰࠧୃ"))
  global bstack111l1ll11_opy_
  global bstack11ll11l1_opy_
  global bstack11ll1l1ll_opy_
  global bstack11l1l1lll_opy_
  global bstack1ll11l1l1_opy_
  global bstack1l1ll1l11_opy_
  global bstack11l111ll1_opy_
  global bstack11111ll1l_opy_
  global bstack11ll111l1_opy_
  global bstack1l1111lll_opy_
  global bstack111llll11_opy_
  global bstack1l1ll111_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack111l1ll11_opy_ = webdriver.Remote.__init__
    bstack11ll11l1_opy_ = WebDriver.quit
    bstack11l111ll1_opy_ = WebDriver.close
    bstack11111ll1l_opy_ = WebDriver.get
  except Exception as e:
    pass
  if bstack1l1llll11_opy_(CONFIG):
    if bstack11l1llll_opy_() < version.parse(bstack11111lll1_opy_):
      logger.error(bstack11llllll1_opy_.format(bstack11l1llll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack11ll111l1_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack111l1111_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1l1111lll_opy_ = Config.getoption
    from _pytest import runner
    bstack111llll11_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack111ll1l11_opy_)
  try:
    from pytest_bdd import reporting
    bstack1l1ll111_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack11ll11_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨୄ"))
  bstack11l1l11ll_opy_ = CONFIG.get(bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ୅"), {}).get(bstack11ll11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ୆"))
  bstack1ll111ll_opy_ = True
  bstack1l1lll1l1_opy_(bstack1ll111ll1_opy_)
  os.environ[bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫେ")] = CONFIG[bstack11ll11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ୈ")]
  os.environ[bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨ୉")] = CONFIG[bstack11ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ୊")]
  os.environ[bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪୋ")] = bstack1llllll11l_opy_.__str__()
  from _pytest.config import main as bstack1ll1l11lll_opy_
  bstack1ll1l11lll_opy_(arg)
def bstack1ll111l11_opy_(arg):
  bstack1l1lll1l1_opy_(bstack1lll11l1l1_opy_)
  from behave.__main__ import main as bstack111l1ll1l_opy_
  bstack111l1ll1l_opy_(arg)
def bstack1l11lll1_opy_():
  logger.info(bstack1ll1ll111l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11ll11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧୌ"), help=bstack11ll11_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡴࡴࡦࡪࡩ୍ࠪ"))
  parser.add_argument(bstack11ll11_opy_ (u"ࠪ࠱ࡺ࠭୎"), bstack11ll11_opy_ (u"ࠫ࠲࠳ࡵࡴࡧࡵࡲࡦࡳࡥࠨ୏"), help=bstack11ll11_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫ୐"))
  parser.add_argument(bstack11ll11_opy_ (u"࠭࠭࡬ࠩ୑"), bstack11ll11_opy_ (u"ࠧ࠮࠯࡮ࡩࡾ࠭୒"), help=bstack11ll11_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡧࡣࡤࡧࡶࡷࠥࡱࡥࡺࠩ୓"))
  parser.add_argument(bstack11ll11_opy_ (u"ࠩ࠰ࡪࠬ୔"), bstack11ll11_opy_ (u"ࠪ࠱࠲࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ୕"), help=bstack11ll11_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪୖ"))
  bstack1l1ll1ll_opy_ = parser.parse_args()
  try:
    bstack1111ll1l1_opy_ = bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡮ࡦࡴ࡬ࡧ࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩୗ")
    if bstack1l1ll1ll_opy_.framework and bstack1l1ll1ll_opy_.framework not in (bstack11ll11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭୘"), bstack11ll11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨ୙")):
      bstack1111ll1l1_opy_ = bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࡽࡲࡲ࠮ࡴࡣࡰࡴࡱ࡫ࠧ୚")
    bstack11lll111_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1111ll1l1_opy_)
    bstack1lll111l11_opy_ = open(bstack11lll111_opy_, bstack11ll11_opy_ (u"ࠩࡵࠫ୛"))
    bstack111l1l1ll_opy_ = bstack1lll111l11_opy_.read()
    bstack1lll111l11_opy_.close()
    if bstack1l1ll1ll_opy_.username:
      bstack111l1l1ll_opy_ = bstack111l1l1ll_opy_.replace(bstack11ll11_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪଡ଼"), bstack1l1ll1ll_opy_.username)
    if bstack1l1ll1ll_opy_.key:
      bstack111l1l1ll_opy_ = bstack111l1l1ll_opy_.replace(bstack11ll11_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ଢ଼"), bstack1l1ll1ll_opy_.key)
    if bstack1l1ll1ll_opy_.framework:
      bstack111l1l1ll_opy_ = bstack111l1l1ll_opy_.replace(bstack11ll11_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭୞"), bstack1l1ll1ll_opy_.framework)
    file_name = bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩୟ")
    file_path = os.path.abspath(file_name)
    bstack1llll1lll_opy_ = open(file_path, bstack11ll11_opy_ (u"ࠧࡸࠩୠ"))
    bstack1llll1lll_opy_.write(bstack111l1l1ll_opy_)
    bstack1llll1lll_opy_.close()
    logger.info(bstack11l1l11l_opy_)
    try:
      os.environ[bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪୡ")] = bstack1l1ll1ll_opy_.framework if bstack1l1ll1ll_opy_.framework != None else bstack11ll11_opy_ (u"ࠤࠥୢ")
      config = yaml.safe_load(bstack111l1l1ll_opy_)
      config[bstack11ll11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪୣ")] = bstack11ll11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱ࡸ࡫ࡴࡶࡲࠪ୤")
      bstack1ll1lllll_opy_(bstack1l111l111_opy_, config)
    except Exception as e:
      logger.debug(bstack1lll111l1l_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1ll1l1l1_opy_.format(str(e)))
def bstack1ll1lllll_opy_(bstack11lll1l1l_opy_, config, bstack1l11l111l_opy_={}):
  global bstack1llllll11l_opy_
  if not config:
    return
  bstack1ll1ll11ll_opy_ = bstack1lllll1111_opy_ if not bstack1llllll11l_opy_ else (
    bstack1lll1l1l1_opy_ if bstack11ll11_opy_ (u"ࠬࡧࡰࡱࠩ୥") in config else bstack1l11ll111_opy_)
  data = {
    bstack11ll11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ୦"): config[bstack11ll11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ୧")],
    bstack11ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ୨"): config[bstack11ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ୩")],
    bstack11ll11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ୪"): bstack11lll1l1l_opy_,
    bstack11ll11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ୫"): {
      bstack11ll11_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ୬"): str(config[bstack11ll11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭୭")]) if bstack11ll11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ୮") in config else bstack11ll11_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ୯"),
      bstack11ll11_opy_ (u"ࠩࡵࡩ࡫࡫ࡲࡳࡧࡵࠫ୰"): bstack11l11ll1_opy_(os.getenv(bstack11ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠧୱ"), bstack11ll11_opy_ (u"ࠦࠧ୲"))),
      bstack11ll11_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧ୳"): bstack11ll11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭୴"),
      bstack11ll11_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨ୵"): bstack1ll1ll11ll_opy_,
      bstack11ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ୶"): config[bstack11ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ୷")] if config[bstack11ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭୸")] else bstack11ll11_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧ୹"),
      bstack11ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ୺"): str(config[bstack11ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ୻")]) if bstack11ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ୼") in config else bstack11ll11_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ୽"),
      bstack11ll11_opy_ (u"ࠩࡲࡷࠬ୾"): sys.platform,
      bstack11ll11_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬ୿"): socket.gethostname()
    }
  }
  update(data[bstack11ll11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ஀")], bstack1l11l111l_opy_)
  try:
    response = bstack1l1l1ll1_opy_(bstack11ll11_opy_ (u"ࠬࡖࡏࡔࡖࠪ஁"), bstack11lll1ll1_opy_(bstack1ll1ll11_opy_), data, {
      bstack11ll11_opy_ (u"࠭ࡡࡶࡶ࡫ࠫஂ"): (config[bstack11ll11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩஃ")], config[bstack11ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ஄")])
    })
    if response:
      logger.debug(bstack11l11l1ll_opy_.format(bstack11lll1l1l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1lllll111_opy_.format(str(e)))
def bstack11l11ll1_opy_(framework):
  return bstack11ll11_opy_ (u"ࠤࡾࢁ࠲ࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࡿࢂࠨஅ").format(str(framework), __version__) if framework else bstack11ll11_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࡽࢀࠦஆ").format(
    __version__)
def bstack1ll11111l_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack11l1llll1_opy_()
    logger.debug(bstack1ll111l1l_opy_.format(str(CONFIG)))
    bstack1l1llllll_opy_()
    bstack1ll11l1ll_opy_()
  except Exception as e:
    logger.error(bstack11ll11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵ࠲ࠠࡦࡴࡵࡳࡷࡀࠠࠣஇ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1llll1l1l1_opy_
  atexit.register(bstack111ll11ll_opy_)
  signal.signal(signal.SIGINT, bstack11l1ll111_opy_)
  signal.signal(signal.SIGTERM, bstack11l1ll111_opy_)
def bstack1llll1l1l1_opy_(exctype, value, traceback):
  global bstack1llll11l1_opy_
  try:
    for driver in bstack1llll11l1_opy_:
      driver.execute_script(
        bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡸࡺࡡࡵࡷࡶࠦ࠿ࠨࡦࡢ࡫࡯ࡩࡩࠨࠬࠡࠤࡵࡩࡦࡹ࡯࡯ࠤ࠽ࠤࠬஈ") + json.dumps(
          bstack11ll11_opy_ (u"ࠨࡓࡦࡵࡶ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤஉ") + str(value)) + bstack11ll11_opy_ (u"ࠧࡾࡿࠪஊ"))
  except Exception:
    pass
  bstack111lll1ll_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack111lll1ll_opy_(message=bstack11ll11_opy_ (u"ࠨࠩ஋")):
  global CONFIG
  try:
    if message:
      bstack1l11l111l_opy_ = {
        bstack11ll11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ஌"): str(message)
      }
      bstack1ll1lllll_opy_(bstack1llll11lll_opy_, CONFIG, bstack1l11l111l_opy_)
    else:
      bstack1ll1lllll_opy_(bstack1llll11lll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11l1l1l11_opy_.format(str(e)))
def bstack11ll11l1l_opy_(bstack1l11l11ll_opy_, size):
  bstack1ll1llll1_opy_ = []
  while len(bstack1l11l11ll_opy_) > size:
    bstack1111111l1_opy_ = bstack1l11l11ll_opy_[:size]
    bstack1ll1llll1_opy_.append(bstack1111111l1_opy_)
    bstack1l11l11ll_opy_ = bstack1l11l11ll_opy_[size:]
  bstack1ll1llll1_opy_.append(bstack1l11l11ll_opy_)
  return bstack1ll1llll1_opy_
def bstack1l1lllll_opy_(args):
  if bstack11ll11_opy_ (u"ࠪ࠱ࡲ࠭஍") in args and bstack11ll11_opy_ (u"ࠫࡵࡪࡢࠨஎ") in args:
    return True
  return False
def run_on_browserstack(bstack1l11llll_opy_=None, bstack111llll1l_opy_=None, bstack111lll11l_opy_=False):
  global CONFIG
  global bstack1llll1l11l_opy_
  global bstack1l11111l1_opy_
  bstack1l1l1l11l_opy_ = bstack11ll11_opy_ (u"ࠬ࠭ஏ")
  bstack1l1l111l1_opy_(bstack11l11ll1l_opy_, logger)
  if bstack1l11llll_opy_ and isinstance(bstack1l11llll_opy_, str):
    bstack1l11llll_opy_ = eval(bstack1l11llll_opy_)
  if bstack1l11llll_opy_:
    CONFIG = bstack1l11llll_opy_[bstack11ll11_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭ஐ")]
    bstack1llll1l11l_opy_ = bstack1l11llll_opy_[bstack11ll11_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ஑")]
    bstack1l11111l1_opy_ = bstack1l11llll_opy_[bstack11ll11_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪஒ")]
    bstack1ll1l1lll1_opy_.bstack11ll111ll_opy_(bstack11ll11_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫஓ"), bstack1l11111l1_opy_)
    bstack1l1l1l11l_opy_ = bstack11ll11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪஔ")
  if not bstack111lll11l_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1ll1l1l11_opy_)
      return
    if sys.argv[1] == bstack11ll11_opy_ (u"ࠫ࠲࠳ࡶࡦࡴࡶ࡭ࡴࡴࠧக") or sys.argv[1] == bstack11ll11_opy_ (u"ࠬ࠳ࡶࠨ஖"):
      logger.info(bstack11ll11_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡖࡹࡵࡪࡲࡲ࡙ࠥࡄࡌࠢࡹࡿࢂ࠭஗").format(__version__))
      return
    if sys.argv[1] == bstack11ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭஘"):
      bstack1l11lll1_opy_()
      return
  args = sys.argv
  bstack1ll11111l_opy_()
  global bstack1ll1l1lll_opy_
  global bstack1ll111ll_opy_
  global bstack1l111111_opy_
  global bstack1lll1111ll_opy_
  global bstack11l1l11ll_opy_
  global bstack1ll1l11l1l_opy_
  global bstack1llll11ll_opy_
  global bstack1lllllll11_opy_
  global bstack11ll11111_opy_
  if not bstack1l1l1l11l_opy_:
    if args[1] == bstack11ll11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨங") or args[1] == bstack11ll11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪச"):
      bstack1l1l1l11l_opy_ = bstack11ll11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ஛")
      args = args[2:]
    elif args[1] == bstack11ll11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪஜ"):
      bstack1l1l1l11l_opy_ = bstack11ll11_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ஝")
      args = args[2:]
    elif args[1] == bstack11ll11_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬஞ"):
      bstack1l1l1l11l_opy_ = bstack11ll11_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ட")
      args = args[2:]
    elif args[1] == bstack11ll11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ஠"):
      bstack1l1l1l11l_opy_ = bstack11ll11_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ஡")
      args = args[2:]
    elif args[1] == bstack11ll11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ஢"):
      bstack1l1l1l11l_opy_ = bstack11ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫண")
      args = args[2:]
    elif args[1] == bstack11ll11_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬத"):
      bstack1l1l1l11l_opy_ = bstack11ll11_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭஥")
      args = args[2:]
    else:
      if not bstack11ll11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ஦") in CONFIG or str(CONFIG[bstack11ll11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ஧")]).lower() in [bstack11ll11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩந"), bstack11ll11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫன")]:
        bstack1l1l1l11l_opy_ = bstack11ll11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫப")
        args = args[1:]
      elif str(CONFIG[bstack11ll11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ஫")]).lower() == bstack11ll11_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ஬"):
        bstack1l1l1l11l_opy_ = bstack11ll11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭஭")
        args = args[1:]
      elif str(CONFIG[bstack11ll11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫம")]).lower() == bstack11ll11_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨய"):
        bstack1l1l1l11l_opy_ = bstack11ll11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩர")
        args = args[1:]
      elif str(CONFIG[bstack11ll11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧற")]).lower() == bstack11ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬல"):
        bstack1l1l1l11l_opy_ = bstack11ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ள")
        args = args[1:]
      elif str(CONFIG[bstack11ll11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪழ")]).lower() == bstack11ll11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨவ"):
        bstack1l1l1l11l_opy_ = bstack11ll11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩஶ")
        args = args[1:]
      else:
        os.environ[bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬஷ")] = bstack1l1l1l11l_opy_
        bstack11ll11ll_opy_(bstack1l1l11l11_opy_)
  global bstack11llll1ll_opy_
  if bstack1l11llll_opy_:
    try:
      os.environ[bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ஸ")] = bstack1l1l1l11l_opy_
      bstack1ll1lllll_opy_(bstack111ll11l_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack11l1l1l11_opy_.format(str(e)))
  global bstack111l1ll11_opy_
  global bstack11ll11l1_opy_
  global bstack1lll1l1111_opy_
  global bstack1lll1ll111_opy_
  global bstack1lll11ll_opy_
  global bstack11ll1l1ll_opy_
  global bstack11l1l1lll_opy_
  global bstack11lllll1l_opy_
  global bstack1ll11l1l1_opy_
  global bstack1l1ll1l11_opy_
  global bstack11l111ll1_opy_
  global bstack111lll1l_opy_
  global bstack1111lll1_opy_
  global bstack11111ll1l_opy_
  global bstack11ll111l1_opy_
  global bstack1l1111lll_opy_
  global bstack111llll11_opy_
  global bstack1l1lll1ll_opy_
  global bstack1l1ll111_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack111l1ll11_opy_ = webdriver.Remote.__init__
    bstack11ll11l1_opy_ = WebDriver.quit
    bstack11l111ll1_opy_ = WebDriver.close
    bstack11111ll1l_opy_ = WebDriver.get
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack11llll1ll_opy_ = Popen.__init__
  except Exception as e:
    pass
  if bstack1l1llll11_opy_(CONFIG):
    if bstack11l1llll_opy_() < version.parse(bstack11111lll1_opy_):
      logger.error(bstack11llllll1_opy_.format(bstack11l1llll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack11ll111l1_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack111l1111_opy_.format(str(e)))
  if bstack1l1l1l11l_opy_ != bstack11ll11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬஹ") or (bstack1l1l1l11l_opy_ == bstack11ll11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭஺") and not bstack1l11llll_opy_):
    bstack1l1lll11_opy_()
  if (bstack1l1l1l11l_opy_ in [bstack11ll11_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭஻"), bstack11ll11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ஼"), bstack11ll11_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ஽")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1l11l11l_opy_
        bstack1lll11ll_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1111ll1l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1lll1ll111_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1ll1l1111_opy_ + str(e))
    except Exception as e:
      bstack11lll1111_opy_(e, bstack1111ll1l_opy_)
    if bstack1l1l1l11l_opy_ != bstack11ll11_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫா"):
      bstack11llll111_opy_()
    bstack1lll1l1111_opy_ = Output.end_test
    bstack11ll1l1ll_opy_ = TestStatus.__init__
    bstack11lllll1l_opy_ = pabot._run
    bstack1ll11l1l1_opy_ = QueueItem.__init__
    bstack1l1ll1l11_opy_ = pabot._create_command_for_execution
    bstack1l1lll1ll_opy_ = pabot._report_results
  if bstack1l1l1l11l_opy_ == bstack11ll11_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫி"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11lll1111_opy_(e, bstack1111l111_opy_)
    bstack111lll1l_opy_ = Runner.run_hook
    bstack1111lll1_opy_ = Step.run
  if bstack1l1l1l11l_opy_ == bstack11ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬீ"):
    try:
      bstack1llll1111_opy_.launch(CONFIG, {
        bstack11ll11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠧு"): bstack11ll11_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩூ") if bstack1l1lllll1_opy_() else bstack11ll11_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨ௃"),
        bstack11ll11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭௄"): bstack1lll1111l_opy_.version(),
        bstack11ll11_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ௅"): __version__
      })
      from _pytest.config import Config
      bstack1l1111lll_opy_ = Config.getoption
      from _pytest import runner
      bstack111llll11_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack111ll1l11_opy_)
    try:
      from pytest_bdd import reporting
      bstack1l1ll111_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack11ll11_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬெ"))
  if bstack1l1l1l11l_opy_ == bstack11ll11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬே"):
    bstack1ll111ll_opy_ = True
    if bstack1l11llll_opy_ and bstack111lll11l_opy_:
      bstack11l1l11ll_opy_ = CONFIG.get(bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪை"), {}).get(bstack11ll11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ௉"))
      bstack1l1lll1l1_opy_(bstack1lll11lll_opy_)
    elif bstack1l11llll_opy_:
      bstack11l1l11ll_opy_ = CONFIG.get(bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬொ"), {}).get(bstack11ll11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫோ"))
      global bstack1llll11l1_opy_
      try:
        if bstack1l1lllll_opy_(bstack1l11llll_opy_[bstack11ll11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ௌ")]) and multiprocessing.current_process().name == bstack11ll11_opy_ (u"ࠫ࠵்࠭"):
          bstack1l11llll_opy_[bstack11ll11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ௎")].remove(bstack11ll11_opy_ (u"࠭࠭࡮ࠩ௏"))
          bstack1l11llll_opy_[bstack11ll11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪௐ")].remove(bstack11ll11_opy_ (u"ࠨࡲࡧࡦࠬ௑"))
          bstack1l11llll_opy_[bstack11ll11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ௒")] = bstack1l11llll_opy_[bstack11ll11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭௓")][0]
          with open(bstack1l11llll_opy_[bstack11ll11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ௔")], bstack11ll11_opy_ (u"ࠬࡸࠧ௕")) as f:
            bstack1l11l11l1_opy_ = f.read()
          bstack1lll1l1ll1_opy_ = bstack11ll11_opy_ (u"ࠨࠢࠣࡨࡵࡳࡲࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡤ࡬ࠢ࡬ࡱࡵࡵࡲࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩࡀࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦࠪࡾࢁ࠮ࡁࠠࡧࡴࡲࡱࠥࡶࡤࡣࠢ࡬ࡱࡵࡵࡲࡵࠢࡓࡨࡧࡁࠠࡰࡩࡢࡨࡧࠦ࠽ࠡࡒࡧࡦ࠳ࡪ࡯ࡠࡤࡵࡩࡦࡱ࠻ࠋࡦࡨࡪࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠩࡵࡨࡰ࡫࠲ࠠࡢࡴࡪ࠰ࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࠿ࠣ࠴࠮ࡀࠊࠡࠢࡷࡶࡾࡀࠊࠡࠢࠣࠤࡦࡸࡧࠡ࠿ࠣࡷࡹࡸࠨࡪࡰࡷࠬࡦࡸࡧࠪ࠭࠴࠴࠮ࠐࠠࠡࡧࡻࡧࡪࡶࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡦࡹࠠࡦ࠼ࠍࠤࠥࠦࠠࡱࡣࡶࡷࠏࠦࠠࡰࡩࡢࡨࡧ࠮ࡳࡦ࡮ࡩ࠰ࡦࡸࡧ࠭ࡶࡨࡱࡵࡵࡲࡢࡴࡼ࠭ࠏࡖࡤࡣ࠰ࡧࡳࡤࡨࠠ࠾ࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯ࠏࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮ࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࡓࡨࡧ࠮ࠩ࠯ࡵࡨࡸࡤࡺࡲࡢࡥࡨࠬ࠮ࡢ࡮ࠣࠤࠥ௖").format(str(bstack1l11llll_opy_))
          bstack11l11lll_opy_ = bstack1lll1l1ll1_opy_ + bstack1l11l11l1_opy_
          bstack111l11lll_opy_ = bstack1l11llll_opy_[bstack11ll11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪௗ")] + bstack11ll11_opy_ (u"ࠨࡡࡥࡷࡹࡧࡣ࡬ࡡࡷࡩࡲࡶ࠮ࡱࡻࠪ௘")
          with open(bstack111l11lll_opy_, bstack11ll11_opy_ (u"ࠩࡺࠫ௙")):
            pass
          with open(bstack111l11lll_opy_, bstack11ll11_opy_ (u"ࠥࡻ࠰ࠨ௚")) as f:
            f.write(bstack11l11lll_opy_)
          import subprocess
          bstack1lll1lll1_opy_ = subprocess.run([bstack11ll11_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࠦ௛"), bstack111l11lll_opy_])
          if os.path.exists(bstack111l11lll_opy_):
            os.unlink(bstack111l11lll_opy_)
          os._exit(bstack1lll1lll1_opy_.returncode)
        else:
          if bstack1l1lllll_opy_(bstack1l11llll_opy_[bstack11ll11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ௜")]):
            bstack1l11llll_opy_[bstack11ll11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ௝")].remove(bstack11ll11_opy_ (u"ࠧ࠮࡯ࠪ௞"))
            bstack1l11llll_opy_[bstack11ll11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ௟")].remove(bstack11ll11_opy_ (u"ࠩࡳࡨࡧ࠭௠"))
            bstack1l11llll_opy_[bstack11ll11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭௡")] = bstack1l11llll_opy_[bstack11ll11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ௢")][0]
          bstack1l1lll1l1_opy_(bstack1lll11lll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1l11llll_opy_[bstack11ll11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ௣")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack11ll11_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨ௤")] = bstack11ll11_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠࠩ௥")
          mod_globals[bstack11ll11_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡࠪ௦")] = os.path.abspath(bstack1l11llll_opy_[bstack11ll11_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ௧")])
          exec(open(bstack1l11llll_opy_[bstack11ll11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭௨")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11ll11_opy_ (u"ࠫࡈࡧࡵࡨࡪࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠫ௩").format(str(e)))
          for driver in bstack1llll11l1_opy_:
            bstack111llll1l_opy_.append({
              bstack11ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ௪"): bstack1l11llll_opy_[bstack11ll11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ௫")],
              bstack11ll11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭௬"): str(e),
              bstack11ll11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ௭"): multiprocessing.current_process().name
            })
            driver.execute_script(
              bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩ௮") + json.dumps(
                bstack11ll11_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ௯") + str(e)) + bstack11ll11_opy_ (u"ࠫࢂࢃࠧ௰"))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1llll11l1_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      bstack1ll1l111l_opy_()
      bstack11l1lll1_opy_()
      bstack1lll1llll_opy_ = {
        bstack11ll11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ௱"): args[0],
        bstack11ll11_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭௲"): CONFIG,
        bstack11ll11_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ௳"): bstack1llll1l11l_opy_,
        bstack11ll11_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ௴"): bstack1l11111l1_opy_
      }
      if bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௵") in CONFIG:
        bstack1l11ll1ll_opy_ = []
        manager = multiprocessing.Manager()
        bstack1l111l11l_opy_ = manager.list()
        if bstack1l1lllll_opy_(args):
          for index, platform in enumerate(CONFIG[bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭௶")]):
            if index == 0:
              bstack1lll1llll_opy_[bstack11ll11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ௷")] = args
            bstack1l11ll1ll_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1lll1llll_opy_, bstack1l111l11l_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ௸")]):
            bstack1l11ll1ll_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1lll1llll_opy_, bstack1l111l11l_opy_)))
        for t in bstack1l11ll1ll_opy_:
          t.start()
        for t in bstack1l11ll1ll_opy_:
          t.join()
        bstack1llll11ll_opy_ = list(bstack1l111l11l_opy_)
      else:
        if bstack1l1lllll_opy_(args):
          bstack1lll1llll_opy_[bstack11ll11_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ௹")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1lll1llll_opy_,))
          test.start()
          test.join()
        else:
          bstack1l1lll1l1_opy_(bstack1lll11lll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11ll11_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩ௺")] = bstack11ll11_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡࠪ௻")
          mod_globals[bstack11ll11_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫ௼")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l1l1l11l_opy_ == bstack11ll11_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ௽") or bstack1l1l1l11l_opy_ == bstack11ll11_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ௾"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack11lll1111_opy_(e, bstack1111ll1l_opy_)
    bstack1ll1l111l_opy_()
    bstack1l1lll1l1_opy_(bstack1lll1ll1ll_opy_)
    if bstack11ll11_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ௿") in args:
      i = args.index(bstack11ll11_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫఀ"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1ll1l1lll_opy_))
    args.insert(0, str(bstack11ll11_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬఁ")))
    pabot.main(args)
  elif bstack1l1l1l11l_opy_ == bstack11ll11_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩం"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11lll1111_opy_(e, bstack1111ll1l_opy_)
    for a in args:
      if bstack11ll11_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨః") in a:
        bstack1lll1111ll_opy_ = int(a.split(bstack11ll11_opy_ (u"ࠪ࠾ࠬఄ"))[1])
      if bstack11ll11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨఅ") in a:
        bstack11l1l11ll_opy_ = str(a.split(bstack11ll11_opy_ (u"ࠬࡀࠧఆ"))[1])
      if bstack11ll11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭ఇ") in a:
        bstack1ll1l11l1l_opy_ = str(a.split(bstack11ll11_opy_ (u"ࠧ࠻ࠩఈ"))[1])
    bstack1lllll1l11_opy_ = None
    if bstack11ll11_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧఉ") in args:
      i = args.index(bstack11ll11_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨఊ"))
      args.pop(i)
      bstack1lllll1l11_opy_ = args.pop(i)
    if bstack1lllll1l11_opy_ is not None:
      global bstack1lll1ll11_opy_
      bstack1lll1ll11_opy_ = bstack1lllll1l11_opy_
    bstack1l1lll1l1_opy_(bstack1lll1ll1ll_opy_)
    run_cli(args)
  elif bstack1l1l1l11l_opy_ == bstack11ll11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪఋ"):
    bstack11ll11ll1_opy_ = bstack1lll1111l_opy_(args, logger, CONFIG, bstack1llllll11l_opy_)
    bstack11ll11ll1_opy_.bstack1111l1ll1_opy_()
    bstack1ll1l111l_opy_()
    bstack1l111111_opy_ = True
    bstack11ll11111_opy_ = bstack11ll11ll1_opy_.bstack1lll111111_opy_()
    bstack11ll11ll1_opy_.bstack1lll1llll_opy_(bstack11l111lll_opy_)
    bstack1lllllll11_opy_ = bstack11ll11ll1_opy_.bstack1lll1lllll_opy_(bstack1l11l1ll_opy_, {
      bstack11ll11_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬఌ"): bstack1llll1l11l_opy_,
      bstack11ll11_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ఍"): bstack1l11111l1_opy_,
      bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩఎ"): bstack1llllll11l_opy_
    })
  elif bstack1l1l1l11l_opy_ == bstack11ll11_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧఏ"):
    try:
      from behave.__main__ import main as bstack111l1ll1l_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11lll1111_opy_(e, bstack1111l111_opy_)
    bstack1ll1l111l_opy_()
    bstack1l111111_opy_ = True
    bstack1lll11l11_opy_ = 1
    if bstack11ll11_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨఐ") in CONFIG:
      bstack1lll11l11_opy_ = CONFIG[bstack11ll11_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ఑")]
    bstack1llll1l11_opy_ = int(bstack1lll11l11_opy_) * int(len(CONFIG[bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ఒ")]))
    config = Configuration(args)
    bstack1111ll111_opy_ = config.paths
    if len(bstack1111ll111_opy_) == 0:
      import glob
      pattern = bstack11ll11_opy_ (u"ࠫ࠯࠰࠯ࠫ࠰ࡩࡩࡦࡺࡵࡳࡧࠪఓ")
      bstack1lll1ll1l_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1lll1ll1l_opy_)
      config = Configuration(args)
      bstack1111ll111_opy_ = config.paths
    bstack1l1llll1l_opy_ = [os.path.normpath(item) for item in bstack1111ll111_opy_]
    bstack1l111l1l_opy_ = [os.path.normpath(item) for item in args]
    bstack11111ll11_opy_ = [item for item in bstack1l111l1l_opy_ if item not in bstack1l1llll1l_opy_]
    import platform as pf
    if pf.system().lower() == bstack11ll11_opy_ (u"ࠬࡽࡩ࡯ࡦࡲࡻࡸ࠭ఔ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l1llll1l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1ll1l11ll1_opy_)))
                    for bstack1ll1l11ll1_opy_ in bstack1l1llll1l_opy_]
    bstack1ll1l1l1l1_opy_ = []
    for spec in bstack1l1llll1l_opy_:
      bstack1lllllllll_opy_ = []
      bstack1lllllllll_opy_ += bstack11111ll11_opy_
      bstack1lllllllll_opy_.append(spec)
      bstack1ll1l1l1l1_opy_.append(bstack1lllllllll_opy_)
    execution_items = []
    for bstack1lllllllll_opy_ in bstack1ll1l1l1l1_opy_:
      for index, _ in enumerate(CONFIG[bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩక")]):
        item = {}
        item[bstack11ll11_opy_ (u"ࠧࡢࡴࡪࠫఖ")] = bstack11ll11_opy_ (u"ࠨࠢࠪగ").join(bstack1lllllllll_opy_)
        item[bstack11ll11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨఘ")] = index
        execution_items.append(item)
    bstack1l11lllll_opy_ = bstack11ll11l1l_opy_(execution_items, bstack1llll1l11_opy_)
    for execution_item in bstack1l11lllll_opy_:
      bstack1l11ll1ll_opy_ = []
      for item in execution_item:
        bstack1l11ll1ll_opy_.append(bstack111lllll_opy_(name=str(item[bstack11ll11_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩఙ")]),
                                             target=bstack1ll111l11_opy_,
                                             args=(item[bstack11ll11_opy_ (u"ࠫࡦࡸࡧࠨచ")],)))
      for t in bstack1l11ll1ll_opy_:
        t.start()
      for t in bstack1l11ll1ll_opy_:
        t.join()
  else:
    bstack11ll11ll_opy_(bstack1l1l11l11_opy_)
  if not bstack1l11llll_opy_:
    bstack1ll1ll1ll_opy_()
def browserstack_initialize(bstack1lll1l1l_opy_=None):
  run_on_browserstack(bstack1lll1l1l_opy_, None, True)
def bstack1ll1ll1ll_opy_():
  bstack1llll1111_opy_.stop()
  bstack1llll1111_opy_.bstack1ll1l1ll1_opy_()
  [bstack111l11ll1_opy_, bstack1lll11ll11_opy_] = bstack1ll1ll1111_opy_()
  if bstack111l11ll1_opy_ is not None and bstack1lll1l1ll_opy_() != -1:
    sessions = bstack1l1ll1lll_opy_(bstack111l11ll1_opy_)
    bstack11ll1lll_opy_(sessions, bstack1lll11ll11_opy_)
def bstack11l111ll_opy_(bstack1l1l111ll_opy_):
  if bstack1l1l111ll_opy_:
    return bstack1l1l111ll_opy_.capitalize()
  else:
    return bstack1l1l111ll_opy_
def bstack1lll1l111l_opy_(bstack1111lll1l_opy_):
  if bstack11ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪఛ") in bstack1111lll1l_opy_ and bstack1111lll1l_opy_[bstack11ll11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫజ")] != bstack11ll11_opy_ (u"ࠧࠨఝ"):
    return bstack1111lll1l_opy_[bstack11ll11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ఞ")]
  else:
    bstack1ll111l1_opy_ = bstack11ll11_opy_ (u"ࠤࠥట")
    if bstack11ll11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪఠ") in bstack1111lll1l_opy_ and bstack1111lll1l_opy_[bstack11ll11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫడ")] != None:
      bstack1ll111l1_opy_ += bstack1111lll1l_opy_[bstack11ll11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬఢ")] + bstack11ll11_opy_ (u"ࠨࠬࠡࠤణ")
      if bstack1111lll1l_opy_[bstack11ll11_opy_ (u"ࠧࡰࡵࠪత")] == bstack11ll11_opy_ (u"ࠣ࡫ࡲࡷࠧథ"):
        bstack1ll111l1_opy_ += bstack11ll11_opy_ (u"ࠤ࡬ࡓࡘࠦࠢద")
      bstack1ll111l1_opy_ += (bstack1111lll1l_opy_[bstack11ll11_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧధ")] or bstack11ll11_opy_ (u"ࠫࠬన"))
      return bstack1ll111l1_opy_
    else:
      bstack1ll111l1_opy_ += bstack11l111ll_opy_(bstack1111lll1l_opy_[bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭఩")]) + bstack11ll11_opy_ (u"ࠨࠠࠣప") + (
              bstack1111lll1l_opy_[bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩఫ")] or bstack11ll11_opy_ (u"ࠨࠩబ")) + bstack11ll11_opy_ (u"ࠤ࠯ࠤࠧభ")
      if bstack1111lll1l_opy_[bstack11ll11_opy_ (u"ࠪࡳࡸ࠭మ")] == bstack11ll11_opy_ (u"ࠦ࡜࡯࡮ࡥࡱࡺࡷࠧయ"):
        bstack1ll111l1_opy_ += bstack11ll11_opy_ (u"ࠧ࡝ࡩ࡯ࠢࠥర")
      bstack1ll111l1_opy_ += bstack1111lll1l_opy_[bstack11ll11_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪఱ")] or bstack11ll11_opy_ (u"ࠧࠨల")
      return bstack1ll111l1_opy_
def bstack11lllll1_opy_(bstack11l1l11l1_opy_):
  if bstack11l1l11l1_opy_ == bstack11ll11_opy_ (u"ࠣࡦࡲࡲࡪࠨళ"):
    return bstack11ll11_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾࡬ࡸࡥࡦࡰ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦ࡬ࡸࡥࡦࡰࠥࡂࡈࡵ࡭ࡱ࡮ࡨࡸࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬఴ")
  elif bstack11l1l11l1_opy_ == bstack11ll11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥవ"):
    return bstack11ll11_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡲࡦࡦ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡷ࡫ࡤࠣࡀࡉࡥ࡮ࡲࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧశ")
  elif bstack11l1l11l1_opy_ == bstack11ll11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧష"):
    return bstack11ll11_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡩࡵࡩࡪࡴ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡩࡵࡩࡪࡴࠢ࠿ࡒࡤࡷࡸ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭స")
  elif bstack11l1l11l1_opy_ == bstack11ll11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨహ"):
    return bstack11ll11_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡶࡪࡪ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡴࡨࡨࠧࡄࡅࡳࡴࡲࡶࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ఺")
  elif bstack11l1l11l1_opy_ == bstack11ll11_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ఻"):
    return bstack11ll11_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࠩࡥࡦࡣ࠶࠶࠻ࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࠤࡧࡨࡥ࠸࠸࠶ࠣࡀࡗ࡭ࡲ࡫࡯ࡶࡶ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ఼")
  elif bstack11l1l11l1_opy_ == bstack11ll11_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠧఽ"):
    return bstack11ll11_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡣ࡮ࡤࡧࡰࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡣ࡮ࡤࡧࡰࠨ࠾ࡓࡷࡱࡲ࡮ࡴࡧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ా")
  else:
    return bstack11ll11_opy_ (u"࠭࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࠪి") + bstack11l111ll_opy_(
      bstack11l1l11l1_opy_) + bstack11ll11_opy_ (u"ࠧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ీ")
def bstack1ll1l1ll1l_opy_(session):
  return bstack11ll11_opy_ (u"ࠨ࠾ࡷࡶࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡸ࡯ࡸࠤࡁࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠥࡹࡥࡴࡵ࡬ࡳࡳ࠳࡮ࡢ࡯ࡨࠦࡃࡂࡡࠡࡪࡵࡩ࡫ࡃࠢࡼࡿࠥࠤࡹࡧࡲࡨࡧࡷࡁࠧࡥࡢ࡭ࡣࡱ࡯ࠧࡄࡻࡾ࠾࠲ࡥࡃࡂ࠯ࡵࡦࡁࡿࢂࢁࡽ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿࠳ࡹࡸ࠾ࠨు").format(
    session[bstack11ll11_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭ూ")], bstack1lll1l111l_opy_(session), bstack11lllll1_opy_(session[bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡸࡦࡺࡵࡴࠩృ")]),
    bstack11lllll1_opy_(session[bstack11ll11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫౄ")]),
    bstack11l111ll_opy_(session[bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭౅")] or session[bstack11ll11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ె")] or bstack11ll11_opy_ (u"ࠧࠨే")) + bstack11ll11_opy_ (u"ࠣࠢࠥై") + (session[bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ౉")] or bstack11ll11_opy_ (u"ࠪࠫొ")),
    session[bstack11ll11_opy_ (u"ࠫࡴࡹࠧో")] + bstack11ll11_opy_ (u"ࠧࠦࠢౌ") + session[bstack11ll11_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰ్ࠪ")], session[bstack11ll11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ౎")] or bstack11ll11_opy_ (u"ࠨࠩ౏"),
    session[bstack11ll11_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭౐")] if session[bstack11ll11_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺࠧ౑")] else bstack11ll11_opy_ (u"ࠫࠬ౒"))
def bstack11ll1lll_opy_(sessions, bstack1lll11ll11_opy_):
  try:
    bstack11111l11_opy_ = bstack11ll11_opy_ (u"ࠧࠨ౓")
    if not os.path.exists(bstack11111l1ll_opy_):
      os.mkdir(bstack11111l1ll_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11ll11_opy_ (u"࠭ࡡࡴࡵࡨࡸࡸ࠵ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫ౔")), bstack11ll11_opy_ (u"ࠧࡳౕࠩ")) as f:
      bstack11111l11_opy_ = f.read()
    bstack11111l11_opy_ = bstack11111l11_opy_.replace(bstack11ll11_opy_ (u"ࠨࡽࠨࡖࡊ࡙ࡕࡍࡖࡖࡣࡈࡕࡕࡏࡖࠨࢁౖࠬ"), str(len(sessions)))
    bstack11111l11_opy_ = bstack11111l11_opy_.replace(bstack11ll11_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠥࡾࠩ౗"), bstack1lll11ll11_opy_)
    bstack11111l11_opy_ = bstack11111l11_opy_.replace(bstack11ll11_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠧࢀࠫౘ"),
                                              sessions[0].get(bstack11ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡦࡳࡥࠨౙ")) if sessions[0] else bstack11ll11_opy_ (u"ࠬ࠭ౚ"))
    with open(os.path.join(bstack11111l1ll_opy_, bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪ౛")), bstack11ll11_opy_ (u"ࠧࡸࠩ౜")) as stream:
      stream.write(bstack11111l11_opy_.split(bstack11ll11_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬౝ"))[0])
      for session in sessions:
        stream.write(bstack1ll1l1ll1l_opy_(session))
      stream.write(bstack11111l11_opy_.split(bstack11ll11_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ࠭౞"))[1])
    logger.info(bstack11ll11_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࡩࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡨࡵࡪ࡮ࡧࠤࡦࡸࡴࡪࡨࡤࡧࡹࡹࠠࡢࡶࠣࡿࢂ࠭౟").format(bstack11111l1ll_opy_));
  except Exception as e:
    logger.debug(bstack1ll1l11l1_opy_.format(str(e)))
def bstack1l1ll1lll_opy_(bstack111l11ll1_opy_):
  global CONFIG
  try:
    host = bstack11ll11_opy_ (u"ࠫࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪࠧౠ") if bstack11ll11_opy_ (u"ࠬࡧࡰࡱࠩౡ") in CONFIG else bstack11ll11_opy_ (u"࠭ࡡࡱ࡫ࠪౢ")
    user = CONFIG[bstack11ll11_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩౣ")]
    key = CONFIG[bstack11ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ౤")]
    bstack11lll11l_opy_ = bstack11ll11_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨ౥") if bstack11ll11_opy_ (u"ࠪࡥࡵࡶࠧ౦") in CONFIG else bstack11ll11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭౧")
    url = bstack11ll11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࢁࡽ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡪࡹࡳࡪࡱࡱࡷ࠳ࡰࡳࡰࡰࠪ౨").format(user, key, host, bstack11lll11l_opy_,
                                                                                bstack111l11ll1_opy_)
    headers = {
      bstack11ll11_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬ౩"): bstack11ll11_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ౪"),
    }
    proxies = bstack11ll1l111_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack11ll11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭౫")], response.json()))
  except Exception as e:
    logger.debug(bstack1llll11l1l_opy_.format(str(e)))
def bstack1ll1ll1111_opy_():
  global CONFIG
  try:
    if bstack11ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ౬") in CONFIG:
      host = bstack11ll11_opy_ (u"ࠪࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠭౭") if bstack11ll11_opy_ (u"ࠫࡦࡶࡰࠨ౮") in CONFIG else bstack11ll11_opy_ (u"ࠬࡧࡰࡪࠩ౯")
      user = CONFIG[bstack11ll11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ౰")]
      key = CONFIG[bstack11ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ౱")]
      bstack11lll11l_opy_ = bstack11ll11_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ౲") if bstack11ll11_opy_ (u"ࠩࡤࡴࡵ࠭౳") in CONFIG else bstack11ll11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ౴")
      url = bstack11ll11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࢀࢃ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠴ࡪࡴࡱࡱࠫ౵").format(user, key, host, bstack11lll11l_opy_)
      headers = {
        bstack11ll11_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ౶"): bstack11ll11_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ౷"),
      }
      if bstack11ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ౸") in CONFIG:
        params = {bstack11ll11_opy_ (u"ࠨࡰࡤࡱࡪ࠭౹"): CONFIG[bstack11ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ౺")], bstack11ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭౻"): CONFIG[bstack11ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭౼")]}
      else:
        params = {bstack11ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ౽"): CONFIG[bstack11ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ౾")]}
      proxies = bstack11ll1l111_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack111111111_opy_ = response.json()[0][bstack11ll11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡧࡻࡩ࡭ࡦࠪ౿")]
        if bstack111111111_opy_:
          bstack1lll11ll11_opy_ = bstack111111111_opy_[bstack11ll11_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬಀ")].split(bstack11ll11_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤ࠯ࡥࡹ࡮ࡲࡤࠨಁ"))[0] + bstack11ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡵ࠲ࠫಂ") + bstack111111111_opy_[
            bstack11ll11_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧಃ")]
          logger.info(bstack1ll1llll11_opy_.format(bstack1lll11ll11_opy_))
          bstack1l1l11ll_opy_ = CONFIG[bstack11ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ಄")]
          if bstack11ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨಅ") in CONFIG:
            bstack1l1l11ll_opy_ += bstack11ll11_opy_ (u"ࠧࠡࠩಆ") + CONFIG[bstack11ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪಇ")]
          if bstack1l1l11ll_opy_ != bstack111111111_opy_[bstack11ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧಈ")]:
            logger.debug(bstack11l11lll1_opy_.format(bstack111111111_opy_[bstack11ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨಉ")], bstack1l1l11ll_opy_))
          return [bstack111111111_opy_[bstack11ll11_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧಊ")], bstack1lll11ll11_opy_]
    else:
      logger.warn(bstack1lll11ll1_opy_)
  except Exception as e:
    logger.debug(bstack1ll1111l1_opy_.format(str(e)))
  return [None, None]
def bstack1lll1l11_opy_(url, bstack1l11l1l11_opy_=False):
  global CONFIG
  global bstack1lll111l_opy_
  if not bstack1lll111l_opy_:
    hostname = bstack1lll1lll_opy_(url)
    is_private = bstack1ll1l1llll_opy_(hostname)
    if (bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩಋ") in CONFIG and not CONFIG[bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪಌ")]) and (is_private or bstack1l11l1l11_opy_):
      bstack1lll111l_opy_ = hostname
def bstack1lll1lll_opy_(url):
  return urlparse(url).hostname
def bstack1ll1l1llll_opy_(hostname):
  for bstack11lll1lll_opy_ in bstack1llllll111_opy_:
    regex = re.compile(bstack11lll1lll_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1llll111l1_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False