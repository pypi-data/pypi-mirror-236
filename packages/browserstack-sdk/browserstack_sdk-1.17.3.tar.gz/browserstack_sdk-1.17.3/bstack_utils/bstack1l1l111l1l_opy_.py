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
import re
def bstack1l1l1111ll_opy_(fixture_name):
    if fixture_name.startswith(bstack11l1l1_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩბ")):
        return bstack11l1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩგ")
    elif fixture_name.startswith(bstack11l1l1_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩდ")):
        return bstack11l1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩე")
    elif fixture_name.startswith(bstack11l1l1_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩვ")):
        return bstack11l1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩზ")
    elif fixture_name.startswith(bstack11l1l1_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫთ")):
        return bstack11l1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩი")
def bstack1l11llll1l_opy_(fixture_name):
    return bool(re.match(bstack11l1l1_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡽ࡯ࡲࡨࡺࡲࡥࠪࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭კ"), fixture_name))
def bstack1l1l1111l1_opy_(fixture_name):
    return bool(re.match(bstack11l1l1_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪლ"), fixture_name))
def bstack1l11lllll1_opy_(fixture_name):
    return bool(re.match(bstack11l1l1_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪმ"), fixture_name))
def bstack1l1l111l11_opy_(fixture_name):
    if fixture_name.startswith(bstack11l1l1_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ნ")):
        return bstack11l1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ო"), bstack11l1l1_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫპ")
    elif fixture_name.startswith(bstack11l1l1_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧჟ")):
        return bstack11l1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧრ"), bstack11l1l1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ს")
    elif fixture_name.startswith(bstack11l1l1_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨტ")):
        return bstack11l1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨუ"), bstack11l1l1_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩფ")
    elif fixture_name.startswith(bstack11l1l1_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩქ")):
        return bstack11l1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩღ"), bstack11l1l1_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫყ")
    return None, None
def bstack1l1l111ll1_opy_(hook_name):
    if hook_name in [bstack11l1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨშ"), bstack11l1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬჩ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1l11llll11_opy_(hook_name):
    if hook_name in [bstack11l1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬც"), bstack11l1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫძ")]:
        return bstack11l1l1_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫწ")
    elif hook_name in [bstack11l1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ჭ"), bstack11l1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ხ")]:
        return bstack11l1l1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ჯ")
    elif hook_name in [bstack11l1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧჰ"), bstack11l1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ჱ")]:
        return bstack11l1l1_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩჲ")
    elif hook_name in [bstack11l1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨჳ"), bstack11l1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨჴ")]:
        return bstack11l1l1_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫჵ")
    return hook_name
def bstack1l1l111111_opy_(node, scenario):
    if hasattr(node, bstack11l1l1_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫჶ")):
        parts = node.nodeid.rsplit(bstack11l1l1_opy_ (u"ࠥ࡟ࠧჷ"))
        params = parts[-1]
        return bstack11l1l1_opy_ (u"ࠦࢀࢃࠠ࡜ࡽࢀࠦჸ").format(scenario.name, params)
    return scenario.name
def bstack1l11llllll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11l1l1_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧჹ")):
            examples = list(node.callspec.params[bstack11l1l1_opy_ (u"࠭࡟ࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡪࡾࡡ࡮ࡲ࡯ࡩࠬჺ")].values())
        return examples
    except:
        return []
def bstack1l1l11111l_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)