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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack1l1llll11l_opy_, bstack111l11l1l_opy_, get_host_info, bstack1l1lllll1l_opy_, bstack1l1ll1llll_opy_, bstack1l1lllll11_opy_, \
    bstack1ll1111l11_opy_, bstack1l1ll11lll_opy_, bstack1l1l1ll1_opy_, bstack1l1ll1l111_opy_, bstack1ll1111111_opy_, bstack1l1ll11l1l_opy_
from bstack_utils.bstack1l11lll11l_opy_ import bstack1l11lll111_opy_
from bstack_utils.bstack1l111ll1ll_opy_ import bstack1l111ll11l_opy_
bstack11llllll1l_opy_ = [
    bstack11ll11_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᅢ"), bstack11ll11_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪᅣ"), bstack11ll11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᅤ"), bstack11ll11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᅥ"),
    bstack11ll11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᅦ"), bstack11ll11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᅧ"), bstack11ll11_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᅨ")
]
bstack11lll1ll1l_opy_ = bstack11ll11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡣࡰ࡮࡯ࡩࡨࡺ࡯ࡳ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᅩ")
logger = logging.getLogger(__name__)
class bstack1llll1111_opy_:
    bstack1l11lll11l_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l1ll11l1l_opy_(class_method=True)
    def launch(cls, bs_config, bstack11llll1111_opy_):
        cls.bs_config = bs_config
        if not cls.bstack11llll11ll_opy_():
            return
        cls.bstack11lllllll1_opy_()
        bstack1l1111l1l1_opy_ = bstack1l1lllll1l_opy_(bs_config)
        bstack11llll1lll_opy_ = bstack1l1ll1llll_opy_(bs_config)
        data = {
            bstack11ll11_opy_ (u"࠭ࡦࡰࡴࡰࡥࡹ࠭ᅪ"): bstack11ll11_opy_ (u"ࠧ࡫ࡵࡲࡲࠬᅫ"),
            bstack11ll11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡡࡱࡥࡲ࡫ࠧᅬ"): bs_config.get(bstack11ll11_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᅭ"), bstack11ll11_opy_ (u"ࠪࠫᅮ")),
            bstack11ll11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᅯ"): bs_config.get(bstack11ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᅰ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack11ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᅱ"): bs_config.get(bstack11ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᅲ")),
            bstack11ll11_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᅳ"): bs_config.get(bstack11ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᅴ"), bstack11ll11_opy_ (u"ࠪࠫᅵ")),
            bstack11ll11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡢࡸ࡮ࡳࡥࠨᅶ"): datetime.datetime.now().isoformat(),
            bstack11ll11_opy_ (u"ࠬࡺࡡࡨࡵࠪᅷ"): bstack1l1lllll11_opy_(bs_config),
            bstack11ll11_opy_ (u"࠭ࡨࡰࡵࡷࡣ࡮ࡴࡦࡰࠩᅸ"): get_host_info(),
            bstack11ll11_opy_ (u"ࠧࡤ࡫ࡢ࡭ࡳ࡬࡯ࠨᅹ"): bstack111l11l1l_opy_(),
            bstack11ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡳࡷࡱࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᅺ"): os.environ.get(bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨᅻ")),
            bstack11ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡵࡩࡷࡻ࡮ࠨᅼ"): os.environ.get(bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠩᅽ"), False),
            bstack11ll11_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡥࡣࡰࡰࡷࡶࡴࡲࠧᅾ"): bstack1l1llll11l_opy_(),
            bstack11ll11_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᅿ"): {
                bstack11ll11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧᆀ"): bstack11llll1111_opy_.get(bstack11ll11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩᆁ"), bstack11ll11_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩᆂ")),
                bstack11ll11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᆃ"): bstack11llll1111_opy_.get(bstack11ll11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᆄ")),
                bstack11ll11_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᆅ"): bstack11llll1111_opy_.get(bstack11ll11_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫᆆ"))
            }
        }
        config = {
            bstack11ll11_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᆇ"): (bstack1l1111l1l1_opy_, bstack11llll1lll_opy_),
            bstack11ll11_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᆈ"): cls.default_headers()
        }
        response = bstack1l1l1ll1_opy_(bstack11ll11_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᆉ"), cls.request_url(bstack11ll11_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵࠪᆊ")), data, config)
        if response.status_code != 200:
            os.environ[bstack11ll11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪᆋ")] = bstack11ll11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫᆌ")
            os.environ[bstack11ll11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᆍ")] = bstack11ll11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᆎ")
            os.environ[bstack11ll11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧᆏ")] = bstack11ll11_opy_ (u"ࠤࡱࡹࡱࡲࠢᆐ")
            os.environ[bstack11ll11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫᆑ")] = bstack11ll11_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᆒ")
            bstack1l11111ll1_opy_ = response.json()
            if bstack1l11111ll1_opy_ and bstack1l11111ll1_opy_[bstack11ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᆓ")]:
                error_message = bstack1l11111ll1_opy_[bstack11ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᆔ")]
                if bstack1l11111ll1_opy_[bstack11ll11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࡚ࡹࡱࡧࠪᆕ")] == bstack11ll11_opy_ (u"ࠨࡇࡕࡖࡔࡘ࡟ࡊࡐ࡙ࡅࡑࡏࡄࡠࡅࡕࡉࡉࡋࡎࡕࡋࡄࡐࡘ࠭ᆖ"):
                    logger.error(error_message)
                elif bstack1l11111ll1_opy_[bstack11ll11_opy_ (u"ࠩࡨࡶࡷࡵࡲࡕࡻࡳࡩࠬᆗ")] == bstack11ll11_opy_ (u"ࠪࡉࡗࡘࡏࡓࡡࡄࡇࡈࡋࡓࡔࡡࡇࡉࡓࡏࡅࡅࠩᆘ"):
                    logger.info(error_message)
                elif bstack1l11111ll1_opy_[bstack11ll11_opy_ (u"ࠫࡪࡸࡲࡰࡴࡗࡽࡵ࡫ࠧᆙ")] == bstack11ll11_opy_ (u"ࠬࡋࡒࡓࡑࡕࡣࡘࡊࡋࡠࡆࡈࡔࡗࡋࡃࡂࡖࡈࡈࠬᆚ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11ll11_opy_ (u"ࠨࡄࡢࡶࡤࠤࡺࡶ࡬ࡰࡣࡧࠤࡹࡵࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡩࡻࡥࠡࡶࡲࠤࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣᆛ"))
            return [None, None, None]
        logger.debug(bstack11ll11_opy_ (u"ࠧࡕࡧࡶࡸࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫᆜ"))
        os.environ[bstack11ll11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧᆝ")] = bstack11ll11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᆞ")
        bstack1l11111ll1_opy_ = response.json()
        if bstack1l11111ll1_opy_.get(bstack11ll11_opy_ (u"ࠪ࡮ࡼࡺࠧᆟ")):
            os.environ[bstack11ll11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᆠ")] = bstack1l11111ll1_opy_[bstack11ll11_opy_ (u"ࠬࡰࡷࡵࠩᆡ")]
            os.environ[bstack11ll11_opy_ (u"࠭ࡃࡓࡇࡇࡉࡓ࡚ࡉࡂࡎࡖࡣࡋࡕࡒࡠࡅࡕࡅࡘࡎ࡟ࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠪᆢ")] = json.dumps({
                bstack11ll11_opy_ (u"ࠧࡶࡵࡨࡶࡳࡧ࡭ࡦࠩᆣ"): bstack1l1111l1l1_opy_,
                bstack11ll11_opy_ (u"ࠨࡲࡤࡷࡸࡽ࡯ࡳࡦࠪᆤ"): bstack11llll1lll_opy_
            })
        if bstack1l11111ll1_opy_.get(bstack11ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᆥ")):
            os.environ[bstack11ll11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᆦ")] = bstack1l11111ll1_opy_[bstack11ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᆧ")]
        if bstack1l11111ll1_opy_.get(bstack11ll11_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᆨ")):
            os.environ[bstack11ll11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧᆩ")] = str(bstack1l11111ll1_opy_[bstack11ll11_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᆪ")])
        return [bstack1l11111ll1_opy_[bstack11ll11_opy_ (u"ࠨ࡬ࡺࡸࠬᆫ")], bstack1l11111ll1_opy_[bstack11ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᆬ")], bstack1l11111ll1_opy_[bstack11ll11_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᆭ")]]
    @classmethod
    @bstack1l1ll11l1l_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack11ll11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᆮ")] == bstack11ll11_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᆯ") or os.environ[bstack11ll11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬᆰ")] == bstack11ll11_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᆱ"):
            print(bstack11ll11_opy_ (u"ࠨࡇ࡛ࡇࡊࡖࡔࡊࡑࡑࠤࡎࡔࠠࡴࡶࡲࡴࡇࡻࡩ࡭ࡦࡘࡴࡸࡺࡲࡦࡣࡰࠤࡗࡋࡑࡖࡇࡖࡘ࡚ࠥࡏࠡࡖࡈࡗ࡙ࠦࡏࡃࡕࡈࡖ࡛ࡇࡂࡊࡎࡌࡘ࡞ࠦ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩᆲ"))
            return {
                bstack11ll11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᆳ"): bstack11ll11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᆴ"),
                bstack11ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᆵ"): bstack11ll11_opy_ (u"࡚ࠬ࡯࡬ࡧࡱ࠳ࡧࡻࡩ࡭ࡦࡌࡈࠥ࡯ࡳࠡࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧ࠰ࠥࡨࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦ࡭ࡪࡩ࡫ࡸࠥ࡮ࡡࡷࡧࠣࡪࡦ࡯࡬ࡦࡦࠪᆶ")
            }
        else:
            cls.bstack1l11lll11l_opy_.shutdown()
            data = {
                bstack11ll11_opy_ (u"࠭ࡳࡵࡱࡳࡣࡹ࡯࡭ࡦࠩᆷ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack11ll11_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᆸ"): cls.default_headers()
            }
            bstack1ll111l11l_opy_ = bstack11ll11_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸࡺ࡯ࡱࠩᆹ").format(os.environ[bstack11ll11_opy_ (u"ࠤࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠣᆺ")])
            bstack11lllll111_opy_ = cls.request_url(bstack1ll111l11l_opy_)
            response = bstack1l1l1ll1_opy_(bstack11ll11_opy_ (u"ࠪࡔ࡚࡚ࠧᆻ"), bstack11lllll111_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11ll11_opy_ (u"ࠦࡘࡺ࡯ࡱࠢࡵࡩࡶࡻࡥࡴࡶࠣࡲࡴࡺࠠࡰ࡭ࠥᆼ"))
    @classmethod
    def bstack11llll1l1l_opy_(cls):
        if cls.bstack1l11lll11l_opy_ is None:
            return
        cls.bstack1l11lll11l_opy_.shutdown()
    @classmethod
    def bstack1ll1l1ll1_opy_(cls):
        if cls.on():
            print(
                bstack11ll11_opy_ (u"ࠬ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠤࡹࡵࠠࡷ࡫ࡨࡻࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡰࡰࡴࡷ࠰ࠥ࡯࡮ࡴ࡫ࡪ࡬ࡹࡹࠬࠡࡣࡱࡨࠥࡳࡡ࡯ࡻࠣࡱࡴࡸࡥࠡࡦࡨࡦࡺ࡭ࡧࡪࡰࡪࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯ࠢࡤࡰࡱࠦࡡࡵࠢࡲࡲࡪࠦࡰ࡭ࡣࡦࡩࠦࡢ࡮ࠨᆽ").format(os.environ[bstack11ll11_opy_ (u"ࠨࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠧᆾ")]))
    @classmethod
    def bstack11lllllll1_opy_(cls):
        if cls.bstack1l11lll11l_opy_ is not None:
            return
        cls.bstack1l11lll11l_opy_ = bstack1l11lll111_opy_(cls.bstack1l11111l1l_opy_)
        cls.bstack1l11lll11l_opy_.start()
    @classmethod
    def bstack1l1111l1ll_opy_(cls, bstack1l1111ll11_opy_, bstack11lllll1l1_opy_=bstack11ll11_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭ᆿ")):
        if not cls.on():
            return
        bstack11lll1l1l_opy_ = bstack1l1111ll11_opy_[bstack11ll11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᇀ")]
        bstack11lllll1ll_opy_ = {
            bstack11ll11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᇁ"): bstack11ll11_opy_ (u"ࠪࡘࡪࡹࡴࡠࡕࡷࡥࡷࡺ࡟ࡖࡲ࡯ࡳࡦࡪࠧᇂ"),
            bstack11ll11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᇃ"): bstack11ll11_opy_ (u"࡚ࠬࡥࡴࡶࡢࡉࡳࡪ࡟ࡖࡲ࡯ࡳࡦࡪࠧᇄ"),
            bstack11ll11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧᇅ"): bstack11ll11_opy_ (u"ࠧࡕࡧࡶࡸࡤ࡙࡫ࡪࡲࡳࡩࡩࡥࡕࡱ࡮ࡲࡥࡩ࠭ᇆ"),
            bstack11ll11_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᇇ"): bstack11ll11_opy_ (u"ࠩࡏࡳ࡬ࡥࡕࡱ࡮ࡲࡥࡩ࠭ᇈ"),
            bstack11ll11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᇉ"): bstack11ll11_opy_ (u"ࠫࡍࡵ࡯࡬ࡡࡖࡸࡦࡸࡴࡠࡗࡳࡰࡴࡧࡤࠨᇊ"),
            bstack11ll11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᇋ"): bstack11ll11_opy_ (u"࠭ࡈࡰࡱ࡮ࡣࡊࡴࡤࡠࡗࡳࡰࡴࡧࡤࠨᇌ"),
            bstack11ll11_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫᇍ"): bstack11ll11_opy_ (u"ࠨࡅࡅࡘࡤ࡛ࡰ࡭ࡱࡤࡨࠬᇎ")
        }.get(bstack11lll1l1l_opy_)
        if bstack11lllll1l1_opy_ == bstack11ll11_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨᇏ"):
            cls.bstack11lllllll1_opy_()
            cls.bstack1l11lll11l_opy_.add(bstack1l1111ll11_opy_)
        elif bstack11lllll1l1_opy_ == bstack11ll11_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᇐ"):
            cls.bstack1l11111l1l_opy_([bstack1l1111ll11_opy_], bstack11lllll1l1_opy_)
    @classmethod
    @bstack1l1ll11l1l_opy_(class_method=True)
    def bstack1l11111l1l_opy_(cls, bstack1l1111ll11_opy_, bstack11lllll1l1_opy_=bstack11ll11_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪᇑ")):
        config = {
            bstack11ll11_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᇒ"): cls.default_headers()
        }
        response = bstack1l1l1ll1_opy_(bstack11ll11_opy_ (u"࠭ࡐࡐࡕࡗࠫᇓ"), cls.request_url(bstack11lllll1l1_opy_), bstack1l1111ll11_opy_, config)
        bstack1l1111111l_opy_ = response.json()
    @classmethod
    @bstack1l1ll11l1l_opy_(class_method=True)
    def bstack1l1111ll1l_opy_(cls, bstack1l111111l1_opy_):
        bstack11llllll11_opy_ = []
        for log in bstack1l111111l1_opy_:
            bstack1l1111l111_opy_ = {
                bstack11ll11_opy_ (u"ࠧ࡬࡫ࡱࡨࠬᇔ"): bstack11ll11_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡌࡐࡉࠪᇕ"),
                bstack11ll11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᇖ"): log[bstack11ll11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᇗ")],
                bstack11ll11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᇘ"): log[bstack11ll11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᇙ")],
                bstack11ll11_opy_ (u"࠭ࡨࡵࡶࡳࡣࡷ࡫ࡳࡱࡱࡱࡷࡪ࠭ᇚ"): {},
                bstack11ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᇛ"): log[bstack11ll11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᇜ")],
            }
            if bstack11ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᇝ") in log:
                bstack1l1111l111_opy_[bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᇞ")] = log[bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᇟ")]
            elif bstack11ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᇠ") in log:
                bstack1l1111l111_opy_[bstack11ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᇡ")] = log[bstack11ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᇢ")]
            bstack11llllll11_opy_.append(bstack1l1111l111_opy_)
        cls.bstack1l1111l1ll_opy_({
            bstack11ll11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᇣ"): bstack11ll11_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᇤ"),
            bstack11ll11_opy_ (u"ࠪࡰࡴ࡭ࡳࠨᇥ"): bstack11llllll11_opy_
        })
    @classmethod
    @bstack1l1ll11l1l_opy_(class_method=True)
    def bstack1l1111l11l_opy_(cls, steps):
        bstack11lllll11l_opy_ = []
        for step in steps:
            bstack1l11111l11_opy_ = {
                bstack11ll11_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᇦ"): bstack11ll11_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗ࡙ࡋࡐࠨᇧ"),
                bstack11ll11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᇨ"): step[bstack11ll11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᇩ")],
                bstack11ll11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᇪ"): step[bstack11ll11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᇫ")],
                bstack11ll11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᇬ"): step[bstack11ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᇭ")],
                bstack11ll11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᇮ"): step[bstack11ll11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨᇯ")]
            }
            if bstack11ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᇰ") in step:
                bstack1l11111l11_opy_[bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᇱ")] = step[bstack11ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᇲ")]
            elif bstack11ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᇳ") in step:
                bstack1l11111l11_opy_[bstack11ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᇴ")] = step[bstack11ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᇵ")]
            bstack11lllll11l_opy_.append(bstack1l11111l11_opy_)
        cls.bstack1l1111l1ll_opy_({
            bstack11ll11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᇶ"): bstack11ll11_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᇷ"),
            bstack11ll11_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭ᇸ"): bstack11lllll11l_opy_
        })
    @classmethod
    @bstack1l1ll11l1l_opy_(class_method=True)
    def bstack1l11111111_opy_(cls, screenshot):
        cls.bstack1l1111l1ll_opy_({
            bstack11ll11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᇹ"): bstack11ll11_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧᇺ"),
            bstack11ll11_opy_ (u"ࠫࡱࡵࡧࡴࠩᇻ"): [{
                bstack11ll11_opy_ (u"ࠬࡱࡩ࡯ࡦࠪᇼ"): bstack11ll11_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠨᇽ"),
                bstack11ll11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᇾ"): datetime.datetime.utcnow().isoformat() + bstack11ll11_opy_ (u"ࠨ࡜ࠪᇿ"),
                bstack11ll11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪሀ"): screenshot[bstack11ll11_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩሁ")],
                bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫሂ"): screenshot[bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬሃ")]
            }]
        }, bstack11lllll1l1_opy_=bstack11ll11_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫሄ"))
    @classmethod
    @bstack1l1ll11l1l_opy_(class_method=True)
    def bstack1l111ll1_opy_(cls, driver):
        bstack1l1111lll1_opy_ = cls.bstack1l1111lll1_opy_()
        if not bstack1l1111lll1_opy_:
            return
        cls.bstack1l1111l1ll_opy_({
            bstack11ll11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫህ"): bstack11ll11_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬሆ"),
            bstack11ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫሇ"): {
                bstack11ll11_opy_ (u"ࠥࡹࡺ࡯ࡤࠣለ"): cls.bstack1l1111lll1_opy_(),
                bstack11ll11_opy_ (u"ࠦ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠥሉ"): cls.bstack11llll1ll1_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack11ll11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ሊ"), None) is None or os.environ[bstack11ll11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧላ")] == bstack11ll11_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧሌ"):
            return False
        return True
    @classmethod
    def bstack11llll11ll_opy_(cls):
        return bstack1ll1111111_opy_(cls.bs_config.get(bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬል"), False))
    @staticmethod
    def request_url(url):
        return bstack11ll11_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨሎ").format(bstack11lll1ll1l_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack11ll11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩሏ"): bstack11ll11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧሐ"),
            bstack11ll11_opy_ (u"ࠬ࡞࠭ࡃࡕࡗࡅࡈࡑ࠭ࡕࡇࡖࡘࡔࡖࡓࠨሑ"): bstack11ll11_opy_ (u"࠭ࡴࡳࡷࡨࠫሒ")
        }
        if os.environ.get(bstack11ll11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨሓ"), None):
            headers[bstack11ll11_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨሔ")] = bstack11ll11_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬሕ").format(os.environ[bstack11ll11_opy_ (u"ࠥࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠦሖ")])
        return headers
    @staticmethod
    def bstack1l1111lll1_opy_():
        return getattr(threading.current_thread(), bstack11ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨሗ"), None)
    @staticmethod
    def bstack11llll1ll1_opy_(driver):
        return {
            bstack1l1ll11lll_opy_(): bstack1ll1111l11_opy_(driver)
        }
    @staticmethod
    def bstack11lll1llll_opy_(exception_info, report):
        return [{bstack11ll11_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨመ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1l1llllll1_opy_(typename):
        if bstack11ll11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤሙ") in typename:
            return bstack11ll11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣሚ")
        return bstack11ll11_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤማ")
    @staticmethod
    def bstack1l11111lll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1llll1111_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l111111ll_opy_(test, hook_name=None):
        bstack11llll11l1_opy_ = test.parent
        if hook_name in [bstack11ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧሜ"), bstack11ll11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫም"), bstack11ll11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪሞ"), bstack11ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧሟ")]:
            bstack11llll11l1_opy_ = test
        scope = []
        while bstack11llll11l1_opy_ is not None:
            scope.append(bstack11llll11l1_opy_.name)
            bstack11llll11l1_opy_ = bstack11llll11l1_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack11llll111l_opy_(hook_type):
        if hook_type == bstack11ll11_opy_ (u"ࠨࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠦሠ"):
            return bstack11ll11_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡨࡰࡱ࡮ࠦሡ")
        elif hook_type == bstack11ll11_opy_ (u"ࠣࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠧሢ"):
            return bstack11ll11_opy_ (u"ࠤࡗࡩࡦࡸࡤࡰࡹࡱࠤ࡭ࡵ࡯࡬ࠤሣ")
    @staticmethod
    def bstack11llll1l11_opy_(bstack1l1llll1l_opy_):
        try:
            if not bstack1llll1111_opy_.on():
                return bstack1l1llll1l_opy_
            if os.environ.get(bstack11ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠣሤ"), None) == bstack11ll11_opy_ (u"ࠦࡹࡸࡵࡦࠤሥ"):
                tests = os.environ.get(bstack11ll11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠤሦ"), None)
                if tests is None or tests == bstack11ll11_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦሧ"):
                    return bstack1l1llll1l_opy_
                bstack1l1llll1l_opy_ = tests.split(bstack11ll11_opy_ (u"ࠧ࠭ࠩረ"))
                return bstack1l1llll1l_opy_
        except Exception as exc:
            print(bstack11ll11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡳࡧࡵࡹࡳࠦࡨࡢࡰࡧࡰࡪࡸ࠺ࠡࠤሩ"), str(exc))
        return bstack1l1llll1l_opy_
    @classmethod
    def bstack11llllllll_opy_(cls, event: str, bstack1l1111ll11_opy_: bstack1l111ll11l_opy_):
        bstack11lll1lll1_opy_ = {
            bstack11ll11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ሪ"): event,
            bstack1l1111ll11_opy_.bstack1l111ll111_opy_(): bstack1l1111ll11_opy_.bstack1l111l1lll_opy_(event)
        }
        bstack1llll1111_opy_.bstack1l1111l1ll_opy_(bstack11lll1lll1_opy_)