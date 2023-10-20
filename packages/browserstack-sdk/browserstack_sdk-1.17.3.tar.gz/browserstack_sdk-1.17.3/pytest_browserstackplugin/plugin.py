# coding: UTF-8
import sys
bstack1l1ll1l_opy_ = sys.version_info [0] == 2
bstack11lll1_opy_ = 2048
bstack111111l_opy_ = 7
def bstack11l1l1_opy_ (bstack1llll1l_opy_):
    global bstack1l11_opy_
    bstack1111ll1_opy_ = ord (bstack1llll1l_opy_ [-1])
    bstack1111l11_opy_ = bstack1llll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack1111ll1_opy_ % len (bstack1111l11_opy_)
    bstack1lllllll_opy_ = bstack1111l11_opy_ [:bstack11l1l11_opy_] + bstack1111l11_opy_ [bstack11l1l11_opy_:]
    if bstack1l1ll1l_opy_:
        bstack11l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack11lll1_opy_ - (bstack1l11ll1_opy_ + bstack1111ll1_opy_) % bstack111111l_opy_) for bstack1l11ll1_opy_, char in enumerate (bstack1lllllll_opy_)])
    else:
        bstack11l11l_opy_ = str () .join ([chr (ord (char) - bstack11lll1_opy_ - (bstack1l11ll1_opy_ + bstack1111ll1_opy_) % bstack111111l_opy_) for bstack1l11ll1_opy_, char in enumerate (bstack1lllllll_opy_)])
    return eval (bstack11l11l_opy_)
import atexit
import datetime
import inspect
import logging
import os
import sys
import threading
from uuid import uuid4
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack11l11lll1_opy_, bstack1ll1llll1_opy_, update, bstack11l11l111_opy_,
                                       bstack1llll11l1l_opy_, bstack111llll1l_opy_, bstack11lllll11_opy_, bstack1llllll1ll_opy_,
                                       bstack1l111ll1l_opy_, bstack111l111ll_opy_, bstack1l1l1l11_opy_, bstack1lll111ll_opy_,
                                       bstack1lll1l1ll_opy_)
from browserstack_sdk._version import __version__
from bstack_utils.capture import bstack1ll11l1ll1_opy_
from bstack_utils.constants import bstack1l1lll1l1_opy_, bstack111l111l1_opy_, bstack111lllll_opy_, bstack1l1l11111_opy_, \
    bstack1l1111l11_opy_
from bstack_utils.helper import bstack1l1ll1l11l_opy_, bstack1ll1111ll1_opy_, bstack1l11lll11_opy_, bstack1l1lll1l1l_opy_, \
    bstack1l1ll1l1l1_opy_, bstack11ll11l1l_opy_, bstack1lll1lll11_opy_, bstack1l1lll11ll_opy_, bstack1l1llll11_opy_, Notset, \
    bstack1ll11l111_opy_, bstack1ll111111l_opy_, bstack1l1lll11l1_opy_, Result, bstack1ll111l1l1_opy_, bstack1l1llllll1_opy_, bstack1ll11111l1_opy_
from bstack_utils.bstack1l1l1lll1l_opy_ import bstack1l1ll111l1_opy_
from bstack_utils.messages import bstack1llll1l11l_opy_, bstack1ll1l111_opy_, bstack1llllllll_opy_, bstack1l1ll111l_opy_, bstack111llllll_opy_, \
    bstack1111llll1_opy_, bstack11111l11l_opy_, bstack1llllll1l_opy_, bstack1111l111_opy_, bstack1lll1l11l1_opy_, \
    bstack1l1ll1l1l_opy_, bstack1ll111ll_opy_
from bstack_utils.proxy import bstack1ll1l111l_opy_, bstack1l111lll_opy_
from bstack_utils.bstack1l1l111l1l_opy_ import bstack1l1l111ll1_opy_, bstack1l11llll11_opy_, bstack1l1l1111l1_opy_, \
    bstack1l11lllll1_opy_, bstack1l1l111111_opy_, bstack1l1l11111l_opy_
from bstack_utils.bstack1l11l1l1ll_opy_ import bstack1l11l1ll1l_opy_
from bstack_utils.bstack1l11l11lll_opy_ import bstack1l1ll1l11_opy_, bstack11lll111l_opy_, bstack11ll1l1ll_opy_
from bstack_utils.bstack1l111l1l1l_opy_ import bstack1l111l111l_opy_
from bstack_utils.bstack1ll1l11l_opy_ import bstack1lll11ll11_opy_
bstack1llll111_opy_ = None
bstack1lll11l111_opy_ = None
bstack1ll1l1ll_opy_ = None
bstack1l11ll111_opy_ = None
bstack1l11ll1l1_opy_ = None
bstack1lll1llll1_opy_ = None
bstack1ll1lll111_opy_ = None
bstack11lll1l1_opy_ = None
bstack11llll111_opy_ = None
bstack1ll1l1l111_opy_ = None
bstack1lll1111l1_opy_ = None
bstack1ll1ll1111_opy_ = None
bstack11111l1l1_opy_ = None
bstack1ll11llll_opy_ = bstack11l1l1_opy_ (u"ࠪࠫም")
CONFIG = {}
bstack111l1lll_opy_ = False
bstack11l11ll1_opy_ = bstack11l1l1_opy_ (u"ࠫࠬሞ")
bstack1lll111111_opy_ = bstack11l1l1_opy_ (u"ࠬ࠭ሟ")
bstack1ll1l1l11l_opy_ = False
bstack1111lll1l_opy_ = []
bstack11l1lllll_opy_ = bstack111l111l1_opy_
bstack11ll1l11l1_opy_ = bstack11l1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ሠ")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack11l1lllll_opy_,
                    format=bstack11l1l1_opy_ (u"ࠧ࡝ࡰࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷࠬሡ"),
                    datefmt=bstack11l1l1_opy_ (u"ࠨࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪሢ"),
                    stream=sys.stdout)
store = {
    bstack11l1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ሣ"): []
}
def bstack1l11l11ll_opy_():
    global CONFIG
    global bstack11l1lllll_opy_
    if bstack11l1l1_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬሤ") in CONFIG:
        bstack11l1lllll_opy_ = bstack1l1lll1l1_opy_[CONFIG[bstack11l1l1_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ሥ")]]
        logging.getLogger().setLevel(bstack11l1lllll_opy_)
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11ll1lllll_opy_ = {}
bstack11lll1ll1l_opy_ = None
def bstack111l11ll_opy_(page, bstack1l11111l1_opy_):
    try:
        page.evaluate(bstack11l1l1_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨሦ"),
                      bstack11l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪሧ") + json.dumps(
                          bstack1l11111l1_opy_) + bstack11l1l1_opy_ (u"ࠢࡾࡿࠥረ"))
    except Exception as e:
        print(bstack11l1l1_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨሩ"), e)
def bstack1lllll1l1l_opy_(page, message, level):
    try:
        page.evaluate(bstack11l1l1_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥሪ"), bstack11l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨራ") + json.dumps(
            message) + bstack11l1l1_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧሬ") + json.dumps(level) + bstack11l1l1_opy_ (u"ࠬࢃࡽࠨር"))
    except Exception as e:
        print(bstack11l1l1_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾࠤሮ"), e)
def bstack1llll1111_opy_(page, status, message=bstack11l1l1_opy_ (u"ࠢࠣሯ")):
    try:
        if (status == bstack11l1l1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣሰ")):
            page.evaluate(bstack11l1l1_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥሱ"),
                          bstack11l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡵࡩࡦࡹ࡯࡯ࠤ࠽ࠫሲ") + json.dumps(
                              bstack11l1l1_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࠨሳ") + str(message)) + bstack11l1l1_opy_ (u"ࠬ࠲ࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠩሴ") + json.dumps(status) + bstack11l1l1_opy_ (u"ࠨࡽࡾࠤስ"))
        else:
            page.evaluate(bstack11l1l1_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣሶ"),
                          bstack11l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠩሷ") + json.dumps(
                              status) + bstack11l1l1_opy_ (u"ࠤࢀࢁࠧሸ"))
    except Exception as e:
        print(bstack11l1l1_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤࢀࢃࠢሹ"), e)
def pytest_configure(config):
    config.args = bstack1lll11ll11_opy_.bstack11llll11l1_opy_(config.args)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack11ll1l1111_opy_ = item.config.getoption(bstack11l1l1_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ሺ"))
    plugins = item.config.getoption(bstack11l1l1_opy_ (u"ࠧࡶ࡬ࡶࡩ࡬ࡲࡸࠨሻ"))
    report = outcome.get_result()
    bstack11ll1l11ll_opy_(item, call, report)
    if bstack11l1l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠦሼ") not in plugins or bstack1l1llll11_opy_():
        return
    summary = []
    driver = getattr(item, bstack11l1l1_opy_ (u"ࠢࡠࡦࡵ࡭ࡻ࡫ࡲࠣሽ"), None)
    page = getattr(item, bstack11l1l1_opy_ (u"ࠣࡡࡳࡥ࡬࡫ࠢሾ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack11ll1ll1l1_opy_(item, report, summary, bstack11ll1l1111_opy_)
    if (page is not None):
        bstack11ll11ll11_opy_(item, report, summary, bstack11ll1l1111_opy_)
def bstack11ll1ll1l1_opy_(item, report, summary, bstack11ll1l1111_opy_):
    if report.when in [bstack11l1l1_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣሿ"), bstack11l1l1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧቀ")]:
        return
    if not bstack1ll1111ll1_opy_():
        return
    try:
        if (str(bstack11ll1l1111_opy_).lower() != bstack11l1l1_opy_ (u"ࠫࡹࡸࡵࡦࠩቁ")):
            item._driver.execute_script(
                bstack11l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪቂ") + json.dumps(
                    report.nodeid) + bstack11l1l1_opy_ (u"࠭ࡽࡾࠩቃ"))
    except Exception as e:
        summary.append(
            bstack11l1l1_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦ࠼ࠣࡿ࠵ࢃࠢቄ").format(e)
        )
    passed = report.passed or (report.failed and hasattr(report, bstack11l1l1_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥቅ")))
    bstack11llllll1_opy_ = bstack11l1l1_opy_ (u"ࠤࠥቆ")
    if not passed:
        try:
            bstack11llllll1_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11l1l1_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥቇ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11llllll1_opy_))
    try:
        if passed:
            item._driver.execute_script(
                bstack11l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭ቈ")
                + json.dumps(bstack11l1l1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠦࠨ቉"))
                + bstack11l1l1_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣቊ")
            )
        else:
            item._driver.execute_script(
                bstack11l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪቋ")
                + json.dumps(str(bstack11llllll1_opy_))
                + bstack11l1l1_opy_ (u"ࠣ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥቌ")
            )
    except Exception as e:
        summary.append(bstack11l1l1_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡢࡰࡱࡳࡹࡧࡴࡦ࠼ࠣࡿ࠵ࢃࠢቍ").format(e))
def bstack11ll11ll11_opy_(item, report, summary, bstack11ll1l1111_opy_):
    if report.when in [bstack11l1l1_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤ቎"), bstack11l1l1_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨ቏")]:
        return
    if (str(bstack11ll1l1111_opy_).lower() != bstack11l1l1_opy_ (u"ࠬࡺࡲࡶࡧࠪቐ")):
        bstack111l11ll_opy_(item._page, report.nodeid)
    passed = report.passed or (report.failed and hasattr(report, bstack11l1l1_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣቑ")))
    bstack11llllll1_opy_ = bstack11l1l1_opy_ (u"ࠢࠣቒ")
    if not passed:
        try:
            bstack11llllll1_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11l1l1_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣቓ").format(e)
            )
    try:
        if passed:
            bstack1llll1111_opy_(item._page, bstack11l1l1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤቔ"))
        else:
            if bstack11llllll1_opy_:
                bstack1lllll1l1l_opy_(item._page, str(bstack11llllll1_opy_), bstack11l1l1_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤቕ"))
                bstack1llll1111_opy_(item._page, bstack11l1l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦቖ"), str(bstack11llllll1_opy_))
            else:
                bstack1llll1111_opy_(item._page, bstack11l1l1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ቗"))
    except Exception as e:
        summary.append(bstack11l1l1_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻ࠱ࡿࠥቘ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack11l1l1_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ቙"), default=bstack11l1l1_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢቚ"), help=bstack11l1l1_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣቛ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11l1l1_opy_ (u"ࠥ࠱࠲ࡪࡲࡪࡸࡨࡶࠧቜ"), action=bstack11l1l1_opy_ (u"ࠦࡸࡺ࡯ࡳࡧࠥቝ"), default=bstack11l1l1_opy_ (u"ࠧࡩࡨࡳࡱࡰࡩࠧ቞"),
                         help=bstack11l1l1_opy_ (u"ࠨࡄࡳ࡫ࡹࡩࡷࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷࠧ቟"))
def bstack11lll11ll1_opy_(log):
    if not (log[bstack11l1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨበ")] and log[bstack11l1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩቡ")].strip()):
        return
    active = bstack11lll111ll_opy_()
    log = {
        bstack11l1l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨቢ"): log[bstack11l1l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩባ")],
        bstack11l1l1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧቤ"): datetime.datetime.utcnow().isoformat() + bstack11l1l1_opy_ (u"ࠬࡠࠧብ"),
        bstack11l1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧቦ"): log[bstack11l1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨቧ")],
    }
    if active:
        if active[bstack11l1l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭ቨ")] == bstack11l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧቩ"):
            log[bstack11l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪቪ")] = active[bstack11l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫቫ")]
        elif active[bstack11l1l1_opy_ (u"ࠬࡺࡹࡱࡧࠪቬ")] == bstack11l1l1_opy_ (u"࠭ࡴࡦࡵࡷࠫቭ"):
            log[bstack11l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧቮ")] = active[bstack11l1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨቯ")]
    bstack1lll11ll11_opy_.bstack11llllll1l_opy_([log])
def bstack11lll111ll_opy_():
    if len(store[bstack11l1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ተ")]) > 0 and store[bstack11l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧቱ")][-1]:
        return {
            bstack11l1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩቲ"): bstack11l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪታ"),
            bstack11l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ቴ"): store[bstack11l1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫት")][-1]
        }
    if store.get(bstack11l1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬቶ"), None):
        return {
            bstack11l1l1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧቷ"): bstack11l1l1_opy_ (u"ࠪࡸࡪࡹࡴࠨቸ"),
            bstack11l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫቹ"): store[bstack11l1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩቺ")]
        }
    return None
bstack11lll11l1l_opy_ = bstack1ll11l1ll1_opy_(bstack11lll11ll1_opy_)
def pytest_runtest_call(item):
    try:
        if not bstack1lll11ll11_opy_.on() or bstack11ll1l11l1_opy_ != bstack11l1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ቻ"):
            return
        global bstack11lll1ll1l_opy_, bstack11lll11l1l_opy_
        bstack11lll11l1l_opy_.start()
        bstack11ll1ll111_opy_ = {
            bstack11l1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬቼ"): uuid4().__str__(),
            bstack11l1l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬች"): datetime.datetime.utcnow().isoformat() + bstack11l1l1_opy_ (u"ࠩ࡝ࠫቾ")
        }
        bstack11lll1ll1l_opy_ = bstack11ll1ll111_opy_[bstack11l1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨቿ")]
        store[bstack11l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨኀ")] = bstack11ll1ll111_opy_[bstack11l1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪኁ")]
        threading.current_thread().bstack11lll1ll1l_opy_ = bstack11lll1ll1l_opy_
        _11ll1lllll_opy_[item.nodeid] = {**_11ll1lllll_opy_[item.nodeid], **bstack11ll1ll111_opy_}
        bstack11ll11ll1l_opy_(item, _11ll1lllll_opy_[item.nodeid], bstack11l1l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧኂ"))
    except Exception as err:
        print(bstack11l1l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡤࡣ࡯ࡰ࠿ࠦࡻࡾࠩኃ"), str(err))
def pytest_runtest_setup(item):
    if bstack1l1lll11ll_opy_():
        atexit.register(bstack1l111lll1_opy_)
    try:
        if not bstack1lll11ll11_opy_.on():
            return
        bstack11lll11l1l_opy_.start()
        uuid = uuid4().__str__()
        bstack11ll1ll111_opy_ = {
            bstack11l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ኄ"): uuid,
            bstack11l1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ኅ"): datetime.datetime.utcnow().isoformat() + bstack11l1l1_opy_ (u"ࠪ࡞ࠬኆ"),
            bstack11l1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩኇ"): bstack11l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪኈ"),
            bstack11l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ኉"): bstack11l1l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬኊ"),
            bstack11l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫኋ"): bstack11l1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨኌ")
        }
        threading.current_thread().bstack11ll11l1ll_opy_ = uuid
        store[bstack11l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧኍ")] = item
        store[bstack11l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ኎")] = [uuid]
        if not _11ll1lllll_opy_.get(item.nodeid, None):
            _11ll1lllll_opy_[item.nodeid] = {bstack11l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ኏"): [], bstack11l1l1_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨነ"): []}
        _11ll1lllll_opy_[item.nodeid][bstack11l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ኑ")].append(bstack11ll1ll111_opy_[bstack11l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ኒ")])
        _11ll1lllll_opy_[item.nodeid + bstack11l1l1_opy_ (u"ࠩ࠰ࡷࡪࡺࡵࡱࠩና")] = bstack11ll1ll111_opy_
        bstack11ll1ll1ll_opy_(item, bstack11ll1ll111_opy_, bstack11l1l1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫኔ"))
    except Exception as err:
        print(bstack11l1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧን"), str(err))
def pytest_runtest_teardown(item):
    try:
        if not bstack1lll11ll11_opy_.on():
            return
        bstack11ll1ll111_opy_ = {
            bstack11l1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪኖ"): uuid4().__str__(),
            bstack11l1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪኗ"): datetime.datetime.utcnow().isoformat() + bstack11l1l1_opy_ (u"࡛ࠧࠩኘ"),
            bstack11l1l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭ኙ"): bstack11l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧኚ"),
            bstack11l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ኛ"): bstack11l1l1_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨኜ"),
            bstack11l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨኝ"): bstack11l1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨኞ")
        }
        _11ll1lllll_opy_[item.nodeid + bstack11l1l1_opy_ (u"ࠧ࠮ࡶࡨࡥࡷࡪ࡯ࡸࡰࠪኟ")] = bstack11ll1ll111_opy_
        bstack11ll1ll1ll_opy_(item, bstack11ll1ll111_opy_, bstack11l1l1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩአ"))
    except Exception as err:
        print(bstack11l1l1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱ࠾ࠥࢁࡽࠨኡ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1lll11ll11_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1l1l1111l1_opy_(fixturedef.argname):
        store[bstack11l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡲࡵࡤࡶ࡮ࡨࡣ࡮ࡺࡥ࡮ࠩኢ")] = request.node
    elif bstack1l11lllll1_opy_(fixturedef.argname):
        store[bstack11l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩኣ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack11l1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪኤ"): fixturedef.argname,
            bstack11l1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭እ"): bstack1l1lll1l1l_opy_(outcome),
            bstack11l1l1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩኦ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        bstack11lll111l1_opy_ = store[bstack11l1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬኧ")]
        if not _11ll1lllll_opy_.get(bstack11lll111l1_opy_.nodeid, None):
            _11ll1lllll_opy_[bstack11lll111l1_opy_.nodeid] = {bstack11l1l1_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫከ"): []}
        _11ll1lllll_opy_[bstack11lll111l1_opy_.nodeid][bstack11l1l1_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬኩ")].append(fixture)
    except Exception as err:
        logger.debug(bstack11l1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧኪ"), str(err))
if bstack1l1llll11_opy_() and bstack1lll11ll11_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _11ll1lllll_opy_[request.node.nodeid][bstack11l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨካ")].bstack1l111ll1l1_opy_(id(step))
        except Exception as err:
            print(bstack11l1l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶ࠺ࠡࡽࢀࠫኬ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _11ll1lllll_opy_[request.node.nodeid][bstack11l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪክ")].bstack1l11l11l1l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11l1l1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬኮ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack1l111l1l1l_opy_: bstack1l111l111l_opy_ = _11ll1lllll_opy_[request.node.nodeid][bstack11l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬኯ")]
            bstack1l111l1l1l_opy_.bstack1l11l11l1l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11l1l1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧኰ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack11ll1l11l1_opy_
        try:
            if not bstack1lll11ll11_opy_.on() or bstack11ll1l11l1_opy_ != bstack11l1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨ኱"):
                return
            global bstack11lll11l1l_opy_
            bstack11lll11l1l_opy_.start()
            if not _11ll1lllll_opy_.get(request.node.nodeid, None):
                _11ll1lllll_opy_[request.node.nodeid] = {}
            bstack1l111l1l1l_opy_ = bstack1l111l111l_opy_.bstack1l111lll1l_opy_(
                scenario, feature, request.node,
                name=bstack1l1l111111_opy_(request.node, scenario),
                bstack1l111l1111_opy_=bstack1l11lll11_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11l1l1_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧኲ"),
                tags=bstack1l1l11111l_opy_(feature, scenario)
            )
            _11ll1lllll_opy_[request.node.nodeid][bstack11l1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩኳ")] = bstack1l111l1l1l_opy_
            bstack11lll1111l_opy_(bstack1l111l1l1l_opy_.uuid)
            bstack1lll11ll11_opy_.bstack11llll11ll_opy_(bstack11l1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨኴ"), bstack1l111l1l1l_opy_)
        except Exception as err:
            print(bstack11l1l1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪኵ"), str(err))
def bstack11ll1lll11_opy_(bstack11ll11lll1_opy_):
    if bstack11ll11lll1_opy_ in store[bstack11l1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭኶")]:
        store[bstack11l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ኷")].remove(bstack11ll11lll1_opy_)
def bstack11lll1111l_opy_(bstack11ll1l111l_opy_):
    store[bstack11l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨኸ")] = bstack11ll1l111l_opy_
    threading.current_thread().bstack11lll1ll1l_opy_ = bstack11ll1l111l_opy_
@bstack1lll11ll11_opy_.bstack11lllll111_opy_
def bstack11ll1l11ll_opy_(item, call, report):
    global bstack11ll1l11l1_opy_
    try:
        if report.when == bstack11l1l1_opy_ (u"ࠬࡩࡡ࡭࡮ࠪኹ"):
            bstack11lll11l1l_opy_.reset()
        if report.when == bstack11l1l1_opy_ (u"࠭ࡣࡢ࡮࡯ࠫኺ"):
            if bstack11ll1l11l1_opy_ == bstack11l1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧኻ"):
                _11ll1lllll_opy_[item.nodeid][bstack11l1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ኼ")] = bstack1ll111l1l1_opy_(report.stop)
                bstack11ll11ll1l_opy_(item, _11ll1lllll_opy_[item.nodeid], bstack11l1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫኽ"), report, call)
                store[bstack11l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧኾ")] = None
            elif bstack11ll1l11l1_opy_ == bstack11l1l1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣ኿"):
                bstack1l111l1l1l_opy_ = _11ll1lllll_opy_[item.nodeid][bstack11l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨዀ")]
                bstack1l111l1l1l_opy_.set(hooks=_11ll1lllll_opy_[item.nodeid].get(bstack11l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ዁"), []))
                exception, bstack1l1lll111l_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l1lll111l_opy_ = [call.excinfo.exconly(), report.longreprtext]
                bstack1l111l1l1l_opy_.stop(time=bstack1ll111l1l1_opy_(report.stop), result=Result(result=report.outcome, exception=exception, bstack1l1lll111l_opy_=bstack1l1lll111l_opy_))
                bstack1lll11ll11_opy_.bstack11llll11ll_opy_(bstack11l1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩዂ"), _11ll1lllll_opy_[item.nodeid][bstack11l1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫዃ")])
        elif report.when in [bstack11l1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨዄ"), bstack11l1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬዅ")]:
            bstack11ll1ll11l_opy_ = item.nodeid + bstack11l1l1_opy_ (u"ࠫ࠲࠭዆") + report.when
            if report.skipped:
                hook_type = bstack11l1l1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ዇") if report.when == bstack11l1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬወ") else bstack11l1l1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫዉ")
                _11ll1lllll_opy_[bstack11ll1ll11l_opy_] = {
                    bstack11l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ዊ"): uuid4().__str__(),
                    bstack11l1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ዋ"): datetime.datetime.utcfromtimestamp(report.start).isoformat() + bstack11l1l1_opy_ (u"ࠪ࡞ࠬዌ"),
                    bstack11l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧው"): hook_type
                }
            _11ll1lllll_opy_[bstack11ll1ll11l_opy_][bstack11l1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪዎ")] = datetime.datetime.utcfromtimestamp(report.stop).isoformat() + bstack11l1l1_opy_ (u"࡚࠭ࠨዏ")
            bstack11ll1lll11_opy_(_11ll1lllll_opy_[bstack11ll1ll11l_opy_][bstack11l1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬዐ")])
            bstack11ll1ll1ll_opy_(item, _11ll1lllll_opy_[bstack11ll1ll11l_opy_], bstack11l1l1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪዑ"), report, call)
            if report.when == bstack11l1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨዒ"):
                if report.outcome == bstack11l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪዓ"):
                    bstack11ll1ll111_opy_ = {
                        bstack11l1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩዔ"): uuid4().__str__(),
                        bstack11l1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩዕ"): bstack1l11lll11_opy_(),
                        bstack11l1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫዖ"): bstack1l11lll11_opy_()
                    }
                    _11ll1lllll_opy_[item.nodeid] = {**_11ll1lllll_opy_[item.nodeid], **bstack11ll1ll111_opy_}
                    bstack11ll11ll1l_opy_(item, _11ll1lllll_opy_[item.nodeid], bstack11l1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ዗"))
                    bstack11ll11ll1l_opy_(item, _11ll1lllll_opy_[item.nodeid], bstack11l1l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪዘ"), report, call)
    except Exception as err:
        print(bstack11l1l1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࢀࢃࠧዙ"), str(err))
def bstack11ll1l1ll1_opy_(test, bstack11ll1ll111_opy_, result=None, call=None, bstack11l1llll1_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1l111l1l1l_opy_ = {
        bstack11l1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨዚ"): bstack11ll1ll111_opy_[bstack11l1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩዛ")],
        bstack11l1l1_opy_ (u"ࠬࡺࡹࡱࡧࠪዜ"): bstack11l1l1_opy_ (u"࠭ࡴࡦࡵࡷࠫዝ"),
        bstack11l1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬዞ"): test.name,
        bstack11l1l1_opy_ (u"ࠨࡤࡲࡨࡾ࠭ዟ"): {
            bstack11l1l1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧዠ"): bstack11l1l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪዡ"),
            bstack11l1l1_opy_ (u"ࠫࡨࡵࡤࡦࠩዢ"): inspect.getsource(test.obj)
        },
        bstack11l1l1_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩዣ"): test.name,
        bstack11l1l1_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬዤ"): test.name,
        bstack11l1l1_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧዥ"): bstack1lll11ll11_opy_.bstack11llll1111_opy_(test),
        bstack11l1l1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫዦ"): file_path,
        bstack11l1l1_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫዧ"): file_path,
        bstack11l1l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪየ"): bstack11l1l1_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬዩ"),
        bstack11l1l1_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪዪ"): file_path,
        bstack11l1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪያ"): bstack11ll1ll111_opy_[bstack11l1l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫዬ")],
        bstack11l1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫይ"): bstack11l1l1_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩዮ"),
        bstack11l1l1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭ዯ"): {
            bstack11l1l1_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨደ"): test.nodeid
        },
        bstack11l1l1_opy_ (u"ࠬࡺࡡࡨࡵࠪዱ"): bstack1l1ll1l1l1_opy_(test.own_markers)
    }
    if bstack11l1llll1_opy_ in [bstack11l1l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧዲ"), bstack11l1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩዳ")]:
        bstack1l111l1l1l_opy_[bstack11l1l1_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭ዴ")] = {
            bstack11l1l1_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫድ"): bstack11ll1ll111_opy_.get(bstack11l1l1_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬዶ"), [])
        }
    if bstack11l1llll1_opy_ == bstack11l1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬዷ"):
        bstack1l111l1l1l_opy_[bstack11l1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬዸ")] = bstack11l1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧዹ")
        bstack1l111l1l1l_opy_[bstack11l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ዺ")] = bstack11ll1ll111_opy_[bstack11l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧዻ")]
        bstack1l111l1l1l_opy_[bstack11l1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧዼ")] = bstack11ll1ll111_opy_[bstack11l1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨዽ")]
    if result:
        bstack1l111l1l1l_opy_[bstack11l1l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫዾ")] = result.outcome
        bstack1l111l1l1l_opy_[bstack11l1l1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ዿ")] = result.duration * 1000
        bstack1l111l1l1l_opy_[bstack11l1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫጀ")] = bstack11ll1ll111_opy_[bstack11l1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬጁ")]
        if result.failed:
            bstack1l111l1l1l_opy_[bstack11l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧጂ")] = bstack1lll11ll11_opy_.bstack1ll11111ll_opy_(call.excinfo.typename)
            bstack1l111l1l1l_opy_[bstack11l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪጃ")] = bstack1lll11ll11_opy_.bstack11llll111l_opy_(call.excinfo, result)
        bstack1l111l1l1l_opy_[bstack11l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩጄ")] = bstack11ll1ll111_opy_[bstack11l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪጅ")]
    if outcome:
        bstack1l111l1l1l_opy_[bstack11l1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬጆ")] = bstack1l1lll1l1l_opy_(outcome)
        bstack1l111l1l1l_opy_[bstack11l1l1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧጇ")] = 0
        bstack1l111l1l1l_opy_[bstack11l1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬገ")] = bstack11ll1ll111_opy_[bstack11l1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ጉ")]
        if bstack1l111l1l1l_opy_[bstack11l1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩጊ")] == bstack11l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪጋ"):
            bstack1l111l1l1l_opy_[bstack11l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪጌ")] = bstack11l1l1_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭ግ")  # bstack11lll1l1ll_opy_
            bstack1l111l1l1l_opy_[bstack11l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧጎ")] = [{bstack11l1l1_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪጏ"): [bstack11l1l1_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬጐ")]}]
        bstack1l111l1l1l_opy_[bstack11l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ጑")] = bstack11ll1ll111_opy_[bstack11l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩጒ")]
    return bstack1l111l1l1l_opy_
def bstack11ll11l111_opy_(test, bstack11lll1l111_opy_, bstack11l1llll1_opy_, result, call, outcome, bstack11ll1lll1l_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack11lll1l111_opy_[bstack11l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧጓ")]
    hook_name = bstack11lll1l111_opy_[bstack11l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨጔ")]
    hook_data = {
        bstack11l1l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫጕ"): bstack11lll1l111_opy_[bstack11l1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ጖")],
        bstack11l1l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭጗"): bstack11l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧጘ"),
        bstack11l1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨጙ"): bstack11l1l1_opy_ (u"ࠫࢀࢃࠧጚ").format(bstack1l1l111ll1_opy_(hook_name)),
        bstack11l1l1_opy_ (u"ࠬࡨ࡯ࡥࡻࠪጛ"): {
            bstack11l1l1_opy_ (u"࠭࡬ࡢࡰࡪࠫጜ"): bstack11l1l1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧጝ"),
            bstack11l1l1_opy_ (u"ࠨࡥࡲࡨࡪ࠭ጞ"): None
        },
        bstack11l1l1_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨጟ"): test.name,
        bstack11l1l1_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪጠ"): bstack1lll11ll11_opy_.bstack11llll1111_opy_(test, hook_name),
        bstack11l1l1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧጡ"): file_path,
        bstack11l1l1_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧጢ"): file_path,
        bstack11l1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ጣ"): bstack11l1l1_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨጤ"),
        bstack11l1l1_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭ጥ"): file_path,
        bstack11l1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ጦ"): bstack11lll1l111_opy_[bstack11l1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧጧ")],
        bstack11l1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧጨ"): bstack11l1l1_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧጩ") if bstack11ll1l11l1_opy_ == bstack11l1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪጪ") else bstack11l1l1_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧጫ"),
        bstack11l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫጬ"): hook_type
    }
    bstack11ll1l1l11_opy_ = bstack11ll1l1l1l_opy_(_11ll1lllll_opy_.get(test.nodeid, None))
    if bstack11ll1l1l11_opy_:
        hook_data[bstack11l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣ࡮ࡪࠧጭ")] = bstack11ll1l1l11_opy_
    if result:
        hook_data[bstack11l1l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪጮ")] = result.outcome
        hook_data[bstack11l1l1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬጯ")] = result.duration * 1000
        hook_data[bstack11l1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪጰ")] = bstack11lll1l111_opy_[bstack11l1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫጱ")]
        if result.failed:
            hook_data[bstack11l1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ጲ")] = bstack1lll11ll11_opy_.bstack1ll11111ll_opy_(call.excinfo.typename)
            hook_data[bstack11l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩጳ")] = bstack1lll11ll11_opy_.bstack11llll111l_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11l1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩጴ")] = bstack1l1lll1l1l_opy_(outcome)
        hook_data[bstack11l1l1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫጵ")] = 100
        hook_data[bstack11l1l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩጶ")] = bstack11lll1l111_opy_[bstack11l1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪጷ")]
        if hook_data[bstack11l1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ጸ")] == bstack11l1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧጹ"):
            hook_data[bstack11l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧጺ")] = bstack11l1l1_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪጻ")  # bstack11lll1l1ll_opy_
            hook_data[bstack11l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫጼ")] = [{bstack11l1l1_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧጽ"): [bstack11l1l1_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩጾ")]}]
    if bstack11ll1lll1l_opy_:
        hook_data[bstack11l1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ጿ")] = bstack11ll1lll1l_opy_.result
        hook_data[bstack11l1l1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨፀ")] = bstack1ll111111l_opy_(bstack11lll1l111_opy_[bstack11l1l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬፁ")], bstack11lll1l111_opy_[bstack11l1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧፂ")])
        hook_data[bstack11l1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨፃ")] = bstack11lll1l111_opy_[bstack11l1l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩፄ")]
        if hook_data[bstack11l1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬፅ")] == bstack11l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ፆ"):
            hook_data[bstack11l1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ፇ")] = bstack1lll11ll11_opy_.bstack1ll11111ll_opy_(bstack11ll1lll1l_opy_.exception_type)
            hook_data[bstack11l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩፈ")] = [{bstack11l1l1_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬፉ"): bstack1l1lll11l1_opy_(bstack11ll1lll1l_opy_.exception)}]
    return hook_data
def bstack11ll11ll1l_opy_(test, bstack11ll1ll111_opy_, bstack11l1llll1_opy_, result=None, call=None, outcome=None):
    bstack1l111l1l1l_opy_ = bstack11ll1l1ll1_opy_(test, bstack11ll1ll111_opy_, result, call, bstack11l1llll1_opy_, outcome)
    driver = getattr(test, bstack11l1l1_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫፊ"), None)
    if bstack11l1llll1_opy_ == bstack11l1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬፋ") and driver:
        bstack1l111l1l1l_opy_[bstack11l1l1_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫፌ")] = bstack1lll11ll11_opy_.bstack11llll1ll1_opy_(driver)
    if bstack11l1llll1_opy_ == bstack11l1l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧፍ"):
        bstack11l1llll1_opy_ = bstack11l1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩፎ")
    bstack11lll1ll11_opy_ = {
        bstack11l1l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬፏ"): bstack11l1llll1_opy_,
        bstack11l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫፐ"): bstack1l111l1l1l_opy_
    }
    bstack1lll11ll11_opy_.bstack1l1111ll11_opy_(bstack11lll1ll11_opy_)
def bstack11ll1ll1ll_opy_(test, bstack11ll1ll111_opy_, bstack11l1llll1_opy_, result=None, call=None, outcome=None, bstack11ll1lll1l_opy_=None):
    hook_data = bstack11ll11l111_opy_(test, bstack11ll1ll111_opy_, bstack11l1llll1_opy_, result, call, outcome, bstack11ll1lll1l_opy_)
    bstack11lll1ll11_opy_ = {
        bstack11l1l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧፑ"): bstack11l1llll1_opy_,
        bstack11l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳ࠭ፒ"): hook_data
    }
    bstack1lll11ll11_opy_.bstack1l1111ll11_opy_(bstack11lll1ll11_opy_)
def bstack11ll1l1l1l_opy_(bstack11ll1ll111_opy_):
    if not bstack11ll1ll111_opy_:
        return None
    if bstack11ll1ll111_opy_.get(bstack11l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨፓ"), None):
        return getattr(bstack11ll1ll111_opy_[bstack11l1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩፔ")], bstack11l1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬፕ"), None)
    return bstack11ll1ll111_opy_.get(bstack11l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ፖ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1lll11ll11_opy_.on():
            return
        places = [bstack11l1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨፗ"), bstack11l1l1_opy_ (u"ࠪࡧࡦࡲ࡬ࠨፘ"), bstack11l1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ፙ")]
        bstack11llll1lll_opy_ = []
        for bstack11ll11l1l1_opy_ in places:
            records = caplog.get_records(bstack11ll11l1l1_opy_)
            bstack11lll11111_opy_ = bstack11l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬፚ") if bstack11ll11l1l1_opy_ == bstack11l1l1_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ፛") else bstack11l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ፜")
            bstack11ll11l11l_opy_ = request.node.nodeid + (bstack11l1l1_opy_ (u"ࠨࠩ፝") if bstack11ll11l1l1_opy_ == bstack11l1l1_opy_ (u"ࠩࡦࡥࡱࡲࠧ፞") else bstack11l1l1_opy_ (u"ࠪ࠱ࠬ፟") + bstack11ll11l1l1_opy_)
            bstack11ll1l111l_opy_ = bstack11ll1l1l1l_opy_(_11ll1lllll_opy_.get(bstack11ll11l11l_opy_, None))
            if not bstack11ll1l111l_opy_:
                continue
            for record in records:
                if bstack1l1llllll1_opy_(record.message):
                    continue
                bstack11llll1lll_opy_.append({
                    bstack11l1l1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ፠"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack11l1l1_opy_ (u"ࠬࡠࠧ፡"),
                    bstack11l1l1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ።"): record.levelname,
                    bstack11l1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ፣"): record.message,
                    bstack11lll11111_opy_: bstack11ll1l111l_opy_
                })
        if len(bstack11llll1lll_opy_) > 0:
            bstack1lll11ll11_opy_.bstack11llllll1l_opy_(bstack11llll1lll_opy_)
    except Exception as err:
        print(bstack11l1l1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡦࡳࡳࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥ࠻ࠢࡾࢁࠬ፤"), str(err))
def bstack11lll1l1l1_opy_(driver_command, response):
    if driver_command == bstack11l1l1_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭፥"):
        bstack1lll11ll11_opy_.bstack1l11111l11_opy_({
            bstack11l1l1_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩ፦"): response[bstack11l1l1_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪ፧")],
            bstack11l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ፨"): store[bstack11l1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ፩")]
        })
def bstack1l111lll1_opy_():
    global bstack1111lll1l_opy_
    bstack1lll11ll11_opy_.bstack11lllll1ll_opy_()
    for driver in bstack1111lll1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1llll1ll1l_opy_(self, *args, **kwargs):
    bstack111ll111_opy_ = bstack1llll111_opy_(self, *args, **kwargs)
    bstack1lll11ll11_opy_.bstack1ll1l1l1ll_opy_(self)
    return bstack111ll111_opy_
def bstack1ll1ll1ll_opy_(framework_name):
    global bstack1ll11llll_opy_
    global bstack1lll1ll1l_opy_
    bstack1ll11llll_opy_ = framework_name
    logger.info(bstack1ll111ll_opy_.format(bstack1ll11llll_opy_.split(bstack11l1l1_opy_ (u"ࠧ࠮ࠩ፪"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1ll1111ll1_opy_():
            Service.start = bstack11lllll11_opy_
            Service.stop = bstack1llllll1ll_opy_
            webdriver.Remote.__init__ = bstack1llll1ll1_opy_
            webdriver.Remote.get = bstack111l1l1l_opy_
            if not isinstance(os.getenv(bstack11l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡃࡕࡅࡑࡒࡅࡍࠩ፫")), str):
                return
            WebDriver.close = bstack1l111ll1l_opy_
            WebDriver.quit = bstack11l1l111l_opy_
        if not bstack1ll1111ll1_opy_() and bstack1lll11ll11_opy_.on():
            webdriver.Remote.__init__ = bstack1llll1ll1l_opy_
        bstack1lll1ll1l_opy_ = True
    except Exception as e:
        pass
    bstack1ll1l1ll11_opy_()
    if os.environ.get(bstack11l1l1_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧ፬")):
        bstack1lll1ll1l_opy_ = eval(os.environ.get(bstack11l1l1_opy_ (u"ࠪࡗࡊࡒࡅࡏࡋࡘࡑࡤࡕࡒࡠࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡏࡎࡔࡖࡄࡐࡑࡋࡄࠨ፭")))
    if not bstack1lll1ll1l_opy_:
        bstack1l1l1l11_opy_(bstack11l1l1_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨ፮"), bstack1l1ll1l1l_opy_)
    if bstack1lll111ll1_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1lll1l1l1_opy_
        except Exception as e:
            logger.error(bstack1111llll1_opy_.format(str(e)))
    if bstack11l1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ፯") in str(framework_name).lower():
        if not bstack1ll1111ll1_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1llll11l1l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack111llll1l_opy_
            Config.getoption = bstack1l1llll1_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack11l111lll_opy_
        except Exception as e:
            pass
def bstack11l1l111l_opy_(self):
    global bstack1ll11llll_opy_
    global bstack111111ll1_opy_
    global bstack1lll11l111_opy_
    try:
        if bstack11l1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭፰") in bstack1ll11llll_opy_ and self.session_id != None:
            bstack11l1l111_opy_ = bstack11l1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ፱") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ፲")
            bstack1llll1lll_opy_ = bstack1l1ll1l11_opy_(bstack11l1l1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ፳"), bstack11l1l1_opy_ (u"ࠪࠫ፴"), bstack11l1l111_opy_, bstack11l1l1_opy_ (u"ࠫ࠱ࠦࠧ፵").join(
                threading.current_thread().bstackTestErrorMessages), bstack11l1l1_opy_ (u"ࠬ࠭፶"), bstack11l1l1_opy_ (u"࠭ࠧ፷"))
            if self != None:
                self.execute_script(bstack1llll1lll_opy_)
    except Exception as e:
        logger.debug(bstack11l1l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡵࡣࡷࡹࡸࡀࠠࠣ፸") + str(e))
    bstack1lll11l111_opy_(self)
    self.session_id = None
def bstack1llll1ll1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack111111ll1_opy_
    global bstack11l111ll_opy_
    global bstack1ll1l1l11l_opy_
    global bstack1ll11llll_opy_
    global bstack1llll111_opy_
    global bstack1111lll1l_opy_
    global bstack11l11ll1_opy_
    global bstack1lll111111_opy_
    CONFIG[bstack11l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ፹")] = str(bstack1ll11llll_opy_) + str(__version__)
    command_executor = bstack1lll1lll11_opy_(bstack11l11ll1_opy_)
    logger.debug(bstack1l1ll111l_opy_.format(command_executor))
    proxy = bstack1lll1l1ll_opy_(CONFIG, proxy)
    bstack1ll1l1l1l_opy_ = 0
    try:
        if bstack1ll1l1l11l_opy_ is True:
            bstack1ll1l1l1l_opy_ = int(os.environ.get(bstack11l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ፺")))
    except:
        bstack1ll1l1l1l_opy_ = 0
    bstack1ll111lll_opy_ = bstack11l11lll1_opy_(CONFIG, bstack1ll1l1l1l_opy_)
    logger.debug(bstack1llllll1l_opy_.format(str(bstack1ll111lll_opy_)))
    if bstack11l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ፻") in CONFIG and CONFIG[bstack11l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ፼")]:
        bstack11ll1l1ll_opy_(bstack1ll111lll_opy_, bstack1lll111111_opy_)
    if desired_capabilities:
        bstack11l1ll111_opy_ = bstack1ll1llll1_opy_(desired_capabilities)
        bstack11l1ll111_opy_[bstack11l1l1_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ፽")] = bstack1ll11l111_opy_(CONFIG)
        bstack11ll11ll1_opy_ = bstack11l11lll1_opy_(bstack11l1ll111_opy_)
        if bstack11ll11ll1_opy_:
            bstack1ll111lll_opy_ = update(bstack11ll11ll1_opy_, bstack1ll111lll_opy_)
        desired_capabilities = None
    if options:
        bstack111l111ll_opy_(options, bstack1ll111lll_opy_)
    if not options:
        options = bstack11l11l111_opy_(bstack1ll111lll_opy_)
    if proxy and bstack11ll11l1l_opy_() >= version.parse(bstack11l1l1_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭፾")):
        options.proxy(proxy)
    if options and bstack11ll11l1l_opy_() >= version.parse(bstack11l1l1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭፿")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack11ll11l1l_opy_() < version.parse(bstack11l1l1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᎀ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1ll111lll_opy_)
    logger.info(bstack1llllllll_opy_)
    if bstack11ll11l1l_opy_() >= version.parse(bstack11l1l1_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩᎁ")):
        bstack1llll111_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11ll11l1l_opy_() >= version.parse(bstack11l1l1_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩᎂ")):
        bstack1llll111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11ll11l1l_opy_() >= version.parse(bstack11l1l1_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫᎃ")):
        bstack1llll111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1llll111_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1ll1l1l1l1_opy_ = bstack11l1l1_opy_ (u"ࠬ࠭ᎄ")
        if bstack11ll11l1l_opy_() >= version.parse(bstack11l1l1_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧᎅ")):
            bstack1ll1l1l1l1_opy_ = self.caps.get(bstack11l1l1_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢᎆ"))
        else:
            bstack1ll1l1l1l1_opy_ = self.capabilities.get(bstack11l1l1_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣᎇ"))
        if bstack1ll1l1l1l1_opy_:
            if bstack11ll11l1l_opy_() <= version.parse(bstack11l1l1_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩᎈ")):
                self.command_executor._url = bstack11l1l1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᎉ") + bstack11l11ll1_opy_ + bstack11l1l1_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣᎊ")
            else:
                self.command_executor._url = bstack11l1l1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᎋ") + bstack1ll1l1l1l1_opy_ + bstack11l1l1_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢᎌ")
            logger.debug(bstack1ll1l111_opy_.format(bstack1ll1l1l1l1_opy_))
        else:
            logger.debug(bstack1llll1l11l_opy_.format(bstack11l1l1_opy_ (u"ࠢࡐࡲࡷ࡭ࡲࡧ࡬ࠡࡊࡸࡦࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣᎍ")))
    except Exception as e:
        logger.debug(bstack1llll1l11l_opy_.format(e))
    bstack111111ll1_opy_ = self.session_id
    if bstack11l1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᎎ") in bstack1ll11llll_opy_:
        threading.current_thread().bstack11l1111l_opy_ = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        bstack1lll11ll11_opy_.bstack1ll1l1l1ll_opy_(self)
    bstack1111lll1l_opy_.append(self)
    if bstack11l1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᎏ") in CONFIG and bstack11l1l1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ᎐") in CONFIG[bstack11l1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᎑")][bstack1ll1l1l1l_opy_]:
        bstack11l111ll_opy_ = CONFIG[bstack11l1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ᎒")][bstack1ll1l1l1l_opy_][bstack11l1l1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ᎓")]
    logger.debug(bstack1lll1l11l1_opy_.format(bstack111111ll1_opy_))
def bstack111l1l1l_opy_(self, url):
    global bstack11llll111_opy_
    global CONFIG
    try:
        bstack11lll111l_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1111l111_opy_.format(str(err)))
    try:
        bstack11llll111_opy_(self, url)
    except Exception as e:
        try:
            bstack111ll111l_opy_ = str(e)
            if any(err_msg in bstack111ll111l_opy_ for err_msg in bstack1l1l11111_opy_):
                bstack11lll111l_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1111l111_opy_.format(str(err)))
        raise e
def bstack1l1l1ll1_opy_(item, when):
    global bstack1ll1ll1111_opy_
    try:
        bstack1ll1ll1111_opy_(item, when)
    except Exception as e:
        pass
def bstack11l111lll_opy_(item, call, rep):
    global bstack11111l1l1_opy_
    global bstack1111lll1l_opy_
    name = bstack11l1l1_opy_ (u"ࠧࠨ᎔")
    try:
        if rep.when == bstack11l1l1_opy_ (u"ࠨࡥࡤࡰࡱ࠭᎕"):
            bstack111111ll1_opy_ = threading.current_thread().bstack11l1111l_opy_
            bstack11ll1l1111_opy_ = item.config.getoption(bstack11l1l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ᎖"))
            try:
                if (str(bstack11ll1l1111_opy_).lower() != bstack11l1l1_opy_ (u"ࠪࡸࡷࡻࡥࠨ᎗")):
                    name = str(rep.nodeid)
                    bstack1llll1lll_opy_ = bstack1l1ll1l11_opy_(bstack11l1l1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ᎘"), name, bstack11l1l1_opy_ (u"ࠬ࠭᎙"), bstack11l1l1_opy_ (u"࠭ࠧ᎚"), bstack11l1l1_opy_ (u"ࠧࠨ᎛"), bstack11l1l1_opy_ (u"ࠨࠩ᎜"))
                    for driver in bstack1111lll1l_opy_:
                        if bstack111111ll1_opy_ == driver.session_id:
                            driver.execute_script(bstack1llll1lll_opy_)
            except Exception as e:
                logger.debug(bstack11l1l1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ᎝").format(str(e)))
            try:
                status = bstack11l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᎞") if rep.outcome.lower() == bstack11l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᎟") else bstack11l1l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᎠ")
                reason = bstack11l1l1_opy_ (u"࠭ࠧᎡ")
                if (reason != bstack11l1l1_opy_ (u"ࠢࠣᎢ")):
                    try:
                        if (threading.current_thread().bstackTestErrorMessages == None):
                            threading.current_thread().bstackTestErrorMessages = []
                    except Exception as e:
                        threading.current_thread().bstackTestErrorMessages = []
                    threading.current_thread().bstackTestErrorMessages.append(str(reason))
                if status == bstack11l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᎣ"):
                    reason = rep.longrepr.reprcrash.message
                    if (not threading.current_thread().bstackTestErrorMessages):
                        threading.current_thread().bstackTestErrorMessages = []
                    threading.current_thread().bstackTestErrorMessages.append(reason)
                level = bstack11l1l1_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᎤ") if status == bstack11l1l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᎥ") else bstack11l1l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᎦ")
                data = name + bstack11l1l1_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧᎧ") if status == bstack11l1l1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭Ꭸ") else name + bstack11l1l1_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪᎩ") + reason
                bstack1l1llllll_opy_ = bstack1l1ll1l11_opy_(bstack11l1l1_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪᎪ"), bstack11l1l1_opy_ (u"ࠩࠪᎫ"), bstack11l1l1_opy_ (u"ࠪࠫᎬ"), bstack11l1l1_opy_ (u"ࠫࠬᎭ"), level, data)
                for driver in bstack1111lll1l_opy_:
                    if bstack111111ll1_opy_ == driver.session_id:
                        driver.execute_script(bstack1l1llllll_opy_)
            except Exception as e:
                logger.debug(bstack11l1l1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩᎮ").format(str(e)))
    except Exception as e:
        logger.debug(bstack11l1l1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪᎯ").format(str(e)))
    bstack11111l1l1_opy_(item, call, rep)
notset = Notset()
def bstack1l1llll1_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1lll1111l1_opy_
    if str(name).lower() == bstack11l1l1_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧᎰ"):
        return bstack11l1l1_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢᎱ")
    else:
        return bstack1lll1111l1_opy_(self, name, default, skip)
def bstack1lll1l1l1_opy_(self):
    global CONFIG
    global bstack1ll1lll111_opy_
    try:
        proxy = bstack1ll1l111l_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11l1l1_opy_ (u"ࠩ࠱ࡴࡦࡩࠧᎲ")):
                proxies = bstack1l111lll_opy_(proxy, bstack1lll1lll11_opy_())
                if len(proxies) > 0:
                    protocol, bstack11111l1ll_opy_ = proxies.popitem()
                    if bstack11l1l1_opy_ (u"ࠥ࠾࠴࠵ࠢᎳ") in bstack11111l1ll_opy_:
                        return bstack11111l1ll_opy_
                    else:
                        return bstack11l1l1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᎴ") + bstack11111l1ll_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11l1l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤᎵ").format(str(e)))
    return bstack1ll1lll111_opy_(self)
def bstack1lll111ll1_opy_():
    return bstack11l1l1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᎶ") in CONFIG or bstack11l1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᎷ") in CONFIG and bstack11ll11l1l_opy_() >= version.parse(
        bstack111lllll_opy_)
def bstack11ll1111_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack11l111ll_opy_
    global bstack1ll1l1l11l_opy_
    global bstack1ll11llll_opy_
    CONFIG[bstack11l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᎸ")] = str(bstack1ll11llll_opy_) + str(__version__)
    bstack1ll1l1l1l_opy_ = 0
    try:
        if bstack1ll1l1l11l_opy_ is True:
            bstack1ll1l1l1l_opy_ = int(os.environ.get(bstack11l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᎹ")))
    except:
        bstack1ll1l1l1l_opy_ = 0
    CONFIG[bstack11l1l1_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᎺ")] = True
    bstack1ll111lll_opy_ = bstack11l11lll1_opy_(CONFIG, bstack1ll1l1l1l_opy_)
    logger.debug(bstack1llllll1l_opy_.format(str(bstack1ll111lll_opy_)))
    if CONFIG[bstack11l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᎻ")]:
        bstack11ll1l1ll_opy_(bstack1ll111lll_opy_, bstack1lll111111_opy_)
    if bstack11l1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᎼ") in CONFIG and bstack11l1l1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᎽ") in CONFIG[bstack11l1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᎾ")][bstack1ll1l1l1l_opy_]:
        bstack11l111ll_opy_ = CONFIG[bstack11l1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᎿ")][bstack1ll1l1l1l_opy_][bstack11l1l1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᏀ")]
    import urllib
    import json
    bstack1l11llll1_opy_ = bstack11l1l1_opy_ (u"ࠪࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠬᏁ") + urllib.parse.quote(json.dumps(bstack1ll111lll_opy_))
    browser = self.connect(bstack1l11llll1_opy_)
    return browser
def bstack1ll1l1ll11_opy_():
    global bstack1lll1ll1l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack11ll1111_opy_
        bstack1lll1ll1l_opy_ = True
    except Exception as e:
        pass
def bstack11lll1l11l_opy_():
    global CONFIG
    global bstack111l1lll_opy_
    global bstack11l11ll1_opy_
    global bstack1lll111111_opy_
    global bstack1ll1l1l11l_opy_
    CONFIG = json.loads(os.environ.get(bstack11l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪᏂ")))
    bstack111l1lll_opy_ = eval(os.environ.get(bstack11l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭Ꮓ")))
    bstack11l11ll1_opy_ = os.environ.get(bstack11l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡎࡕࡃࡡࡘࡖࡑ࠭Ꮔ"))
    bstack1lll111ll_opy_(CONFIG, bstack111l1lll_opy_)
    bstack1l11l11ll_opy_()
    global bstack1llll111_opy_
    global bstack1lll11l111_opy_
    global bstack1ll1l1ll_opy_
    global bstack1l11ll111_opy_
    global bstack1l11ll1l1_opy_
    global bstack1lll1llll1_opy_
    global bstack11lll1l1_opy_
    global bstack11llll111_opy_
    global bstack1ll1lll111_opy_
    global bstack1lll1111l1_opy_
    global bstack1ll1ll1111_opy_
    global bstack11111l1l1_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1llll111_opy_ = webdriver.Remote.__init__
        bstack1lll11l111_opy_ = WebDriver.quit
        bstack11lll1l1_opy_ = WebDriver.close
        bstack11llll111_opy_ = WebDriver.get
    except Exception as e:
        pass
    if bstack11l1l1_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᏅ") in CONFIG or bstack11l1l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᏆ") in CONFIG:
        if bstack11ll11l1l_opy_() < version.parse(bstack111lllll_opy_):
            logger.error(bstack11111l11l_opy_.format(bstack11ll11l1l_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1ll1lll111_opy_ = RemoteConnection._get_proxy_url
            except Exception as e:
                logger.error(bstack1111llll1_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1lll1111l1_opy_ = Config.getoption
        from _pytest import runner
        bstack1ll1ll1111_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack111llllll_opy_)
    try:
        from pytest_bdd import reporting
        bstack11111l1l1_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11l1l1_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪᏇ"))
    bstack1lll111111_opy_ = CONFIG.get(bstack11l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧᏈ"), {}).get(bstack11l1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭Ꮙ"))
    bstack1ll1l1l11l_opy_ = True
    bstack1ll1ll1ll_opy_(bstack1l1111l11_opy_)
if (bstack1l1lll11ll_opy_()):
    bstack11lll1l11l_opy_()
@bstack1ll11111l1_opy_(class_method=False)
def bstack11lll11lll_opy_(hook_name, event, bstack11lll11l11_opy_=None):
    if hook_name not in [bstack11l1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭Ꮚ"), bstack11l1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᏋ"), bstack11l1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭Ꮜ"), bstack11l1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᏍ"), bstack11l1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧᏎ"), bstack11l1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫᏏ"), bstack11l1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪᏐ"), bstack11l1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᏑ")]:
        return
    node = store[bstack11l1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪᏒ")]
    if hook_name in [bstack11l1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭Ꮣ"), bstack11l1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᏔ")]:
        node = store[bstack11l1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨᏕ")]
    elif hook_name in [bstack11l1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᏖ"), bstack11l1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬᏗ")]:
        node = store[bstack11l1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪᏘ")]
    if event == bstack11l1l1_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭Ꮩ"):
        hook_type = bstack1l11llll11_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack11lll1l111_opy_ = {
            bstack11l1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᏚ"): uuid,
            bstack11l1l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᏛ"): bstack1l11lll11_opy_(),
            bstack11l1l1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᏜ"): bstack11l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᏝ"),
            bstack11l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᏞ"): hook_type,
            bstack11l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨᏟ"): hook_name
        }
        store[bstack11l1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᏠ")].append(uuid)
        bstack11ll1llll1_opy_ = node.nodeid
        if hook_type == bstack11l1l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᏡ"):
            if not _11ll1lllll_opy_.get(bstack11ll1llll1_opy_, None):
                _11ll1lllll_opy_[bstack11ll1llll1_opy_] = {bstack11l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᏢ"): []}
            _11ll1lllll_opy_[bstack11ll1llll1_opy_][bstack11l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᏣ")].append(bstack11lll1l111_opy_[bstack11l1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᏤ")])
        _11ll1lllll_opy_[bstack11ll1llll1_opy_ + bstack11l1l1_opy_ (u"ࠫ࠲࠭Ꮵ") + hook_name] = bstack11lll1l111_opy_
        bstack11ll1ll1ll_opy_(node, bstack11lll1l111_opy_, bstack11l1l1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭Ꮶ"))
    elif event == bstack11l1l1_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᏧ"):
        bstack11ll1ll11l_opy_ = node.nodeid + bstack11l1l1_opy_ (u"ࠧ࠮ࠩᏨ") + hook_name
        _11ll1lllll_opy_[bstack11ll1ll11l_opy_][bstack11l1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭Ꮹ")] = bstack1l11lll11_opy_()
        bstack11ll1lll11_opy_(_11ll1lllll_opy_[bstack11ll1ll11l_opy_][bstack11l1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᏪ")])
        bstack11ll1ll1ll_opy_(node, _11ll1lllll_opy_[bstack11ll1ll11l_opy_], bstack11l1l1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᏫ"), bstack11ll1lll1l_opy_=bstack11lll11l11_opy_)
def bstack11ll1l1lll_opy_():
    global bstack11ll1l11l1_opy_
    if bstack1l1llll11_opy_():
        bstack11ll1l11l1_opy_ = bstack11l1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᏬ")
    else:
        bstack11ll1l11l1_opy_ = bstack11l1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᏭ")
@bstack1lll11ll11_opy_.bstack11lllll111_opy_
def bstack11ll11llll_opy_():
    bstack11ll1l1lll_opy_()
    if bstack1l1ll1l11l_opy_():
        bstack1l11l1ll1l_opy_(bstack11lll1l1l1_opy_)
    bstack1l1l1lll1l_opy_ = bstack1l1ll111l1_opy_(bstack11lll11lll_opy_)
bstack11ll11llll_opy_()