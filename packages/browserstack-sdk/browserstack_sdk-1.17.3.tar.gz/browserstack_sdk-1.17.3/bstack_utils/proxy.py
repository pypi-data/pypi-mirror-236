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
import os
from urllib.parse import urlparse
from bstack_utils.messages import bstack1l1l1l11l1_opy_
def bstack1l1l11l1l1_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1l1l11l1ll_opy_(bstack1l1l11ll11_opy_, bstack1l1l11l111_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1l1l11ll11_opy_):
        with open(bstack1l1l11ll11_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1l1l11l1l1_opy_(bstack1l1l11ll11_opy_):
        pac = get_pac(url=bstack1l1l11ll11_opy_)
    else:
        raise Exception(bstack11l1l1_opy_ (u"ࠬࡖࡡࡤࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠬႬ").format(bstack1l1l11ll11_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11l1l1_opy_ (u"ࠨ࠸࠯࠺࠱࠼࠳࠾ࠢႭ"), 80))
        bstack1l1l111lll_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1l1l111lll_opy_ = bstack11l1l1_opy_ (u"ࠧ࠱࠰࠳࠲࠵࠴࠰ࠨႮ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1l1l11l111_opy_, bstack1l1l111lll_opy_)
    return proxy_url
def bstack1l111l1l_opy_(config):
    return bstack11l1l1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫႯ") in config or bstack11l1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭Ⴐ") in config
def bstack1ll1l111l_opy_(config):
    if not bstack1l111l1l_opy_(config):
        return
    if config.get(bstack11l1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭Ⴑ")):
        return config.get(bstack11l1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧႲ"))
    if config.get(bstack11l1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩႳ")):
        return config.get(bstack11l1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪႴ"))
def bstack1111l1ll1_opy_(config, bstack1l1l11l111_opy_):
    proxy = bstack1ll1l111l_opy_(config)
    proxies = {}
    if config.get(bstack11l1l1_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪႵ")) or config.get(bstack11l1l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬႶ")):
        if proxy.endswith(bstack11l1l1_opy_ (u"ࠩ࠱ࡴࡦࡩࠧႷ")):
            proxies = bstack1l111lll_opy_(proxy, bstack1l1l11l111_opy_)
        else:
            proxies = {
                bstack11l1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩႸ"): proxy
            }
    return proxies
def bstack1l111lll_opy_(bstack1l1l11ll11_opy_, bstack1l1l11l111_opy_):
    proxies = {}
    global bstack1l1l11l11l_opy_
    if bstack11l1l1_opy_ (u"ࠫࡕࡇࡃࡠࡒࡕࡓ࡝࡟ࠧႹ") in globals():
        return bstack1l1l11l11l_opy_
    try:
        proxy = bstack1l1l11l1ll_opy_(bstack1l1l11ll11_opy_, bstack1l1l11l111_opy_)
        if bstack11l1l1_opy_ (u"ࠧࡊࡉࡓࡇࡆࡘࠧႺ") in proxy:
            proxies = {}
        elif bstack11l1l1_opy_ (u"ࠨࡈࡕࡖࡓࠦႻ") in proxy or bstack11l1l1_opy_ (u"ࠢࡉࡖࡗࡔࡘࠨႼ") in proxy or bstack11l1l1_opy_ (u"ࠣࡕࡒࡇࡐ࡙ࠢႽ") in proxy:
            bstack1l1l11ll1l_opy_ = proxy.split(bstack11l1l1_opy_ (u"ࠤࠣࠦႾ"))
            if bstack11l1l1_opy_ (u"ࠥ࠾࠴࠵ࠢႿ") in bstack11l1l1_opy_ (u"ࠦࠧჀ").join(bstack1l1l11ll1l_opy_[1:]):
                proxies = {
                    bstack11l1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫჁ"): bstack11l1l1_opy_ (u"ࠨࠢჂ").join(bstack1l1l11ll1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭Ⴣ"): str(bstack1l1l11ll1l_opy_[0]).lower() + bstack11l1l1_opy_ (u"ࠣ࠼࠲࠳ࠧჄ") + bstack11l1l1_opy_ (u"ࠤࠥჅ").join(bstack1l1l11ll1l_opy_[1:])
                }
        elif bstack11l1l1_opy_ (u"ࠥࡔࡗࡕࡘ࡚ࠤ჆") in proxy:
            bstack1l1l11ll1l_opy_ = proxy.split(bstack11l1l1_opy_ (u"ࠦࠥࠨჇ"))
            if bstack11l1l1_opy_ (u"ࠧࡀ࠯࠰ࠤ჈") in bstack11l1l1_opy_ (u"ࠨࠢ჉").join(bstack1l1l11ll1l_opy_[1:]):
                proxies = {
                    bstack11l1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭჊"): bstack11l1l1_opy_ (u"ࠣࠤ჋").join(bstack1l1l11ll1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨ჌"): bstack11l1l1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦჍ") + bstack11l1l1_opy_ (u"ࠦࠧ჎").join(bstack1l1l11ll1l_opy_[1:])
                }
        else:
            proxies = {
                bstack11l1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ჏"): proxy
            }
    except Exception as e:
        print(bstack11l1l1_opy_ (u"ࠨࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥა"), bstack1l1l1l11l1_opy_.format(bstack1l1l11ll11_opy_, str(e)))
    bstack1l1l11l11l_opy_ = proxies
    return proxies