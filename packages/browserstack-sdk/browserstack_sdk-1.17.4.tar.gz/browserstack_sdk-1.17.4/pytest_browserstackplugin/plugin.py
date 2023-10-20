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
import datetime
import inspect
import logging
import os
import sys
import threading
from uuid import uuid4
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1ll11llll_opy_, bstack1llll111_opy_, update, bstack1lll11l1_opy_,
                                       bstack11llllll_opy_, bstack1l11lll1l_opy_, bstack111l1lll1_opy_, bstack11ll1l11l_opy_,
                                       bstack11ll1l11_opy_, bstack1l11l111_opy_, bstack11lll1111_opy_, bstack1ll1lll11_opy_,
                                       bstack1llll11ll1_opy_)
from browserstack_sdk._version import __version__
from bstack_utils.capture import bstack1ll11l1l11_opy_
from bstack_utils.constants import bstack1l1111l11_opy_, bstack11l11l111_opy_, bstack11111lll1_opy_, bstack111ll11l1_opy_, \
    bstack1ll111ll1_opy_
from bstack_utils.helper import bstack1ll111l111_opy_, bstack1l1lll1lll_opy_, bstack1l111l1l1_opy_, bstack1l1ll1l1ll_opy_, \
    bstack1l1lllllll_opy_, bstack11l1llll_opy_, bstack1lllllll1_opy_, bstack1ll1111l1l_opy_, bstack1l1lllll1_opy_, Notset, \
    bstack1ll11ll11_opy_, bstack1l1ll1ll1l_opy_, bstack1l1lll11ll_opy_, Result, bstack1l1llll1l1_opy_, bstack1l1ll1l11l_opy_, bstack1l1ll11l1l_opy_
from bstack_utils.bstack1l1l1llll1_opy_ import bstack1l1l1ll1l1_opy_
from bstack_utils.messages import bstack11llll1l1_opy_, bstack1l11111l_opy_, bstack1ll1ll1ll1_opy_, bstack1ll11lll_opy_, bstack111ll1l11_opy_, \
    bstack111l1111_opy_, bstack11llllll1_opy_, bstack111111l1l_opy_, bstack1lll11lll1_opy_, bstack1l11llll1_opy_, \
    bstack1lll1lll11_opy_, bstack11111l11l_opy_
from bstack_utils.proxy import bstack111l11111_opy_, bstack1ll1lll1ll_opy_
from bstack_utils.bstack1l1l111l11_opy_ import bstack1l11lllll1_opy_, bstack1l1l111lll_opy_, bstack1l1l11111l_opy_, \
    bstack1l1l111111_opy_, bstack1l1l111ll1_opy_, bstack1l1l111l1l_opy_
from bstack_utils.bstack1l11l1l1ll_opy_ import bstack1l11l1ll11_opy_
from bstack_utils.bstack1l11l1l11l_opy_ import bstack1l1ll11ll_opy_, bstack1lll1l11_opy_, bstack1llll1lll1_opy_
from bstack_utils.bstack1l111ll1ll_opy_ import bstack1l11l1111l_opy_
from bstack_utils.bstack1lllll111l_opy_ import bstack1llll1111_opy_
bstack111l1ll11_opy_ = None
bstack11ll11l1_opy_ = None
bstack11ll1l1ll_opy_ = None
bstack11l1l1lll_opy_ = None
bstack1ll11l1l1_opy_ = None
bstack1l1ll1l11_opy_ = None
bstack11ll111l1_opy_ = None
bstack11l111ll1_opy_ = None
bstack11111ll1l_opy_ = None
bstack11llll1ll_opy_ = None
bstack1l1111lll_opy_ = None
bstack111llll11_opy_ = None
bstack1l1ll111_opy_ = None
bstack1llll1111l_opy_ = bstack11ll11_opy_ (u"ࠪࠫራ")
CONFIG = {}
bstack1l11111l1_opy_ = False
bstack1llll1l11l_opy_ = bstack11ll11_opy_ (u"ࠫࠬሬ")
bstack11l1l11ll_opy_ = bstack11ll11_opy_ (u"ࠬ࠭ር")
bstack1ll111ll_opy_ = False
bstack1llll11l1_opy_ = []
bstack1llll1ll_opy_ = bstack11l11l111_opy_
bstack11ll1l1l1l_opy_ = bstack11ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ሮ")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1llll1ll_opy_,
                    format=bstack11ll11_opy_ (u"ࠧ࡝ࡰࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷࠬሯ"),
                    datefmt=bstack11ll11_opy_ (u"ࠨࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪሰ"),
                    stream=sys.stdout)
store = {
    bstack11ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ሱ"): []
}
def bstack1l1llllll_opy_():
    global CONFIG
    global bstack1llll1ll_opy_
    if bstack11ll11_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬሲ") in CONFIG:
        bstack1llll1ll_opy_ = bstack1l1111l11_opy_[CONFIG[bstack11ll11_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ሳ")]]
        logging.getLogger().setLevel(bstack1llll1ll_opy_)
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11lll1l11l_opy_ = {}
bstack1l1111lll1_opy_ = None
def bstack1lll1l1lll_opy_(page, bstack1lll1ll1_opy_):
    try:
        page.evaluate(bstack11ll11_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨሴ"),
                      bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪስ") + json.dumps(
                          bstack1lll1ll1_opy_) + bstack11ll11_opy_ (u"ࠢࡾࡿࠥሶ"))
    except Exception as e:
        print(bstack11ll11_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨሷ"), e)
def bstack1lll11l1ll_opy_(page, message, level):
    try:
        page.evaluate(bstack11ll11_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥሸ"), bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨሹ") + json.dumps(
            message) + bstack11ll11_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧሺ") + json.dumps(level) + bstack11ll11_opy_ (u"ࠬࢃࡽࠨሻ"))
    except Exception as e:
        print(bstack11ll11_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾࠤሼ"), e)
def bstack1l111llll_opy_(page, status, message=bstack11ll11_opy_ (u"ࠢࠣሽ")):
    try:
        if (status == bstack11ll11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣሾ")):
            page.evaluate(bstack11ll11_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥሿ"),
                          bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡵࡩࡦࡹ࡯࡯ࠤ࠽ࠫቀ") + json.dumps(
                              bstack11ll11_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࠨቁ") + str(message)) + bstack11ll11_opy_ (u"ࠬ࠲ࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠩቂ") + json.dumps(status) + bstack11ll11_opy_ (u"ࠨࡽࡾࠤቃ"))
        else:
            page.evaluate(bstack11ll11_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣቄ"),
                          bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠩቅ") + json.dumps(
                              status) + bstack11ll11_opy_ (u"ࠤࢀࢁࠧቆ"))
    except Exception as e:
        print(bstack11ll11_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤࢀࢃࠢቇ"), e)
def pytest_configure(config):
    config.args = bstack1llll1111_opy_.bstack11llll1l11_opy_(config.args)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack11lll11l1l_opy_ = item.config.getoption(bstack11ll11_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ቈ"))
    plugins = item.config.getoption(bstack11ll11_opy_ (u"ࠧࡶ࡬ࡶࡩ࡬ࡲࡸࠨ቉"))
    report = outcome.get_result()
    bstack11lll11ll1_opy_(item, call, report)
    if bstack11ll11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠦቊ") not in plugins or bstack1l1lllll1_opy_():
        return
    summary = []
    driver = getattr(item, bstack11ll11_opy_ (u"ࠢࡠࡦࡵ࡭ࡻ࡫ࡲࠣቋ"), None)
    page = getattr(item, bstack11ll11_opy_ (u"ࠣࡡࡳࡥ࡬࡫ࠢቌ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack11lll1l111_opy_(item, report, summary, bstack11lll11l1l_opy_)
    if (page is not None):
        bstack11lll11111_opy_(item, report, summary, bstack11lll11l1l_opy_)
def bstack11lll1l111_opy_(item, report, summary, bstack11lll11l1l_opy_):
    if report.when in [bstack11ll11_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣቍ"), bstack11ll11_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧ቎")]:
        return
    if not bstack1l1lll1lll_opy_():
        return
    try:
        if (str(bstack11lll11l1l_opy_).lower() != bstack11ll11_opy_ (u"ࠫࡹࡸࡵࡦࠩ቏")):
            item._driver.execute_script(
                bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪቐ") + json.dumps(
                    report.nodeid) + bstack11ll11_opy_ (u"࠭ࡽࡾࠩቑ"))
    except Exception as e:
        summary.append(
            bstack11ll11_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦ࠼ࠣࡿ࠵ࢃࠢቒ").format(e)
        )
    passed = report.passed or (report.failed and hasattr(report, bstack11ll11_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥቓ")))
    bstack1l1l1111l_opy_ = bstack11ll11_opy_ (u"ࠤࠥቔ")
    if not passed:
        try:
            bstack1l1l1111l_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11ll11_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥቕ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1l1111l_opy_))
    try:
        if passed:
            item._driver.execute_script(
                bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭ቖ")
                + json.dumps(bstack11ll11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠦࠨ቗"))
                + bstack11ll11_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣቘ")
            )
        else:
            item._driver.execute_script(
                bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪ቙")
                + json.dumps(str(bstack1l1l1111l_opy_))
                + bstack11ll11_opy_ (u"ࠣ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥቚ")
            )
    except Exception as e:
        summary.append(bstack11ll11_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡢࡰࡱࡳࡹࡧࡴࡦ࠼ࠣࡿ࠵ࢃࠢቛ").format(e))
def bstack11lll11111_opy_(item, report, summary, bstack11lll11l1l_opy_):
    if report.when in [bstack11ll11_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤቜ"), bstack11ll11_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨቝ")]:
        return
    if (str(bstack11lll11l1l_opy_).lower() != bstack11ll11_opy_ (u"ࠬࡺࡲࡶࡧࠪ቞")):
        bstack1lll1l1lll_opy_(item._page, report.nodeid)
    passed = report.passed or (report.failed and hasattr(report, bstack11ll11_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣ቟")))
    bstack1l1l1111l_opy_ = bstack11ll11_opy_ (u"ࠢࠣበ")
    if not passed:
        try:
            bstack1l1l1111l_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11ll11_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣቡ").format(e)
            )
    try:
        if passed:
            bstack1l111llll_opy_(item._page, bstack11ll11_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤቢ"))
        else:
            if bstack1l1l1111l_opy_:
                bstack1lll11l1ll_opy_(item._page, str(bstack1l1l1111l_opy_), bstack11ll11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤባ"))
                bstack1l111llll_opy_(item._page, bstack11ll11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦቤ"), str(bstack1l1l1111l_opy_))
            else:
                bstack1l111llll_opy_(item._page, bstack11ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧብ"))
    except Exception as e:
        summary.append(bstack11ll11_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻ࠱ࡿࠥቦ").format(e))
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
    parser.addoption(bstack11ll11_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦቧ"), default=bstack11ll11_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢቨ"), help=bstack11ll11_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣቩ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11ll11_opy_ (u"ࠥ࠱࠲ࡪࡲࡪࡸࡨࡶࠧቪ"), action=bstack11ll11_opy_ (u"ࠦࡸࡺ࡯ࡳࡧࠥቫ"), default=bstack11ll11_opy_ (u"ࠧࡩࡨࡳࡱࡰࡩࠧቬ"),
                         help=bstack11ll11_opy_ (u"ࠨࡄࡳ࡫ࡹࡩࡷࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷࠧቭ"))
def bstack11lll11lll_opy_(log):
    if not (log[bstack11ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨቮ")] and log[bstack11ll11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩቯ")].strip()):
        return
    active = bstack11ll1ll1ll_opy_()
    log = {
        bstack11ll11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨተ"): log[bstack11ll11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩቱ")],
        bstack11ll11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧቲ"): datetime.datetime.utcnow().isoformat() + bstack11ll11_opy_ (u"ࠬࡠࠧታ"),
        bstack11ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧቴ"): log[bstack11ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨት")],
    }
    if active:
        if active[bstack11ll11_opy_ (u"ࠨࡶࡼࡴࡪ࠭ቶ")] == bstack11ll11_opy_ (u"ࠩ࡫ࡳࡴࡱࠧቷ"):
            log[bstack11ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪቸ")] = active[bstack11ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫቹ")]
        elif active[bstack11ll11_opy_ (u"ࠬࡺࡹࡱࡧࠪቺ")] == bstack11ll11_opy_ (u"࠭ࡴࡦࡵࡷࠫቻ"):
            log[bstack11ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧቼ")] = active[bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨች")]
    bstack1llll1111_opy_.bstack1l1111ll1l_opy_([log])
def bstack11ll1ll1ll_opy_():
    if len(store[bstack11ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ቾ")]) > 0 and store[bstack11ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧቿ")][-1]:
        return {
            bstack11ll11_opy_ (u"ࠫࡹࡿࡰࡦࠩኀ"): bstack11ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪኁ"),
            bstack11ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ኂ"): store[bstack11ll11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫኃ")][-1]
        }
    if store.get(bstack11ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬኄ"), None):
        return {
            bstack11ll11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧኅ"): bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࠨኆ"),
            bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫኇ"): store[bstack11ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩኈ")]
        }
    return None
bstack11ll1ll11l_opy_ = bstack1ll11l1l11_opy_(bstack11lll11lll_opy_)
def pytest_runtest_call(item):
    try:
        if not bstack1llll1111_opy_.on() or bstack11ll1l1l1l_opy_ != bstack11ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭኉"):
            return
        global bstack1l1111lll1_opy_, bstack11ll1ll11l_opy_
        bstack11ll1ll11l_opy_.start()
        bstack11ll1l111l_opy_ = {
            bstack11ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬኊ"): uuid4().__str__(),
            bstack11ll11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬኋ"): datetime.datetime.utcnow().isoformat() + bstack11ll11_opy_ (u"ࠩ࡝ࠫኌ")
        }
        bstack1l1111lll1_opy_ = bstack11ll1l111l_opy_[bstack11ll11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨኍ")]
        store[bstack11ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ኎")] = bstack11ll1l111l_opy_[bstack11ll11_opy_ (u"ࠬࡻࡵࡪࡦࠪ኏")]
        threading.current_thread().bstack1l1111lll1_opy_ = bstack1l1111lll1_opy_
        _11lll1l11l_opy_[item.nodeid] = {**_11lll1l11l_opy_[item.nodeid], **bstack11ll1l111l_opy_}
        bstack11lll1l1l1_opy_(item, _11lll1l11l_opy_[item.nodeid], bstack11ll11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧነ"))
    except Exception as err:
        print(bstack11ll11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡤࡣ࡯ࡰ࠿ࠦࡻࡾࠩኑ"), str(err))
def pytest_runtest_setup(item):
    if bstack1ll1111l1l_opy_():
        atexit.register(bstack111ll11ll_opy_)
    try:
        if not bstack1llll1111_opy_.on():
            return
        bstack11ll1ll11l_opy_.start()
        uuid = uuid4().__str__()
        bstack11ll1l111l_opy_ = {
            bstack11ll11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ኒ"): uuid,
            bstack11ll11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ና"): datetime.datetime.utcnow().isoformat() + bstack11ll11_opy_ (u"ࠪ࡞ࠬኔ"),
            bstack11ll11_opy_ (u"ࠫࡹࡿࡰࡦࠩን"): bstack11ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪኖ"),
            bstack11ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩኗ"): bstack11ll11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬኘ"),
            bstack11ll11_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫኙ"): bstack11ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨኚ")
        }
        threading.current_thread().bstack11lll1111l_opy_ = uuid
        store[bstack11ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧኛ")] = item
        store[bstack11ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨኜ")] = [uuid]
        if not _11lll1l11l_opy_.get(item.nodeid, None):
            _11lll1l11l_opy_[item.nodeid] = {bstack11ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫኝ"): [], bstack11ll11_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨኞ"): []}
        _11lll1l11l_opy_[item.nodeid][bstack11ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ኟ")].append(bstack11ll1l111l_opy_[bstack11ll11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭አ")])
        _11lll1l11l_opy_[item.nodeid + bstack11ll11_opy_ (u"ࠩ࠰ࡷࡪࡺࡵࡱࠩኡ")] = bstack11ll1l111l_opy_
        bstack11ll1ll1l1_opy_(item, bstack11ll1l111l_opy_, bstack11ll11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫኢ"))
    except Exception as err:
        print(bstack11ll11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧኣ"), str(err))
def pytest_runtest_teardown(item):
    try:
        if not bstack1llll1111_opy_.on():
            return
        bstack11ll1l111l_opy_ = {
            bstack11ll11_opy_ (u"ࠬࡻࡵࡪࡦࠪኤ"): uuid4().__str__(),
            bstack11ll11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪእ"): datetime.datetime.utcnow().isoformat() + bstack11ll11_opy_ (u"࡛ࠧࠩኦ"),
            bstack11ll11_opy_ (u"ࠨࡶࡼࡴࡪ࠭ኧ"): bstack11ll11_opy_ (u"ࠩ࡫ࡳࡴࡱࠧከ"),
            bstack11ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ኩ"): bstack11ll11_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨኪ"),
            bstack11ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨካ"): bstack11ll11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨኬ")
        }
        _11lll1l11l_opy_[item.nodeid + bstack11ll11_opy_ (u"ࠧ࠮ࡶࡨࡥࡷࡪ࡯ࡸࡰࠪክ")] = bstack11ll1l111l_opy_
        bstack11ll1ll1l1_opy_(item, bstack11ll1l111l_opy_, bstack11ll11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩኮ"))
    except Exception as err:
        print(bstack11ll11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱ࠾ࠥࢁࡽࠨኯ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1llll1111_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1l1l11111l_opy_(fixturedef.argname):
        store[bstack11ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡲࡵࡤࡶ࡮ࡨࡣ࡮ࡺࡥ࡮ࠩኰ")] = request.node
    elif bstack1l1l111111_opy_(fixturedef.argname):
        store[bstack11ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩ኱")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack11ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪኲ"): fixturedef.argname,
            bstack11ll11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ኳ"): bstack1l1ll1l1ll_opy_(outcome),
            bstack11ll11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩኴ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        bstack11ll11l1ll_opy_ = store[bstack11ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬኵ")]
        if not _11lll1l11l_opy_.get(bstack11ll11l1ll_opy_.nodeid, None):
            _11lll1l11l_opy_[bstack11ll11l1ll_opy_.nodeid] = {bstack11ll11_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ኶"): []}
        _11lll1l11l_opy_[bstack11ll11l1ll_opy_.nodeid][bstack11ll11_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ኷")].append(fixture)
    except Exception as err:
        logger.debug(bstack11ll11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧኸ"), str(err))
if bstack1l1lllll1_opy_() and bstack1llll1111_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _11lll1l11l_opy_[request.node.nodeid][bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨኹ")].bstack1l111lllll_opy_(id(step))
        except Exception as err:
            print(bstack11ll11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶ࠺ࠡࡽࢀࠫኺ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _11lll1l11l_opy_[request.node.nodeid][bstack11ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪኻ")].bstack1l111l1l11_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11ll11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬኼ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack1l111ll1ll_opy_: bstack1l11l1111l_opy_ = _11lll1l11l_opy_[request.node.nodeid][bstack11ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬኽ")]
            bstack1l111ll1ll_opy_.bstack1l111l1l11_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11ll11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧኾ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack11ll1l1l1l_opy_
        try:
            if not bstack1llll1111_opy_.on() or bstack11ll1l1l1l_opy_ != bstack11ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨ኿"):
                return
            global bstack11ll1ll11l_opy_
            bstack11ll1ll11l_opy_.start()
            if not _11lll1l11l_opy_.get(request.node.nodeid, None):
                _11lll1l11l_opy_[request.node.nodeid] = {}
            bstack1l111ll1ll_opy_ = bstack1l11l1111l_opy_.bstack1l111l11l1_opy_(
                scenario, feature, request.node,
                name=bstack1l1l111ll1_opy_(request.node, scenario),
                bstack1l11l111ll_opy_=bstack1l111l1l1_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11ll11_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧዀ"),
                tags=bstack1l1l111l1l_opy_(feature, scenario)
            )
            _11lll1l11l_opy_[request.node.nodeid][bstack11ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ዁")] = bstack1l111ll1ll_opy_
            bstack11lll11l11_opy_(bstack1l111ll1ll_opy_.uuid)
            bstack1llll1111_opy_.bstack11llllllll_opy_(bstack11ll11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨዂ"), bstack1l111ll1ll_opy_)
        except Exception as err:
            print(bstack11ll11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪዃ"), str(err))
def bstack11ll1lll1l_opy_(bstack11ll1lll11_opy_):
    if bstack11ll1lll11_opy_ in store[bstack11ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ዄ")]:
        store[bstack11ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧዅ")].remove(bstack11ll1lll11_opy_)
def bstack11lll11l11_opy_(bstack11ll11ll11_opy_):
    store[bstack11ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ዆")] = bstack11ll11ll11_opy_
    threading.current_thread().bstack1l1111lll1_opy_ = bstack11ll11ll11_opy_
@bstack1llll1111_opy_.bstack1l11111lll_opy_
def bstack11lll11ll1_opy_(item, call, report):
    global bstack11ll1l1l1l_opy_
    try:
        if report.when == bstack11ll11_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ዇"):
            bstack11ll1ll11l_opy_.reset()
        if report.when == bstack11ll11_opy_ (u"࠭ࡣࡢ࡮࡯ࠫወ"):
            if bstack11ll1l1l1l_opy_ == bstack11ll11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧዉ"):
                _11lll1l11l_opy_[item.nodeid][bstack11ll11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ዊ")] = bstack1l1llll1l1_opy_(report.stop)
                bstack11lll1l1l1_opy_(item, _11lll1l11l_opy_[item.nodeid], bstack11ll11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫዋ"), report, call)
                store[bstack11ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧዌ")] = None
            elif bstack11ll1l1l1l_opy_ == bstack11ll11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣው"):
                bstack1l111ll1ll_opy_ = _11lll1l11l_opy_[item.nodeid][bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨዎ")]
                bstack1l111ll1ll_opy_.set(hooks=_11lll1l11l_opy_[item.nodeid].get(bstack11ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬዏ"), []))
                exception, bstack1l1lll111l_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l1lll111l_opy_ = [call.excinfo.exconly(), report.longreprtext]
                bstack1l111ll1ll_opy_.stop(time=bstack1l1llll1l1_opy_(report.stop), result=Result(result=report.outcome, exception=exception, bstack1l1lll111l_opy_=bstack1l1lll111l_opy_))
                bstack1llll1111_opy_.bstack11llllllll_opy_(bstack11ll11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩዐ"), _11lll1l11l_opy_[item.nodeid][bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫዑ")])
        elif report.when in [bstack11ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨዒ"), bstack11ll11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬዓ")]:
            bstack11ll11l11l_opy_ = item.nodeid + bstack11ll11_opy_ (u"ࠫ࠲࠭ዔ") + report.when
            if report.skipped:
                hook_type = bstack11ll11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪዕ") if report.when == bstack11ll11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬዖ") else bstack11ll11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫ዗")
                _11lll1l11l_opy_[bstack11ll11l11l_opy_] = {
                    bstack11ll11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ዘ"): uuid4().__str__(),
                    bstack11ll11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ዙ"): datetime.datetime.utcfromtimestamp(report.start).isoformat() + bstack11ll11_opy_ (u"ࠪ࡞ࠬዚ"),
                    bstack11ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧዛ"): hook_type
                }
            _11lll1l11l_opy_[bstack11ll11l11l_opy_][bstack11ll11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪዜ")] = datetime.datetime.utcfromtimestamp(report.stop).isoformat() + bstack11ll11_opy_ (u"࡚࠭ࠨዝ")
            bstack11ll1lll1l_opy_(_11lll1l11l_opy_[bstack11ll11l11l_opy_][bstack11ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬዞ")])
            bstack11ll1ll1l1_opy_(item, _11lll1l11l_opy_[bstack11ll11l11l_opy_], bstack11ll11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪዟ"), report, call)
            if report.when == bstack11ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨዠ"):
                if report.outcome == bstack11ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪዡ"):
                    bstack11ll1l111l_opy_ = {
                        bstack11ll11_opy_ (u"ࠫࡺࡻࡩࡥࠩዢ"): uuid4().__str__(),
                        bstack11ll11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩዣ"): bstack1l111l1l1_opy_(),
                        bstack11ll11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫዤ"): bstack1l111l1l1_opy_()
                    }
                    _11lll1l11l_opy_[item.nodeid] = {**_11lll1l11l_opy_[item.nodeid], **bstack11ll1l111l_opy_}
                    bstack11lll1l1l1_opy_(item, _11lll1l11l_opy_[item.nodeid], bstack11ll11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨዥ"))
                    bstack11lll1l1l1_opy_(item, _11lll1l11l_opy_[item.nodeid], bstack11ll11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪዦ"), report, call)
    except Exception as err:
        print(bstack11ll11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࢀࢃࠧዧ"), str(err))
def bstack11ll1l1lll_opy_(test, bstack11ll1l111l_opy_, result=None, call=None, bstack11lll1l1l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1l111ll1ll_opy_ = {
        bstack11ll11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨየ"): bstack11ll1l111l_opy_[bstack11ll11_opy_ (u"ࠫࡺࡻࡩࡥࠩዩ")],
        bstack11ll11_opy_ (u"ࠬࡺࡹࡱࡧࠪዪ"): bstack11ll11_opy_ (u"࠭ࡴࡦࡵࡷࠫያ"),
        bstack11ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬዬ"): test.name,
        bstack11ll11_opy_ (u"ࠨࡤࡲࡨࡾ࠭ይ"): {
            bstack11ll11_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧዮ"): bstack11ll11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪዯ"),
            bstack11ll11_opy_ (u"ࠫࡨࡵࡤࡦࠩደ"): inspect.getsource(test.obj)
        },
        bstack11ll11_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩዱ"): test.name,
        bstack11ll11_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬዲ"): test.name,
        bstack11ll11_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧዳ"): bstack1llll1111_opy_.bstack1l111111ll_opy_(test),
        bstack11ll11_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫዴ"): file_path,
        bstack11ll11_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫድ"): file_path,
        bstack11ll11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪዶ"): bstack11ll11_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬዷ"),
        bstack11ll11_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪዸ"): file_path,
        bstack11ll11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪዹ"): bstack11ll1l111l_opy_[bstack11ll11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫዺ")],
        bstack11ll11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫዻ"): bstack11ll11_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩዼ"),
        bstack11ll11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭ዽ"): {
            bstack11ll11_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨዾ"): test.nodeid
        },
        bstack11ll11_opy_ (u"ࠬࡺࡡࡨࡵࠪዿ"): bstack1l1lllllll_opy_(test.own_markers)
    }
    if bstack11lll1l1l_opy_ in [bstack11ll11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧጀ"), bstack11ll11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩጁ")]:
        bstack1l111ll1ll_opy_[bstack11ll11_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭ጂ")] = {
            bstack11ll11_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫጃ"): bstack11ll1l111l_opy_.get(bstack11ll11_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬጄ"), [])
        }
    if bstack11lll1l1l_opy_ == bstack11ll11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬጅ"):
        bstack1l111ll1ll_opy_[bstack11ll11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬጆ")] = bstack11ll11_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧጇ")
        bstack1l111ll1ll_opy_[bstack11ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ገ")] = bstack11ll1l111l_opy_[bstack11ll11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧጉ")]
        bstack1l111ll1ll_opy_[bstack11ll11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧጊ")] = bstack11ll1l111l_opy_[bstack11ll11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨጋ")]
    if result:
        bstack1l111ll1ll_opy_[bstack11ll11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫጌ")] = result.outcome
        bstack1l111ll1ll_opy_[bstack11ll11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ግ")] = result.duration * 1000
        bstack1l111ll1ll_opy_[bstack11ll11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫጎ")] = bstack11ll1l111l_opy_[bstack11ll11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬጏ")]
        if result.failed:
            bstack1l111ll1ll_opy_[bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧጐ")] = bstack1llll1111_opy_.bstack1l1llllll1_opy_(call.excinfo.typename)
            bstack1l111ll1ll_opy_[bstack11ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ጑")] = bstack1llll1111_opy_.bstack11lll1llll_opy_(call.excinfo, result)
        bstack1l111ll1ll_opy_[bstack11ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩጒ")] = bstack11ll1l111l_opy_[bstack11ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪጓ")]
    if outcome:
        bstack1l111ll1ll_opy_[bstack11ll11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬጔ")] = bstack1l1ll1l1ll_opy_(outcome)
        bstack1l111ll1ll_opy_[bstack11ll11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧጕ")] = 0
        bstack1l111ll1ll_opy_[bstack11ll11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ጖")] = bstack11ll1l111l_opy_[bstack11ll11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭጗")]
        if bstack1l111ll1ll_opy_[bstack11ll11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩጘ")] == bstack11ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪጙ"):
            bstack1l111ll1ll_opy_[bstack11ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪጚ")] = bstack11ll11_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭ጛ")  # bstack11ll11ll1l_opy_
            bstack1l111ll1ll_opy_[bstack11ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧጜ")] = [{bstack11ll11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪጝ"): [bstack11ll11_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬጞ")]}]
        bstack1l111ll1ll_opy_[bstack11ll11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨጟ")] = bstack11ll1l111l_opy_[bstack11ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩጠ")]
    return bstack1l111ll1ll_opy_
def bstack11ll1ll111_opy_(test, bstack11lll1ll11_opy_, bstack11lll1l1l_opy_, result, call, outcome, bstack11lll111ll_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack11lll1ll11_opy_[bstack11ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧጡ")]
    hook_name = bstack11lll1ll11_opy_[bstack11ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨጢ")]
    hook_data = {
        bstack11ll11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫጣ"): bstack11lll1ll11_opy_[bstack11ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬጤ")],
        bstack11ll11_opy_ (u"ࠨࡶࡼࡴࡪ࠭ጥ"): bstack11ll11_opy_ (u"ࠩ࡫ࡳࡴࡱࠧጦ"),
        bstack11ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨጧ"): bstack11ll11_opy_ (u"ࠫࢀࢃࠧጨ").format(bstack1l11lllll1_opy_(hook_name)),
        bstack11ll11_opy_ (u"ࠬࡨ࡯ࡥࡻࠪጩ"): {
            bstack11ll11_opy_ (u"࠭࡬ࡢࡰࡪࠫጪ"): bstack11ll11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧጫ"),
            bstack11ll11_opy_ (u"ࠨࡥࡲࡨࡪ࠭ጬ"): None
        },
        bstack11ll11_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨጭ"): test.name,
        bstack11ll11_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪጮ"): bstack1llll1111_opy_.bstack1l111111ll_opy_(test, hook_name),
        bstack11ll11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧጯ"): file_path,
        bstack11ll11_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧጰ"): file_path,
        bstack11ll11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ጱ"): bstack11ll11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨጲ"),
        bstack11ll11_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭ጳ"): file_path,
        bstack11ll11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ጴ"): bstack11lll1ll11_opy_[bstack11ll11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧጵ")],
        bstack11ll11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧጶ"): bstack11ll11_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧጷ") if bstack11ll1l1l1l_opy_ == bstack11ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪጸ") else bstack11ll11_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧጹ"),
        bstack11ll11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫጺ"): hook_type
    }
    bstack11ll1l1ll1_opy_ = bstack11ll11llll_opy_(_11lll1l11l_opy_.get(test.nodeid, None))
    if bstack11ll1l1ll1_opy_:
        hook_data[bstack11ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣ࡮ࡪࠧጻ")] = bstack11ll1l1ll1_opy_
    if result:
        hook_data[bstack11ll11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪጼ")] = result.outcome
        hook_data[bstack11ll11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬጽ")] = result.duration * 1000
        hook_data[bstack11ll11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪጾ")] = bstack11lll1ll11_opy_[bstack11ll11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫጿ")]
        if result.failed:
            hook_data[bstack11ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ፀ")] = bstack1llll1111_opy_.bstack1l1llllll1_opy_(call.excinfo.typename)
            hook_data[bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩፁ")] = bstack1llll1111_opy_.bstack11lll1llll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11ll11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩፂ")] = bstack1l1ll1l1ll_opy_(outcome)
        hook_data[bstack11ll11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫፃ")] = 100
        hook_data[bstack11ll11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩፄ")] = bstack11lll1ll11_opy_[bstack11ll11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪፅ")]
        if hook_data[bstack11ll11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ፆ")] == bstack11ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧፇ"):
            hook_data[bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧፈ")] = bstack11ll11_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪፉ")  # bstack11ll11ll1l_opy_
            hook_data[bstack11ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫፊ")] = [{bstack11ll11_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧፋ"): [bstack11ll11_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩፌ")]}]
    if bstack11lll111ll_opy_:
        hook_data[bstack11ll11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ፍ")] = bstack11lll111ll_opy_.result
        hook_data[bstack11ll11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨፎ")] = bstack1l1ll1ll1l_opy_(bstack11lll1ll11_opy_[bstack11ll11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬፏ")], bstack11lll1ll11_opy_[bstack11ll11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧፐ")])
        hook_data[bstack11ll11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨፑ")] = bstack11lll1ll11_opy_[bstack11ll11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩፒ")]
        if hook_data[bstack11ll11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬፓ")] == bstack11ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ፔ"):
            hook_data[bstack11ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ፕ")] = bstack1llll1111_opy_.bstack1l1llllll1_opy_(bstack11lll111ll_opy_.exception_type)
            hook_data[bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩፖ")] = [{bstack11ll11_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬፗ"): bstack1l1lll11ll_opy_(bstack11lll111ll_opy_.exception)}]
    return hook_data
def bstack11lll1l1l1_opy_(test, bstack11ll1l111l_opy_, bstack11lll1l1l_opy_, result=None, call=None, outcome=None):
    bstack1l111ll1ll_opy_ = bstack11ll1l1lll_opy_(test, bstack11ll1l111l_opy_, result, call, bstack11lll1l1l_opy_, outcome)
    driver = getattr(test, bstack11ll11_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫፘ"), None)
    if bstack11lll1l1l_opy_ == bstack11ll11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬፙ") and driver:
        bstack1l111ll1ll_opy_[bstack11ll11_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫፚ")] = bstack1llll1111_opy_.bstack11llll1ll1_opy_(driver)
    if bstack11lll1l1l_opy_ == bstack11ll11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧ፛"):
        bstack11lll1l1l_opy_ = bstack11ll11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ፜")
    bstack11lll1lll1_opy_ = {
        bstack11ll11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ፝"): bstack11lll1l1l_opy_,
        bstack11ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ፞"): bstack1l111ll1ll_opy_
    }
    bstack1llll1111_opy_.bstack1l1111l1ll_opy_(bstack11lll1lll1_opy_)
def bstack11ll1ll1l1_opy_(test, bstack11ll1l111l_opy_, bstack11lll1l1l_opy_, result=None, call=None, outcome=None, bstack11lll111ll_opy_=None):
    hook_data = bstack11ll1ll111_opy_(test, bstack11ll1l111l_opy_, bstack11lll1l1l_opy_, result, call, outcome, bstack11lll111ll_opy_)
    bstack11lll1lll1_opy_ = {
        bstack11ll11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ፟"): bstack11lll1l1l_opy_,
        bstack11ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳ࠭፠"): hook_data
    }
    bstack1llll1111_opy_.bstack1l1111l1ll_opy_(bstack11lll1lll1_opy_)
def bstack11ll11llll_opy_(bstack11ll1l111l_opy_):
    if not bstack11ll1l111l_opy_:
        return None
    if bstack11ll1l111l_opy_.get(bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ፡"), None):
        return getattr(bstack11ll1l111l_opy_[bstack11ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ።")], bstack11ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ፣"), None)
    return bstack11ll1l111l_opy_.get(bstack11ll11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭፤"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1llll1111_opy_.on():
            return
        places = [bstack11ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ፥"), bstack11ll11_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ፦"), bstack11ll11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭፧")]
        bstack1l111111l1_opy_ = []
        for bstack11lll1l1ll_opy_ in places:
            records = caplog.get_records(bstack11lll1l1ll_opy_)
            bstack11ll1l11l1_opy_ = bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ፨") if bstack11lll1l1ll_opy_ == bstack11ll11_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ፩") else bstack11ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ፪")
            bstack11ll1l1l11_opy_ = request.node.nodeid + (bstack11ll11_opy_ (u"ࠨࠩ፫") if bstack11lll1l1ll_opy_ == bstack11ll11_opy_ (u"ࠩࡦࡥࡱࡲࠧ፬") else bstack11ll11_opy_ (u"ࠪ࠱ࠬ፭") + bstack11lll1l1ll_opy_)
            bstack11ll11ll11_opy_ = bstack11ll11llll_opy_(_11lll1l11l_opy_.get(bstack11ll1l1l11_opy_, None))
            if not bstack11ll11ll11_opy_:
                continue
            for record in records:
                if bstack1l1ll1l11l_opy_(record.message):
                    continue
                bstack1l111111l1_opy_.append({
                    bstack11ll11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ፮"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack11ll11_opy_ (u"ࠬࡠࠧ፯"),
                    bstack11ll11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ፰"): record.levelname,
                    bstack11ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ፱"): record.message,
                    bstack11ll1l11l1_opy_: bstack11ll11ll11_opy_
                })
        if len(bstack1l111111l1_opy_) > 0:
            bstack1llll1111_opy_.bstack1l1111ll1l_opy_(bstack1l111111l1_opy_)
    except Exception as err:
        print(bstack11ll11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡦࡳࡳࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥ࠻ࠢࡾࢁࠬ፲"), str(err))
def bstack11ll1l1111_opy_(driver_command, response):
    if driver_command == bstack11ll11_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭፳"):
        bstack1llll1111_opy_.bstack1l11111111_opy_({
            bstack11ll11_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩ፴"): response[bstack11ll11_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪ፵")],
            bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ፶"): store[bstack11ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ፷")]
        })
def bstack111ll11ll_opy_():
    global bstack1llll11l1_opy_
    bstack1llll1111_opy_.bstack11llll1l1l_opy_()
    for driver in bstack1llll11l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll1lllll1_opy_(self, *args, **kwargs):
    bstack111111ll1_opy_ = bstack111l1ll11_opy_(self, *args, **kwargs)
    bstack1llll1111_opy_.bstack1l111ll1_opy_(self)
    return bstack111111ll1_opy_
def bstack1l1lll1l1_opy_(framework_name):
    global bstack1llll1111l_opy_
    global bstack1l1l1ll1l_opy_
    bstack1llll1111l_opy_ = framework_name
    logger.info(bstack11111l11l_opy_.format(bstack1llll1111l_opy_.split(bstack11ll11_opy_ (u"ࠧ࠮ࠩ፸"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1lll1lll_opy_():
            Service.start = bstack111l1lll1_opy_
            Service.stop = bstack11ll1l11l_opy_
            webdriver.Remote.__init__ = bstack11lll1l1_opy_
            webdriver.Remote.get = bstack111ll1l1_opy_
            if not isinstance(os.getenv(bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡃࡕࡅࡑࡒࡅࡍࠩ፹")), str):
                return
            WebDriver.close = bstack11ll1l11_opy_
            WebDriver.quit = bstack1ll1lll11l_opy_
        if not bstack1l1lll1lll_opy_() and bstack1llll1111_opy_.on():
            webdriver.Remote.__init__ = bstack1ll1lllll1_opy_
        bstack1l1l1ll1l_opy_ = True
    except Exception as e:
        pass
    bstack11lll111l_opy_()
    if os.environ.get(bstack11ll11_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧ፺")):
        bstack1l1l1ll1l_opy_ = eval(os.environ.get(bstack11ll11_opy_ (u"ࠪࡗࡊࡒࡅࡏࡋࡘࡑࡤࡕࡒࡠࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡏࡎࡔࡖࡄࡐࡑࡋࡄࠨ፻")))
    if not bstack1l1l1ll1l_opy_:
        bstack11lll1111_opy_(bstack11ll11_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨ፼"), bstack1lll1lll11_opy_)
    if bstack1lll1lll1l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack11l1111l_opy_
        except Exception as e:
            logger.error(bstack111l1111_opy_.format(str(e)))
    if bstack11ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ፽") in str(framework_name).lower():
        if not bstack1l1lll1lll_opy_():
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
def bstack1ll1lll11l_opy_(self):
    global bstack1llll1111l_opy_
    global bstack1l11ll1l_opy_
    global bstack11ll11l1_opy_
    try:
        if bstack11ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭፾") in bstack1llll1111l_opy_ and self.session_id != None:
            bstack1llll1llll_opy_ = bstack11ll11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ፿") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᎀ")
            bstack11llll11l_opy_ = bstack1l1ll11ll_opy_(bstack11ll11_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᎁ"), bstack11ll11_opy_ (u"ࠪࠫᎂ"), bstack1llll1llll_opy_, bstack11ll11_opy_ (u"ࠫ࠱ࠦࠧᎃ").join(
                threading.current_thread().bstackTestErrorMessages), bstack11ll11_opy_ (u"ࠬ࠭ᎄ"), bstack11ll11_opy_ (u"࠭ࠧᎅ"))
            if self != None:
                self.execute_script(bstack11llll11l_opy_)
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡵࡣࡷࡹࡸࡀࠠࠣᎆ") + str(e))
    bstack11ll11l1_opy_(self)
    self.session_id = None
def bstack11lll1l1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1l11ll1l_opy_
    global bstack1l11lll11_opy_
    global bstack1ll111ll_opy_
    global bstack1llll1111l_opy_
    global bstack111l1ll11_opy_
    global bstack1llll11l1_opy_
    global bstack1llll1l11l_opy_
    global bstack11l1l11ll_opy_
    CONFIG[bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᎇ")] = str(bstack1llll1111l_opy_) + str(__version__)
    command_executor = bstack1lllllll1_opy_(bstack1llll1l11l_opy_)
    logger.debug(bstack1ll11lll_opy_.format(command_executor))
    proxy = bstack1llll11ll1_opy_(CONFIG, proxy)
    bstack111l111l_opy_ = 0
    try:
        if bstack1ll111ll_opy_ is True:
            bstack111l111l_opy_ = int(os.environ.get(bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᎈ")))
    except:
        bstack111l111l_opy_ = 0
    bstack11111ll1_opy_ = bstack1ll11llll_opy_(CONFIG, bstack111l111l_opy_)
    logger.debug(bstack111111l1l_opy_.format(str(bstack11111ll1_opy_)))
    if bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᎉ") in CONFIG and CONFIG[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᎊ")]:
        bstack1llll1lll1_opy_(bstack11111ll1_opy_, bstack11l1l11ll_opy_)
    if desired_capabilities:
        bstack111l11ll_opy_ = bstack1llll111_opy_(desired_capabilities)
        bstack111l11ll_opy_[bstack11ll11_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᎋ")] = bstack1ll11ll11_opy_(CONFIG)
        bstack1ll1l1l111_opy_ = bstack1ll11llll_opy_(bstack111l11ll_opy_)
        if bstack1ll1l1l111_opy_:
            bstack11111ll1_opy_ = update(bstack1ll1l1l111_opy_, bstack11111ll1_opy_)
        desired_capabilities = None
    if options:
        bstack1l11l111_opy_(options, bstack11111ll1_opy_)
    if not options:
        options = bstack1lll11l1_opy_(bstack11111ll1_opy_)
    if proxy and bstack11l1llll_opy_() >= version.parse(bstack11ll11_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ᎌ")):
        options.proxy(proxy)
    if options and bstack11l1llll_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᎍ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack11l1llll_opy_() < version.parse(bstack11ll11_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᎎ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack11111ll1_opy_)
    logger.info(bstack1ll1ll1ll1_opy_)
    if bstack11l1llll_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩᎏ")):
        bstack111l1ll11_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l1llll_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩ᎐")):
        bstack111l1ll11_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l1llll_opy_() >= version.parse(bstack11ll11_opy_ (u"ࠫ࠷࠴࠵࠴࠰࠳ࠫ᎑")):
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
        bstack111l111ll_opy_ = bstack11ll11_opy_ (u"ࠬ࠭᎒")
        if bstack11l1llll_opy_() >= version.parse(bstack11ll11_opy_ (u"࠭࠴࠯࠲࠱࠴ࡧ࠷ࠧ᎓")):
            bstack111l111ll_opy_ = self.caps.get(bstack11ll11_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ᎔"))
        else:
            bstack111l111ll_opy_ = self.capabilities.get(bstack11ll11_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ᎕"))
        if bstack111l111ll_opy_:
            if bstack11l1llll_opy_() <= version.parse(bstack11ll11_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩ᎖")):
                self.command_executor._url = bstack11ll11_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ᎗") + bstack1llll1l11l_opy_ + bstack11ll11_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣ᎘")
            else:
                self.command_executor._url = bstack11ll11_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢ᎙") + bstack111l111ll_opy_ + bstack11ll11_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢ᎚")
            logger.debug(bstack1l11111l_opy_.format(bstack111l111ll_opy_))
        else:
            logger.debug(bstack11llll1l1_opy_.format(bstack11ll11_opy_ (u"ࠢࡐࡲࡷ࡭ࡲࡧ࡬ࠡࡊࡸࡦࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣ᎛")))
    except Exception as e:
        logger.debug(bstack11llll1l1_opy_.format(e))
    bstack1l11ll1l_opy_ = self.session_id
    if bstack11ll11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ᎜") in bstack1llll1111l_opy_:
        threading.current_thread().bstack11l1ll1l_opy_ = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        bstack1llll1111_opy_.bstack1l111ll1_opy_(self)
    bstack1llll11l1_opy_.append(self)
    if bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ᎝") in CONFIG and bstack11ll11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ᎞") in CONFIG[bstack11ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᎟")][bstack111l111l_opy_]:
        bstack1l11lll11_opy_ = CONFIG[bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᎠ")][bstack111l111l_opy_][bstack11ll11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᎡ")]
    logger.debug(bstack1l11llll1_opy_.format(bstack1l11ll1l_opy_))
def bstack111ll1l1_opy_(self, url):
    global bstack11111ll1l_opy_
    global CONFIG
    try:
        bstack1lll1l11_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1lll11lll1_opy_.format(str(err)))
    try:
        bstack11111ll1l_opy_(self, url)
    except Exception as e:
        try:
            bstack11l11l11l_opy_ = str(e)
            if any(err_msg in bstack11l11l11l_opy_ for err_msg in bstack111ll11l1_opy_):
                bstack1lll1l11_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1lll11lll1_opy_.format(str(err)))
        raise e
def bstack1l111l11_opy_(item, when):
    global bstack111llll11_opy_
    try:
        bstack111llll11_opy_(item, when)
    except Exception as e:
        pass
def bstack1llllllll_opy_(item, call, rep):
    global bstack1l1ll111_opy_
    global bstack1llll11l1_opy_
    name = bstack11ll11_opy_ (u"ࠧࠨᎢ")
    try:
        if rep.when == bstack11ll11_opy_ (u"ࠨࡥࡤࡰࡱ࠭Ꭳ"):
            bstack1l11ll1l_opy_ = threading.current_thread().bstack11l1ll1l_opy_
            bstack11lll11l1l_opy_ = item.config.getoption(bstack11ll11_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᎤ"))
            try:
                if (str(bstack11lll11l1l_opy_).lower() != bstack11ll11_opy_ (u"ࠪࡸࡷࡻࡥࠨᎥ")):
                    name = str(rep.nodeid)
                    bstack11llll11l_opy_ = bstack1l1ll11ll_opy_(bstack11ll11_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᎦ"), name, bstack11ll11_opy_ (u"ࠬ࠭Ꭷ"), bstack11ll11_opy_ (u"࠭ࠧᎨ"), bstack11ll11_opy_ (u"ࠧࠨᎩ"), bstack11ll11_opy_ (u"ࠨࠩᎪ"))
                    for driver in bstack1llll11l1_opy_:
                        if bstack1l11ll1l_opy_ == driver.session_id:
                            driver.execute_script(bstack11llll11l_opy_)
            except Exception as e:
                logger.debug(bstack11ll11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩᎫ").format(str(e)))
            try:
                status = bstack11ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᎬ") if rep.outcome.lower() == bstack11ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᎭ") else bstack11ll11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᎮ")
                reason = bstack11ll11_opy_ (u"࠭ࠧᎯ")
                if (reason != bstack11ll11_opy_ (u"ࠢࠣᎰ")):
                    try:
                        if (threading.current_thread().bstackTestErrorMessages == None):
                            threading.current_thread().bstackTestErrorMessages = []
                    except Exception as e:
                        threading.current_thread().bstackTestErrorMessages = []
                    threading.current_thread().bstackTestErrorMessages.append(str(reason))
                if status == bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᎱ"):
                    reason = rep.longrepr.reprcrash.message
                    if (not threading.current_thread().bstackTestErrorMessages):
                        threading.current_thread().bstackTestErrorMessages = []
                    threading.current_thread().bstackTestErrorMessages.append(reason)
                level = bstack11ll11_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧᎲ") if status == bstack11ll11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᎳ") else bstack11ll11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᎴ")
                data = name + bstack11ll11_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧᎵ") if status == bstack11ll11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭Ꮆ") else name + bstack11ll11_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪᎷ") + reason
                bstack1lll11ll1l_opy_ = bstack1l1ll11ll_opy_(bstack11ll11_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪᎸ"), bstack11ll11_opy_ (u"ࠩࠪᎹ"), bstack11ll11_opy_ (u"ࠪࠫᎺ"), bstack11ll11_opy_ (u"ࠫࠬᎻ"), level, data)
                for driver in bstack1llll11l1_opy_:
                    if bstack1l11ll1l_opy_ == driver.session_id:
                        driver.execute_script(bstack1lll11ll1l_opy_)
            except Exception as e:
                logger.debug(bstack11ll11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩᎼ").format(str(e)))
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪᎽ").format(str(e)))
    bstack1l1ll111_opy_(item, call, rep)
notset = Notset()
def bstack1111l1lll_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l1111lll_opy_
    if str(name).lower() == bstack11ll11_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧᎾ"):
        return bstack11ll11_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢᎿ")
    else:
        return bstack1l1111lll_opy_(self, name, default, skip)
def bstack11l1111l_opy_(self):
    global CONFIG
    global bstack11ll111l1_opy_
    try:
        proxy = bstack111l11111_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11ll11_opy_ (u"ࠩ࠱ࡴࡦࡩࠧᏀ")):
                proxies = bstack1ll1lll1ll_opy_(proxy, bstack1lllllll1_opy_())
                if len(proxies) > 0:
                    protocol, bstack11111lll_opy_ = proxies.popitem()
                    if bstack11ll11_opy_ (u"ࠥ࠾࠴࠵ࠢᏁ") in bstack11111lll_opy_:
                        return bstack11111lll_opy_
                    else:
                        return bstack11ll11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᏂ") + bstack11111lll_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11ll11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤᏃ").format(str(e)))
    return bstack11ll111l1_opy_(self)
def bstack1lll1lll1l_opy_():
    return bstack11ll11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᏄ") in CONFIG or bstack11ll11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᏅ") in CONFIG and bstack11l1llll_opy_() >= version.parse(
        bstack11111lll1_opy_)
def bstack1l11ll1l1_opy_(self,
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
    global bstack1l11lll11_opy_
    global bstack1ll111ll_opy_
    global bstack1llll1111l_opy_
    CONFIG[bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᏆ")] = str(bstack1llll1111l_opy_) + str(__version__)
    bstack111l111l_opy_ = 0
    try:
        if bstack1ll111ll_opy_ is True:
            bstack111l111l_opy_ = int(os.environ.get(bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᏇ")))
    except:
        bstack111l111l_opy_ = 0
    CONFIG[bstack11ll11_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᏈ")] = True
    bstack11111ll1_opy_ = bstack1ll11llll_opy_(CONFIG, bstack111l111l_opy_)
    logger.debug(bstack111111l1l_opy_.format(str(bstack11111ll1_opy_)))
    if CONFIG[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᏉ")]:
        bstack1llll1lll1_opy_(bstack11111ll1_opy_, bstack11l1l11ll_opy_)
    if bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᏊ") in CONFIG and bstack11ll11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᏋ") in CONFIG[bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᏌ")][bstack111l111l_opy_]:
        bstack1l11lll11_opy_ = CONFIG[bstack11ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᏍ")][bstack111l111l_opy_][bstack11ll11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᏎ")]
    import urllib
    import json
    bstack1ll1l111ll_opy_ = bstack11ll11_opy_ (u"ࠪࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠬᏏ") + urllib.parse.quote(json.dumps(bstack11111ll1_opy_))
    browser = self.connect(bstack1ll1l111ll_opy_)
    return browser
def bstack11lll111l_opy_():
    global bstack1l1l1ll1l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1l11ll1l1_opy_
        bstack1l1l1ll1l_opy_ = True
    except Exception as e:
        pass
def bstack11ll1l11ll_opy_():
    global CONFIG
    global bstack1l11111l1_opy_
    global bstack1llll1l11l_opy_
    global bstack11l1l11ll_opy_
    global bstack1ll111ll_opy_
    CONFIG = json.loads(os.environ.get(bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪᏐ")))
    bstack1l11111l1_opy_ = eval(os.environ.get(bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭Ꮡ")))
    bstack1llll1l11l_opy_ = os.environ.get(bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡎࡕࡃࡡࡘࡖࡑ࠭Ꮢ"))
    bstack1ll1lll11_opy_(CONFIG, bstack1l11111l1_opy_)
    bstack1l1llllll_opy_()
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
    if bstack11ll11_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᏓ") in CONFIG or bstack11ll11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᏔ") in CONFIG:
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
        logger.debug(bstack11ll11_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪᏕ"))
    bstack11l1l11ll_opy_ = CONFIG.get(bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧᏖ"), {}).get(bstack11ll11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭Ꮧ"))
    bstack1ll111ll_opy_ = True
    bstack1l1lll1l1_opy_(bstack1ll111ll1_opy_)
if (bstack1ll1111l1l_opy_()):
    bstack11ll1l11ll_opy_()
@bstack1l1ll11l1l_opy_(class_method=False)
def bstack11ll1llll1_opy_(hook_name, event, bstack11ll11lll1_opy_=None):
    if hook_name not in [bstack11ll11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭Ꮨ"), bstack11ll11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᏙ"), bstack11ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭Ꮪ"), bstack11ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᏛ"), bstack11ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧᏜ"), bstack11ll11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫᏝ"), bstack11ll11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪᏞ"), bstack11ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᏟ")]:
        return
    node = store[bstack11ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪᏠ")]
    if hook_name in [bstack11ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭Ꮱ"), bstack11ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᏢ")]:
        node = store[bstack11ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨᏣ")]
    elif hook_name in [bstack11ll11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᏤ"), bstack11ll11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬᏥ")]:
        node = store[bstack11ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪᏦ")]
    if event == bstack11ll11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭Ꮷ"):
        hook_type = bstack1l1l111lll_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack11lll1ll11_opy_ = {
            bstack11ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᏨ"): uuid,
            bstack11ll11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᏩ"): bstack1l111l1l1_opy_(),
            bstack11ll11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᏪ"): bstack11ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᏫ"),
            bstack11ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᏬ"): hook_type,
            bstack11ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨᏭ"): hook_name
        }
        store[bstack11ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᏮ")].append(uuid)
        bstack11ll1lllll_opy_ = node.nodeid
        if hook_type == bstack11ll11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᏯ"):
            if not _11lll1l11l_opy_.get(bstack11ll1lllll_opy_, None):
                _11lll1l11l_opy_[bstack11ll1lllll_opy_] = {bstack11ll11_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᏰ"): []}
            _11lll1l11l_opy_[bstack11ll1lllll_opy_][bstack11ll11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᏱ")].append(bstack11lll1ll11_opy_[bstack11ll11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᏲ")])
        _11lll1l11l_opy_[bstack11ll1lllll_opy_ + bstack11ll11_opy_ (u"ࠫ࠲࠭Ᏻ") + hook_name] = bstack11lll1ll11_opy_
        bstack11ll1ll1l1_opy_(node, bstack11lll1ll11_opy_, bstack11ll11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭Ᏼ"))
    elif event == bstack11ll11_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᏵ"):
        bstack11ll11l11l_opy_ = node.nodeid + bstack11ll11_opy_ (u"ࠧ࠮ࠩ᏶") + hook_name
        _11lll1l11l_opy_[bstack11ll11l11l_opy_][bstack11ll11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᏷")] = bstack1l111l1l1_opy_()
        bstack11ll1lll1l_opy_(_11lll1l11l_opy_[bstack11ll11l11l_opy_][bstack11ll11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᏸ")])
        bstack11ll1ll1l1_opy_(node, _11lll1l11l_opy_[bstack11ll11l11l_opy_], bstack11ll11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᏹ"), bstack11lll111ll_opy_=bstack11ll11lll1_opy_)
def bstack11lll111l1_opy_():
    global bstack11ll1l1l1l_opy_
    if bstack1l1lllll1_opy_():
        bstack11ll1l1l1l_opy_ = bstack11ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᏺ")
    else:
        bstack11ll1l1l1l_opy_ = bstack11ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᏻ")
@bstack1llll1111_opy_.bstack1l11111lll_opy_
def bstack11ll11l1l1_opy_():
    bstack11lll111l1_opy_()
    if bstack1ll111l111_opy_():
        bstack1l11l1ll11_opy_(bstack11ll1l1111_opy_)
    bstack1l1l1llll1_opy_ = bstack1l1l1ll1l1_opy_(bstack11ll1llll1_opy_)
bstack11ll11l1l1_opy_()