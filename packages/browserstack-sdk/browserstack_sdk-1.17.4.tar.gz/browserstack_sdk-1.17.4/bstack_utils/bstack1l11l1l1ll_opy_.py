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
class bstack1l11l1ll11_opy_:
    def __init__(self, handler):
        self._1l11ll1111_opy_ = None
        self.handler = handler
        self._1l11l1ll1l_opy_ = self.bstack1l11l1llll_opy_()
        self.patch()
    def patch(self):
        self._1l11ll1111_opy_ = self._1l11l1ll1l_opy_.execute
        self._1l11l1ll1l_opy_.execute = self.bstack1l11l1lll1_opy_()
    def bstack1l11l1lll1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            response = self._1l11ll1111_opy_(this, driver_command, *args, **kwargs)
            self.handler(driver_command, response)
            return response
        return execute
    def reset(self):
        self._1l11l1ll1l_opy_.execute = self._1l11ll1111_opy_
    @staticmethod
    def bstack1l11l1llll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver