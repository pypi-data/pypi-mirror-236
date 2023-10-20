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
import os
from urllib.parse import urlparse
from bstack_utils.messages import bstack1l1l1l1l11_opy_
def bstack1l1l11l111_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1l1l11ll1l_opy_(bstack1l1l11l1ll_opy_, bstack1l1l11lll1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1l1l11l1ll_opy_):
        with open(bstack1l1l11l1ll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1l1l11l111_opy_(bstack1l1l11l1ll_opy_):
        pac = get_pac(url=bstack1l1l11l1ll_opy_)
    else:
        raise Exception(bstack11ll11_opy_ (u"ࠬࡖࡡࡤࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠬႺ").format(bstack1l1l11l1ll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11ll11_opy_ (u"ࠨ࠸࠯࠺࠱࠼࠳࠾ࠢႻ"), 80))
        bstack1l1l11l11l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1l1l11l11l_opy_ = bstack11ll11_opy_ (u"ࠧ࠱࠰࠳࠲࠵࠴࠰ࠨႼ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1l1l11lll1_opy_, bstack1l1l11l11l_opy_)
    return proxy_url
def bstack1l1llll11_opy_(config):
    return bstack11ll11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫႽ") in config or bstack11ll11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭Ⴞ") in config
def bstack111l11111_opy_(config):
    if not bstack1l1llll11_opy_(config):
        return
    if config.get(bstack11ll11_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭Ⴟ")):
        return config.get(bstack11ll11_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧჀ"))
    if config.get(bstack11ll11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩჁ")):
        return config.get(bstack11ll11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪჂ"))
def bstack11ll1l111_opy_(config, bstack1l1l11lll1_opy_):
    proxy = bstack111l11111_opy_(config)
    proxies = {}
    if config.get(bstack11ll11_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪჃ")) or config.get(bstack11ll11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬჄ")):
        if proxy.endswith(bstack11ll11_opy_ (u"ࠩ࠱ࡴࡦࡩࠧჅ")):
            proxies = bstack1ll1lll1ll_opy_(proxy, bstack1l1l11lll1_opy_)
        else:
            proxies = {
                bstack11ll11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩ჆"): proxy
            }
    return proxies
def bstack1ll1lll1ll_opy_(bstack1l1l11l1ll_opy_, bstack1l1l11lll1_opy_):
    proxies = {}
    global bstack1l1l11ll11_opy_
    if bstack11ll11_opy_ (u"ࠫࡕࡇࡃࡠࡒࡕࡓ࡝࡟ࠧჇ") in globals():
        return bstack1l1l11ll11_opy_
    try:
        proxy = bstack1l1l11ll1l_opy_(bstack1l1l11l1ll_opy_, bstack1l1l11lll1_opy_)
        if bstack11ll11_opy_ (u"ࠧࡊࡉࡓࡇࡆࡘࠧ჈") in proxy:
            proxies = {}
        elif bstack11ll11_opy_ (u"ࠨࡈࡕࡖࡓࠦ჉") in proxy or bstack11ll11_opy_ (u"ࠢࡉࡖࡗࡔࡘࠨ჊") in proxy or bstack11ll11_opy_ (u"ࠣࡕࡒࡇࡐ࡙ࠢ჋") in proxy:
            bstack1l1l11l1l1_opy_ = proxy.split(bstack11ll11_opy_ (u"ࠤࠣࠦ჌"))
            if bstack11ll11_opy_ (u"ࠥ࠾࠴࠵ࠢჍ") in bstack11ll11_opy_ (u"ࠦࠧ჎").join(bstack1l1l11l1l1_opy_[1:]):
                proxies = {
                    bstack11ll11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ჏"): bstack11ll11_opy_ (u"ࠨࠢა").join(bstack1l1l11l1l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack11ll11_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ბ"): str(bstack1l1l11l1l1_opy_[0]).lower() + bstack11ll11_opy_ (u"ࠣ࠼࠲࠳ࠧგ") + bstack11ll11_opy_ (u"ࠤࠥდ").join(bstack1l1l11l1l1_opy_[1:])
                }
        elif bstack11ll11_opy_ (u"ࠥࡔࡗࡕࡘ࡚ࠤე") in proxy:
            bstack1l1l11l1l1_opy_ = proxy.split(bstack11ll11_opy_ (u"ࠦࠥࠨვ"))
            if bstack11ll11_opy_ (u"ࠧࡀ࠯࠰ࠤზ") in bstack11ll11_opy_ (u"ࠨࠢთ").join(bstack1l1l11l1l1_opy_[1:]):
                proxies = {
                    bstack11ll11_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ი"): bstack11ll11_opy_ (u"ࠣࠤკ").join(bstack1l1l11l1l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack11ll11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨლ"): bstack11ll11_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦმ") + bstack11ll11_opy_ (u"ࠦࠧნ").join(bstack1l1l11l1l1_opy_[1:])
                }
        else:
            proxies = {
                bstack11ll11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫო"): proxy
            }
    except Exception as e:
        print(bstack11ll11_opy_ (u"ࠨࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥპ"), bstack1l1l1l1l11_opy_.format(bstack1l1l11l1ll_opy_, str(e)))
    bstack1l1l11ll11_opy_ = proxies
    return proxies