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
import sys
class bstack1ll11l1ll1_opy_:
    def __init__(self, handler):
        self._1ll11l11l1_opy_ = sys.stdout.write
        self._1ll11l11ll_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack1ll11l1l11_opy_
        sys.stdout.error = self.bstack1ll11l1l1l_opy_
    def bstack1ll11l1l11_opy_(self, _str):
        self._1ll11l11l1_opy_(_str)
        if self.handler:
            self.handler({bstack11l1l1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫಠ"): bstack11l1l1_opy_ (u"࠭ࡉࡏࡈࡒࠫಡ"), bstack11l1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨಢ"): _str})
    def bstack1ll11l1l1l_opy_(self, _str):
        self._1ll11l11ll_opy_(_str)
        if self.handler:
            self.handler({bstack11l1l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧಣ"): bstack11l1l1_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨತ"), bstack11l1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫಥ"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._1ll11l11l1_opy_
        sys.stderr.write = self._1ll11l11ll_opy_