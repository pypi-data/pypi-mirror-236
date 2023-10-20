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
import re
def bstack1l1l1111ll_opy_(fixture_name):
    if fixture_name.startswith(bstack11ll11_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩჟ")):
        return bstack11ll11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩრ")
    elif fixture_name.startswith(bstack11ll11_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩს")):
        return bstack11ll11_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩტ")
    elif fixture_name.startswith(bstack11ll11_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩუ")):
        return bstack11ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩფ")
    elif fixture_name.startswith(bstack11ll11_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫქ")):
        return bstack11ll11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩღ")
def bstack1l1l1111l1_opy_(fixture_name):
    return bool(re.match(bstack11ll11_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡽ࡯ࡲࡨࡺࡲࡥࠪࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ყ"), fixture_name))
def bstack1l1l11111l_opy_(fixture_name):
    return bool(re.match(bstack11ll11_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪშ"), fixture_name))
def bstack1l1l111111_opy_(fixture_name):
    return bool(re.match(bstack11ll11_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪჩ"), fixture_name))
def bstack1l11llll1l_opy_(fixture_name):
    if fixture_name.startswith(bstack11ll11_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ც")):
        return bstack11ll11_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ძ"), bstack11ll11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫწ")
    elif fixture_name.startswith(bstack11ll11_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧჭ")):
        return bstack11ll11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧხ"), bstack11ll11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ჯ")
    elif fixture_name.startswith(bstack11ll11_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨჰ")):
        return bstack11ll11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨჱ"), bstack11ll11_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩჲ")
    elif fixture_name.startswith(bstack11ll11_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩჳ")):
        return bstack11ll11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩჴ"), bstack11ll11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫჵ")
    return None, None
def bstack1l11lllll1_opy_(hook_name):
    if hook_name in [bstack11ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨჶ"), bstack11ll11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬჷ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1l1l111lll_opy_(hook_name):
    if hook_name in [bstack11ll11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬჸ"), bstack11ll11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫჹ")]:
        return bstack11ll11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫჺ")
    elif hook_name in [bstack11ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭჻"), bstack11ll11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ჼ")]:
        return bstack11ll11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ჽ")
    elif hook_name in [bstack11ll11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧჾ"), bstack11ll11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ჿ")]:
        return bstack11ll11_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩᄀ")
    elif hook_name in [bstack11ll11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨᄁ"), bstack11ll11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨᄂ")]:
        return bstack11ll11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫᄃ")
    return hook_name
def bstack1l1l111ll1_opy_(node, scenario):
    if hasattr(node, bstack11ll11_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫᄄ")):
        parts = node.nodeid.rsplit(bstack11ll11_opy_ (u"ࠥ࡟ࠧᄅ"))
        params = parts[-1]
        return bstack11ll11_opy_ (u"ࠦࢀࢃࠠ࡜ࡽࢀࠦᄆ").format(scenario.name, params)
    return scenario.name
def bstack1l11llllll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11ll11_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᄇ")):
            examples = list(node.callspec.params[bstack11ll11_opy_ (u"࠭࡟ࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡪࡾࡡ࡮ࡲ࡯ࡩࠬᄈ")].values())
        return examples
    except:
        return []
def bstack1l1l111l1l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)