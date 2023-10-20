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
conf = {
    bstack11ll11_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪದ"): False,
    bstack11ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ಧ"): True,
}
class Config(object):
    instance = None
    def __init__(self):
        self._1ll11l1111_opy_ = conf
    @classmethod
    def get_instance(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name):
        return self._1ll11l1111_opy_.get(property_name, None)
    def bstack11ll111ll_opy_(self, property_name, bstack1ll11l111l_opy_):
        self._1ll11l1111_opy_[property_name] = bstack1ll11l111l_opy_