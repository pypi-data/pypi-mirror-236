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
class bstack1l11l1ll1l_opy_:
    def __init__(self, handler):
        self._1l11l1ll11_opy_ = None
        self.handler = handler
        self._1l11l1l1l1_opy_ = self.bstack1l11l1lll1_opy_()
        self.patch()
    def patch(self):
        self._1l11l1ll11_opy_ = self._1l11l1l1l1_opy_.execute
        self._1l11l1l1l1_opy_.execute = self.bstack1l11l1llll_opy_()
    def bstack1l11l1llll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            response = self._1l11l1ll11_opy_(this, driver_command, *args, **kwargs)
            self.handler(driver_command, response)
            return response
        return execute
    def reset(self):
        self._1l11l1l1l1_opy_.execute = self._1l11l1ll11_opy_
    @staticmethod
    def bstack1l11l1lll1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver