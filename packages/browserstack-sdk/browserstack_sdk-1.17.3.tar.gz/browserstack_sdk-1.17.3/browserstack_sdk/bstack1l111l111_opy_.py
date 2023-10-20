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
import multiprocessing
import os
from browserstack_sdk.bstack11l1l1l1l_opy_ import *
from bstack_utils.helper import bstack11lll1l11_opy_
from bstack_utils.messages import bstack111llllll_opy_
from bstack_utils.constants import bstack1l1111l11_opy_
class bstack111l1l1l1_opy_:
    def __init__(self, args, logger, bstack1ll1l11111_opy_, bstack1ll11l1lll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1ll1l11111_opy_ = bstack1ll1l11111_opy_
        self.bstack1ll11l1lll_opy_ = bstack1ll11l1lll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1ll11l1l1_opy_ = []
        self.bstack1ll11lll11_opy_ = None
        self.bstack1lll11l1ll_opy_ = []
        self.bstack1ll11llll1_opy_ = self.bstack1ll1l1l1_opy_()
        self.bstack1ll1l11ll1_opy_ = -1
    def bstack1ll1l11ll_opy_(self, bstack1ll11ll111_opy_):
        self.parse_args()
        self.bstack1ll1l111l1_opy_()
        self.bstack1ll11lllll_opy_(bstack1ll11ll111_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    def bstack1ll11lll1l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1ll1l11ll1_opy_ = -1
        if bstack11l1l1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ಍") in self.bstack1ll1l11111_opy_:
            self.bstack1ll1l11ll1_opy_ = self.bstack1ll1l11111_opy_[bstack11l1l1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨಎ")]
        try:
            bstack1ll11ll1ll_opy_ = [bstack11l1l1_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫಏ"), bstack11l1l1_opy_ (u"ࠪ࠱࠲ࡶ࡬ࡶࡩ࡬ࡲࡸ࠭ಐ"), bstack11l1l1_opy_ (u"ࠫ࠲ࡶࠧ಑")]
            if self.bstack1ll1l11ll1_opy_ >= 0:
                bstack1ll11ll1ll_opy_.extend([bstack11l1l1_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ಒ"), bstack11l1l1_opy_ (u"࠭࠭࡯ࠩಓ")])
            for arg in bstack1ll11ll1ll_opy_:
                self.bstack1ll11lll1l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1ll1l111l1_opy_(self):
        bstack1ll11lll11_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1ll11lll11_opy_ = bstack1ll11lll11_opy_
        return bstack1ll11lll11_opy_
    def bstack11ll111l_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            import importlib
            bstack1ll11ll11l_opy_ = importlib.find_loader(bstack11l1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩಔ"))
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack111llllll_opy_)
    def bstack1ll11lllll_opy_(self, bstack1ll11ll111_opy_):
        if bstack1ll11ll111_opy_:
            self.bstack1ll11lll11_opy_.append(bstack11l1l1_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬಕ"))
            self.bstack1ll11lll11_opy_.append(bstack11l1l1_opy_ (u"ࠩࡗࡶࡺ࡫ࠧಖ"))
        self.bstack1ll11lll11_opy_.append(bstack11l1l1_opy_ (u"ࠪ࠱ࡵ࠭ಗ"))
        self.bstack1ll11lll11_opy_.append(bstack11l1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠩಘ"))
        self.bstack1ll11lll11_opy_.append(bstack11l1l1_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧಙ"))
        self.bstack1ll11lll11_opy_.append(bstack11l1l1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ಚ"))
        if self.bstack1ll1l11ll1_opy_ > 1:
            self.bstack1ll11lll11_opy_.append(bstack11l1l1_opy_ (u"ࠧ࠮ࡰࠪಛ"))
            self.bstack1ll11lll11_opy_.append(str(self.bstack1ll1l11ll1_opy_))
    def bstack1ll11ll1l1_opy_(self):
        bstack1lll11l1ll_opy_ = []
        for spec in self.bstack1ll11l1l1_opy_:
            bstack1l111l11l_opy_ = [spec]
            bstack1l111l11l_opy_ += self.bstack1ll11lll11_opy_
            bstack1lll11l1ll_opy_.append(bstack1l111l11l_opy_)
        self.bstack1lll11l1ll_opy_ = bstack1lll11l1ll_opy_
        return bstack1lll11l1ll_opy_
    def bstack1ll1l1l1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1ll11llll1_opy_ = True
            return True
        except Exception as e:
            self.bstack1ll11llll1_opy_ = False
        return self.bstack1ll11llll1_opy_
    def bstack1llll11l_opy_(self, bstack1ll1l1111l_opy_, bstack1ll1l11ll_opy_):
        bstack1ll1l11ll_opy_[bstack11l1l1_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨಜ")] = self.bstack1ll1l11111_opy_
        if bstack11l1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬಝ") in self.bstack1ll1l11111_opy_:
            bstack111lll1l_opy_ = []
            manager = multiprocessing.Manager()
            bstack111lll11l_opy_ = manager.list()
            for index, platform in enumerate(self.bstack1ll1l11111_opy_[bstack11l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ಞ")]):
                bstack111lll1l_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack1ll1l1111l_opy_,
                                                           args=(self.bstack1ll11lll11_opy_, bstack1ll1l11ll_opy_)))
            i = 0
            for t in bstack111lll1l_opy_:
                os.environ[bstack11l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫಟ")] = str(i)
                i += 1
                t.start()
            for t in bstack111lll1l_opy_:
                t.join()
            return bstack111lll11l_opy_