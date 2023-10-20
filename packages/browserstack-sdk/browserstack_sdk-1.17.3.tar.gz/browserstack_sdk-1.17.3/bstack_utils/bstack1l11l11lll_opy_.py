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
import json
import os
from bstack_utils.helper import bstack1ll111l111_opy_, bstack1ll11111_opy_, bstack1l1l1lll1_opy_, \
    bstack1l1lllll11_opy_
def bstack1l111lll1_opy_(bstack1l11l1l111_opy_):
    for driver in bstack1l11l1l111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l1ll1l11_opy_(type, name, status, reason, bstack1lll11ll1l_opy_, bstack111ll1l11_opy_):
    bstack11111111l_opy_ = {
        bstack11l1l1_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧ჻"): type,
        bstack11l1l1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫჼ"): {}
    }
    if type == bstack11l1l1_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫჽ"):
        bstack11111111l_opy_[bstack11l1l1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ჾ")][bstack11l1l1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪჿ")] = bstack1lll11ll1l_opy_
        bstack11111111l_opy_[bstack11l1l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᄀ")][bstack11l1l1_opy_ (u"࠭ࡤࡢࡶࡤࠫᄁ")] = json.dumps(str(bstack111ll1l11_opy_))
    if type == bstack11l1l1_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᄂ"):
        bstack11111111l_opy_[bstack11l1l1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᄃ")][bstack11l1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᄄ")] = name
    if type == bstack11l1l1_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᄅ"):
        bstack11111111l_opy_[bstack11l1l1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᄆ")][bstack11l1l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᄇ")] = status
        if status == bstack11l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᄈ") and str(reason) != bstack11l1l1_opy_ (u"ࠢࠣᄉ"):
            bstack11111111l_opy_[bstack11l1l1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᄊ")][bstack11l1l1_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᄋ")] = json.dumps(str(reason))
    bstack1lllllll11_opy_ = bstack11l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨᄌ").format(json.dumps(bstack11111111l_opy_))
    return bstack1lllllll11_opy_
def bstack11lll111l_opy_(url, config, logger, bstack1lll111l1_opy_=False):
    hostname = bstack1ll11111_opy_(url)
    is_private = bstack1l1l1lll1_opy_(hostname)
    try:
        if is_private or bstack1lll111l1_opy_:
            file_path = bstack1ll111l111_opy_(bstack11l1l1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᄍ"), bstack11l1l1_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᄎ"), logger)
            if os.environ.get(bstack11l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᄏ")) and eval(
                    os.environ.get(bstack11l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᄐ"))):
                return
            if (bstack11l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᄑ") in config and not config[bstack11l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᄒ")]):
                os.environ[bstack11l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᄓ")] = str(True)
                bstack1l11l1l11l_opy_ = {bstack11l1l1_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ᄔ"): hostname}
                bstack1l1lllll11_opy_(bstack11l1l1_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᄕ"), bstack11l1l1_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫᄖ"), bstack1l11l1l11l_opy_, logger)
    except Exception as e:
        pass
def bstack11ll1l1ll_opy_(caps, bstack1l11l11ll1_opy_):
    if bstack11l1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᄗ") in caps:
        caps[bstack11l1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᄘ")][bstack11l1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨᄙ")] = True
        if bstack1l11l11ll1_opy_:
            caps[bstack11l1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᄚ")][bstack11l1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᄛ")] = bstack1l11l11ll1_opy_
    else:
        caps[bstack11l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪᄜ")] = True
        if bstack1l11l11ll1_opy_:
            caps[bstack11l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᄝ")] = bstack1l11l11ll1_opy_