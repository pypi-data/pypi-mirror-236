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
import json
import os
from bstack_utils.helper import bstack1l1ll1ll11_opy_, bstack1lll1lll_opy_, bstack1ll1l1llll_opy_, \
    bstack1l1lll1l11_opy_
def bstack111ll11ll_opy_(bstack1l11l11lll_opy_):
    for driver in bstack1l11l11lll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l1ll11ll_opy_(type, name, status, reason, bstack1l11ll11_opy_, bstack1l1l1l11_opy_):
    bstack1ll11l11_opy_ = {
        bstack11ll11_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧᄉ"): type,
        bstack11ll11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᄊ"): {}
    }
    if type == bstack11ll11_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫᄋ"):
        bstack1ll11l11_opy_[bstack11ll11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᄌ")][bstack11ll11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᄍ")] = bstack1l11ll11_opy_
        bstack1ll11l11_opy_[bstack11ll11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᄎ")][bstack11ll11_opy_ (u"࠭ࡤࡢࡶࡤࠫᄏ")] = json.dumps(str(bstack1l1l1l11_opy_))
    if type == bstack11ll11_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᄐ"):
        bstack1ll11l11_opy_[bstack11ll11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᄑ")][bstack11ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᄒ")] = name
    if type == bstack11ll11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᄓ"):
        bstack1ll11l11_opy_[bstack11ll11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᄔ")][bstack11ll11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᄕ")] = status
        if status == bstack11ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᄖ") and str(reason) != bstack11ll11_opy_ (u"ࠢࠣᄗ"):
            bstack1ll11l11_opy_[bstack11ll11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᄘ")][bstack11ll11_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᄙ")] = json.dumps(str(reason))
    bstack1l111ll1l_opy_ = bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨᄚ").format(json.dumps(bstack1ll11l11_opy_))
    return bstack1l111ll1l_opy_
def bstack1lll1l11_opy_(url, config, logger, bstack1l11l1l11_opy_=False):
    hostname = bstack1lll1lll_opy_(url)
    is_private = bstack1ll1l1llll_opy_(hostname)
    try:
        if is_private or bstack1l11l1l11_opy_:
            file_path = bstack1l1ll1ll11_opy_(bstack11ll11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᄛ"), bstack11ll11_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᄜ"), logger)
            if os.environ.get(bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᄝ")) and eval(
                    os.environ.get(bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᄞ"))):
                return
            if (bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᄟ") in config and not config[bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᄠ")]):
                os.environ[bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᄡ")] = str(True)
                bstack1l11l1l111_opy_ = {bstack11ll11_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ᄢ"): hostname}
                bstack1l1lll1l11_opy_(bstack11ll11_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᄣ"), bstack11ll11_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫᄤ"), bstack1l11l1l111_opy_, logger)
    except Exception as e:
        pass
def bstack1llll1lll1_opy_(caps, bstack1l11l1l1l1_opy_):
    if bstack11ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᄥ") in caps:
        caps[bstack11ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᄦ")][bstack11ll11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨᄧ")] = True
        if bstack1l11l1l1l1_opy_:
            caps[bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᄨ")][bstack11ll11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᄩ")] = bstack1l11l1l1l1_opy_
    else:
        caps[bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪᄪ")] = True
        if bstack1l11l1l1l1_opy_:
            caps[bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᄫ")] = bstack1l11l1l1l1_opy_