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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack1l1ll1lll1_opy_, bstack1lll1ll11_opy_, get_host_info, bstack1l1lll1lll_opy_, bstack1l1lllllll_opy_, bstack1l1lllll1l_opy_, \
    bstack1l1lll1ll1_opy_, bstack1l1ll1l111_opy_, bstack111lll111_opy_, bstack1l1llll111_opy_, bstack1ll1111l1l_opy_, bstack1ll11111l1_opy_
from bstack_utils.bstack1l11ll11l1_opy_ import bstack1l11lll1l1_opy_
from bstack_utils.bstack1l111l1l1l_opy_ import bstack1l111ll1ll_opy_
bstack11lllll1l1_opy_ = [
    bstack11l1l1_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᅔ"), bstack11l1l1_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪᅕ"), bstack11l1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᅖ"), bstack11l1l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᅗ"),
    bstack11l1l1_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᅘ"), bstack11l1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᅙ"), bstack11l1l1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᅚ")
]
bstack1l111111l1_opy_ = bstack11l1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡣࡰ࡮࡯ࡩࡨࡺ࡯ࡳ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᅛ")
logger = logging.getLogger(__name__)
class bstack1lll11ll11_opy_:
    bstack1l11ll11l1_opy_ = None
    bs_config = None
    @classmethod
    @bstack1ll11111l1_opy_(class_method=True)
    def launch(cls, bs_config, bstack1l1111l11l_opy_):
        cls.bs_config = bs_config
        if not cls.bstack11lll1llll_opy_():
            return
        cls.bstack1l1111ll1l_opy_()
        bstack1l1111111l_opy_ = bstack1l1lll1lll_opy_(bs_config)
        bstack1l1111l111_opy_ = bstack1l1lllllll_opy_(bs_config)
        data = {
            bstack11l1l1_opy_ (u"࠭ࡦࡰࡴࡰࡥࡹ࠭ᅜ"): bstack11l1l1_opy_ (u"ࠧ࡫ࡵࡲࡲࠬᅝ"),
            bstack11l1l1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡡࡱࡥࡲ࡫ࠧᅞ"): bs_config.get(bstack11l1l1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᅟ"), bstack11l1l1_opy_ (u"ࠪࠫᅠ")),
            bstack11l1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᅡ"): bs_config.get(bstack11l1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᅢ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack11l1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᅣ"): bs_config.get(bstack11l1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᅤ")),
            bstack11l1l1_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᅥ"): bs_config.get(bstack11l1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᅦ"), bstack11l1l1_opy_ (u"ࠪࠫᅧ")),
            bstack11l1l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡢࡸ࡮ࡳࡥࠨᅨ"): datetime.datetime.now().isoformat(),
            bstack11l1l1_opy_ (u"ࠬࡺࡡࡨࡵࠪᅩ"): bstack1l1lllll1l_opy_(bs_config),
            bstack11l1l1_opy_ (u"࠭ࡨࡰࡵࡷࡣ࡮ࡴࡦࡰࠩᅪ"): get_host_info(),
            bstack11l1l1_opy_ (u"ࠧࡤ࡫ࡢ࡭ࡳ࡬࡯ࠨᅫ"): bstack1lll1ll11_opy_(),
            bstack11l1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡳࡷࡱࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᅬ"): os.environ.get(bstack11l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨᅭ")),
            bstack11l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡵࡩࡷࡻ࡮ࠨᅮ"): os.environ.get(bstack11l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠩᅯ"), False),
            bstack11l1l1_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡥࡣࡰࡰࡷࡶࡴࡲࠧᅰ"): bstack1l1ll1lll1_opy_(),
            bstack11l1l1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᅱ"): {
                bstack11l1l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧᅲ"): bstack1l1111l11l_opy_.get(bstack11l1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩᅳ"), bstack11l1l1_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩᅴ")),
                bstack11l1l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᅵ"): bstack1l1111l11l_opy_.get(bstack11l1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᅶ")),
                bstack11l1l1_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᅷ"): bstack1l1111l11l_opy_.get(bstack11l1l1_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫᅸ"))
            }
        }
        config = {
            bstack11l1l1_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᅹ"): (bstack1l1111111l_opy_, bstack1l1111l111_opy_),
            bstack11l1l1_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᅺ"): cls.default_headers()
        }
        response = bstack111lll111_opy_(bstack11l1l1_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᅻ"), cls.request_url(bstack11l1l1_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵࠪᅼ")), data, config)
        if response.status_code != 200:
            os.environ[bstack11l1l1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪᅽ")] = bstack11l1l1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫᅾ")
            os.environ[bstack11l1l1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᅿ")] = bstack11l1l1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᆀ")
            os.environ[bstack11l1l1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧᆁ")] = bstack11l1l1_opy_ (u"ࠤࡱࡹࡱࡲࠢᆂ")
            os.environ[bstack11l1l1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫᆃ")] = bstack11l1l1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᆄ")
            bstack1l11111l1l_opy_ = response.json()
            if bstack1l11111l1l_opy_ and bstack1l11111l1l_opy_[bstack11l1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᆅ")]:
                error_message = bstack1l11111l1l_opy_[bstack11l1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᆆ")]
                if bstack1l11111l1l_opy_[bstack11l1l1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࡚ࡹࡱࡧࠪᆇ")] == bstack11l1l1_opy_ (u"ࠨࡇࡕࡖࡔࡘ࡟ࡊࡐ࡙ࡅࡑࡏࡄࡠࡅࡕࡉࡉࡋࡎࡕࡋࡄࡐࡘ࠭ᆈ"):
                    logger.error(error_message)
                elif bstack1l11111l1l_opy_[bstack11l1l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࡕࡻࡳࡩࠬᆉ")] == bstack11l1l1_opy_ (u"ࠪࡉࡗࡘࡏࡓࡡࡄࡇࡈࡋࡓࡔࡡࡇࡉࡓࡏࡅࡅࠩᆊ"):
                    logger.info(error_message)
                elif bstack1l11111l1l_opy_[bstack11l1l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࡗࡽࡵ࡫ࠧᆋ")] == bstack11l1l1_opy_ (u"ࠬࡋࡒࡓࡑࡕࡣࡘࡊࡋࡠࡆࡈࡔࡗࡋࡃࡂࡖࡈࡈࠬᆌ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l1ll1ll11_opy_ (u"ࠨࡄࡢࡶࡤࠤࡺࡶ࡬ࡰࡣࡧࠤࡹࡵࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡩࡻࡥࠡࡶࡲࠤࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣᆍ"))
            return [None, None, None]
        logger.debug(bstack11l1l1_opy_ (u"ࠧࡕࡧࡶࡸࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫᆎ"))
        os.environ[bstack11l1l1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧᆏ")] = bstack11l1l1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᆐ")
        bstack1l11111l1l_opy_ = response.json()
        if bstack1l11111l1l_opy_.get(bstack11l1l1_opy_ (u"ࠪ࡮ࡼࡺࠧᆑ")):
            os.environ[bstack11l1l1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᆒ")] = bstack1l11111l1l_opy_[bstack11l1l1_opy_ (u"ࠬࡰࡷࡵࠩᆓ")]
            os.environ[bstack11l1l1_opy_ (u"࠭ࡃࡓࡇࡇࡉࡓ࡚ࡉࡂࡎࡖࡣࡋࡕࡒࡠࡅࡕࡅࡘࡎ࡟ࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠪᆔ")] = json.dumps({
                bstack11l1l1_opy_ (u"ࠧࡶࡵࡨࡶࡳࡧ࡭ࡦࠩᆕ"): bstack1l1111111l_opy_,
                bstack11l1l1_opy_ (u"ࠨࡲࡤࡷࡸࡽ࡯ࡳࡦࠪᆖ"): bstack1l1111l111_opy_
            })
        if bstack1l11111l1l_opy_.get(bstack11l1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᆗ")):
            os.environ[bstack11l1l1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᆘ")] = bstack1l11111l1l_opy_[bstack11l1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᆙ")]
        if bstack1l11111l1l_opy_.get(bstack11l1l1_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᆚ")):
            os.environ[bstack11l1l1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧᆛ")] = str(bstack1l11111l1l_opy_[bstack11l1l1_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᆜ")])
        return [bstack1l11111l1l_opy_[bstack11l1l1_opy_ (u"ࠨ࡬ࡺࡸࠬᆝ")], bstack1l11111l1l_opy_[bstack11l1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᆞ")], bstack1l11111l1l_opy_[bstack11l1l1_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᆟ")]]
    @classmethod
    @bstack1ll11111l1_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack11l1l1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᆠ")] == bstack11l1l1_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᆡ") or os.environ[bstack11l1l1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬᆢ")] == bstack11l1l1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᆣ"):
            print(bstack11l1l1_opy_ (u"ࠨࡇ࡛ࡇࡊࡖࡔࡊࡑࡑࠤࡎࡔࠠࡴࡶࡲࡴࡇࡻࡩ࡭ࡦࡘࡴࡸࡺࡲࡦࡣࡰࠤࡗࡋࡑࡖࡇࡖࡘ࡚ࠥࡏࠡࡖࡈࡗ࡙ࠦࡏࡃࡕࡈࡖ࡛ࡇࡂࡊࡎࡌࡘ࡞ࠦ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩᆤ"))
            return {
                bstack11l1l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᆥ"): bstack11l1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᆦ"),
                bstack11l1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᆧ"): bstack11l1l1_opy_ (u"࡚ࠬ࡯࡬ࡧࡱ࠳ࡧࡻࡩ࡭ࡦࡌࡈࠥ࡯ࡳࠡࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧ࠰ࠥࡨࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦ࡭ࡪࡩ࡫ࡸࠥ࡮ࡡࡷࡧࠣࡪࡦ࡯࡬ࡦࡦࠪᆨ")
            }
        else:
            cls.bstack1l11ll11l1_opy_.shutdown()
            data = {
                bstack11l1l1_opy_ (u"࠭ࡳࡵࡱࡳࡣࡹ࡯࡭ࡦࠩᆩ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack11l1l1_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᆪ"): cls.default_headers()
            }
            bstack1ll111l11l_opy_ = bstack11l1l1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸࡺ࡯ࡱࠩᆫ").format(os.environ[bstack11l1l1_opy_ (u"ࠤࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠣᆬ")])
            bstack1l1111l1ll_opy_ = cls.request_url(bstack1ll111l11l_opy_)
            response = bstack111lll111_opy_(bstack11l1l1_opy_ (u"ࠪࡔ࡚࡚ࠧᆭ"), bstack1l1111l1ll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11l1l1_opy_ (u"ࠦࡘࡺ࡯ࡱࠢࡵࡩࡶࡻࡥࡴࡶࠣࡲࡴࡺࠠࡰ࡭ࠥᆮ"))
    @classmethod
    def bstack11lllll1ll_opy_(cls):
        if cls.bstack1l11ll11l1_opy_ is None:
            return
        cls.bstack1l11ll11l1_opy_.shutdown()
    @classmethod
    def bstack11lll1ll1_opy_(cls):
        if cls.on():
            print(
                bstack11l1l1_opy_ (u"ࠬ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠤࡹࡵࠠࡷ࡫ࡨࡻࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡰࡰࡴࡷ࠰ࠥ࡯࡮ࡴ࡫ࡪ࡬ࡹࡹࠬࠡࡣࡱࡨࠥࡳࡡ࡯ࡻࠣࡱࡴࡸࡥࠡࡦࡨࡦࡺ࡭ࡧࡪࡰࡪࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯ࠢࡤࡰࡱࠦࡡࡵࠢࡲࡲࡪࠦࡰ࡭ࡣࡦࡩࠦࡢ࡮ࠨᆯ").format(os.environ[bstack11l1l1_opy_ (u"ࠨࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠧᆰ")]))
    @classmethod
    def bstack1l1111ll1l_opy_(cls):
        if cls.bstack1l11ll11l1_opy_ is not None:
            return
        cls.bstack1l11ll11l1_opy_ = bstack1l11lll1l1_opy_(cls.bstack1l11111ll1_opy_)
        cls.bstack1l11ll11l1_opy_.start()
    @classmethod
    def bstack1l1111ll11_opy_(cls, bstack11lll1lll1_opy_, bstack1l1111l1l1_opy_=bstack11l1l1_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭ᆱ")):
        if not cls.on():
            return
        bstack11l1llll1_opy_ = bstack11lll1lll1_opy_[bstack11l1l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᆲ")]
        bstack11lllll11l_opy_ = {
            bstack11l1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᆳ"): bstack11l1l1_opy_ (u"ࠪࡘࡪࡹࡴࡠࡕࡷࡥࡷࡺ࡟ࡖࡲ࡯ࡳࡦࡪࠧᆴ"),
            bstack11l1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᆵ"): bstack11l1l1_opy_ (u"࡚ࠬࡥࡴࡶࡢࡉࡳࡪ࡟ࡖࡲ࡯ࡳࡦࡪࠧᆶ"),
            bstack11l1l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧᆷ"): bstack11l1l1_opy_ (u"ࠧࡕࡧࡶࡸࡤ࡙࡫ࡪࡲࡳࡩࡩࡥࡕࡱ࡮ࡲࡥࡩ࠭ᆸ"),
            bstack11l1l1_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᆹ"): bstack11l1l1_opy_ (u"ࠩࡏࡳ࡬ࡥࡕࡱ࡮ࡲࡥࡩ࠭ᆺ"),
            bstack11l1l1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᆻ"): bstack11l1l1_opy_ (u"ࠫࡍࡵ࡯࡬ࡡࡖࡸࡦࡸࡴࡠࡗࡳࡰࡴࡧࡤࠨᆼ"),
            bstack11l1l1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᆽ"): bstack11l1l1_opy_ (u"࠭ࡈࡰࡱ࡮ࡣࡊࡴࡤࡠࡗࡳࡰࡴࡧࡤࠨᆾ"),
            bstack11l1l1_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫᆿ"): bstack11l1l1_opy_ (u"ࠨࡅࡅࡘࡤ࡛ࡰ࡭ࡱࡤࡨࠬᇀ")
        }.get(bstack11l1llll1_opy_)
        if bstack1l1111l1l1_opy_ == bstack11l1l1_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨᇁ"):
            cls.bstack1l1111ll1l_opy_()
            cls.bstack1l11ll11l1_opy_.add(bstack11lll1lll1_opy_)
        elif bstack1l1111l1l1_opy_ == bstack11l1l1_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᇂ"):
            cls.bstack1l11111ll1_opy_([bstack11lll1lll1_opy_], bstack1l1111l1l1_opy_)
    @classmethod
    @bstack1ll11111l1_opy_(class_method=True)
    def bstack1l11111ll1_opy_(cls, bstack11lll1lll1_opy_, bstack1l1111l1l1_opy_=bstack11l1l1_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪᇃ")):
        config = {
            bstack11l1l1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᇄ"): cls.default_headers()
        }
        response = bstack111lll111_opy_(bstack11l1l1_opy_ (u"࠭ࡐࡐࡕࡗࠫᇅ"), cls.request_url(bstack1l1111l1l1_opy_), bstack11lll1lll1_opy_, config)
        bstack11llll1l11_opy_ = response.json()
    @classmethod
    @bstack1ll11111l1_opy_(class_method=True)
    def bstack11llllll1l_opy_(cls, bstack11llll1lll_opy_):
        bstack11lllllll1_opy_ = []
        for log in bstack11llll1lll_opy_:
            bstack11llll1l1l_opy_ = {
                bstack11l1l1_opy_ (u"ࠧ࡬࡫ࡱࡨࠬᇆ"): bstack11l1l1_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡌࡐࡉࠪᇇ"),
                bstack11l1l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᇈ"): log[bstack11l1l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᇉ")],
                bstack11l1l1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᇊ"): log[bstack11l1l1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᇋ")],
                bstack11l1l1_opy_ (u"࠭ࡨࡵࡶࡳࡣࡷ࡫ࡳࡱࡱࡱࡷࡪ࠭ᇌ"): {},
                bstack11l1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᇍ"): log[bstack11l1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᇎ")],
            }
            if bstack11l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᇏ") in log:
                bstack11llll1l1l_opy_[bstack11l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᇐ")] = log[bstack11l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᇑ")]
            elif bstack11l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᇒ") in log:
                bstack11llll1l1l_opy_[bstack11l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᇓ")] = log[bstack11l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᇔ")]
            bstack11lllllll1_opy_.append(bstack11llll1l1l_opy_)
        cls.bstack1l1111ll11_opy_({
            bstack11l1l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᇕ"): bstack11l1l1_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᇖ"),
            bstack11l1l1_opy_ (u"ࠪࡰࡴ࡭ࡳࠨᇗ"): bstack11lllllll1_opy_
        })
    @classmethod
    @bstack1ll11111l1_opy_(class_method=True)
    def bstack1l11111lll_opy_(cls, steps):
        bstack1l111111ll_opy_ = []
        for step in steps:
            bstack11llllllll_opy_ = {
                bstack11l1l1_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᇘ"): bstack11l1l1_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗ࡙ࡋࡐࠨᇙ"),
                bstack11l1l1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᇚ"): step[bstack11l1l1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᇛ")],
                bstack11l1l1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᇜ"): step[bstack11l1l1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᇝ")],
                bstack11l1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᇞ"): step[bstack11l1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᇟ")],
                bstack11l1l1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᇠ"): step[bstack11l1l1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨᇡ")]
            }
            if bstack11l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᇢ") in step:
                bstack11llllllll_opy_[bstack11l1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᇣ")] = step[bstack11l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᇤ")]
            elif bstack11l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᇥ") in step:
                bstack11llllllll_opy_[bstack11l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᇦ")] = step[bstack11l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᇧ")]
            bstack1l111111ll_opy_.append(bstack11llllllll_opy_)
        cls.bstack1l1111ll11_opy_({
            bstack11l1l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᇨ"): bstack11l1l1_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᇩ"),
            bstack11l1l1_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭ᇪ"): bstack1l111111ll_opy_
        })
    @classmethod
    @bstack1ll11111l1_opy_(class_method=True)
    def bstack1l11111l11_opy_(cls, screenshot):
        cls.bstack1l1111ll11_opy_({
            bstack11l1l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᇫ"): bstack11l1l1_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧᇬ"),
            bstack11l1l1_opy_ (u"ࠫࡱࡵࡧࡴࠩᇭ"): [{
                bstack11l1l1_opy_ (u"ࠬࡱࡩ࡯ࡦࠪᇮ"): bstack11l1l1_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠨᇯ"),
                bstack11l1l1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᇰ"): datetime.datetime.utcnow().isoformat() + bstack11l1l1_opy_ (u"ࠨ࡜ࠪᇱ"),
                bstack11l1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᇲ"): screenshot[bstack11l1l1_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩᇳ")],
                bstack11l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᇴ"): screenshot[bstack11l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᇵ")]
            }]
        }, bstack1l1111l1l1_opy_=bstack11l1l1_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᇶ"))
    @classmethod
    @bstack1ll11111l1_opy_(class_method=True)
    def bstack1ll1l1l1ll_opy_(cls, driver):
        bstack11lll1ll1l_opy_ = cls.bstack11lll1ll1l_opy_()
        if not bstack11lll1ll1l_opy_:
            return
        cls.bstack1l1111ll11_opy_({
            bstack11l1l1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᇷ"): bstack11l1l1_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬᇸ"),
            bstack11l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫᇹ"): {
                bstack11l1l1_opy_ (u"ࠥࡹࡺ࡯ࡤࠣᇺ"): cls.bstack11lll1ll1l_opy_(),
                bstack11l1l1_opy_ (u"ࠦ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠥᇻ"): cls.bstack11llll1ll1_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack11l1l1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᇼ"), None) is None or os.environ[bstack11l1l1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᇽ")] == bstack11l1l1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᇾ"):
            return False
        return True
    @classmethod
    def bstack11lll1llll_opy_(cls):
        return bstack1ll1111l1l_opy_(cls.bs_config.get(bstack11l1l1_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᇿ"), False))
    @staticmethod
    def request_url(url):
        return bstack11l1l1_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨሀ").format(bstack1l111111l1_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack11l1l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩሁ"): bstack11l1l1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧሂ"),
            bstack11l1l1_opy_ (u"ࠬ࡞࠭ࡃࡕࡗࡅࡈࡑ࠭ࡕࡇࡖࡘࡔࡖࡓࠨሃ"): bstack11l1l1_opy_ (u"࠭ࡴࡳࡷࡨࠫሄ")
        }
        if os.environ.get(bstack11l1l1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨህ"), None):
            headers[bstack11l1l1_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨሆ")] = bstack11l1l1_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬሇ").format(os.environ[bstack11l1l1_opy_ (u"ࠥࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠦለ")])
        return headers
    @staticmethod
    def bstack11lll1ll1l_opy_():
        return getattr(threading.current_thread(), bstack11l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨሉ"), None)
    @staticmethod
    def bstack11llll1ll1_opy_(driver):
        return {
            bstack1l1ll1l111_opy_(): bstack1l1lll1ll1_opy_(driver)
        }
    @staticmethod
    def bstack11llll111l_opy_(exception_info, report):
        return [{bstack11l1l1_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨሊ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1ll11111ll_opy_(typename):
        if bstack11l1l1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤላ") in typename:
            return bstack11l1l1_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣሌ")
        return bstack11l1l1_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤል")
    @staticmethod
    def bstack11lllll111_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1lll11ll11_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11llll1111_opy_(test, hook_name=None):
        bstack11llllll11_opy_ = test.parent
        if hook_name in [bstack11l1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧሎ"), bstack11l1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫሏ"), bstack11l1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪሐ"), bstack11l1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧሑ")]:
            bstack11llllll11_opy_ = test
        scope = []
        while bstack11llllll11_opy_ is not None:
            scope.append(bstack11llllll11_opy_.name)
            bstack11llllll11_opy_ = bstack11llllll11_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1l11111111_opy_(hook_type):
        if hook_type == bstack11l1l1_opy_ (u"ࠨࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠦሒ"):
            return bstack11l1l1_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡨࡰࡱ࡮ࠦሓ")
        elif hook_type == bstack11l1l1_opy_ (u"ࠣࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠧሔ"):
            return bstack11l1l1_opy_ (u"ࠤࡗࡩࡦࡸࡤࡰࡹࡱࠤ࡭ࡵ࡯࡬ࠤሕ")
    @staticmethod
    def bstack11llll11l1_opy_(bstack1ll11l1l1_opy_):
        try:
            if not bstack1lll11ll11_opy_.on():
                return bstack1ll11l1l1_opy_
            if os.environ.get(bstack11l1l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠣሖ"), None) == bstack11l1l1_opy_ (u"ࠦࡹࡸࡵࡦࠤሗ"):
                tests = os.environ.get(bstack11l1l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠤመ"), None)
                if tests is None or tests == bstack11l1l1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦሙ"):
                    return bstack1ll11l1l1_opy_
                bstack1ll11l1l1_opy_ = tests.split(bstack11l1l1_opy_ (u"ࠧ࠭ࠩሚ"))
                return bstack1ll11l1l1_opy_
        except Exception as exc:
            print(bstack11l1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡳࡧࡵࡹࡳࠦࡨࡢࡰࡧࡰࡪࡸ࠺ࠡࠤማ"), str(exc))
        return bstack1ll11l1l1_opy_
    @classmethod
    def bstack11llll11ll_opy_(cls, event: str, bstack11lll1lll1_opy_: bstack1l111ll1ll_opy_):
        bstack11lll1ll11_opy_ = {
            bstack11l1l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ሜ"): event,
            bstack11lll1lll1_opy_.bstack1l111l1l11_opy_(): bstack11lll1lll1_opy_.bstack1l11l11111_opy_(event)
        }
        bstack1lll11ll11_opy_.bstack1l1111ll11_opy_(bstack11lll1ll11_opy_)