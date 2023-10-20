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
import threading
bstack1l11ll1lll_opy_ = 1000
bstack1l11ll1l11_opy_ = 5
bstack1l11ll111l_opy_ = 30
bstack1l11lll1ll_opy_ = 2
class bstack1l11lll111_opy_:
    def __init__(self, handler, bstack1l11ll1ll1_opy_=bstack1l11ll1lll_opy_, bstack1l11ll11l1_opy_=bstack1l11ll1l11_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1l11ll1ll1_opy_ = bstack1l11ll1ll1_opy_
        self.bstack1l11ll11l1_opy_ = bstack1l11ll11l1_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack1l11ll1l1l_opy_()
    def bstack1l11ll1l1l_opy_(self):
        self.timer = threading.Timer(self.bstack1l11ll11l1_opy_, self.bstack1l11ll11ll_opy_)
        self.timer.start()
    def bstack1l11lll1l1_opy_(self):
        self.timer.cancel()
    def bstack1l11llll11_opy_(self):
        self.bstack1l11lll1l1_opy_()
        self.bstack1l11ll1l1l_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1l11ll1ll1_opy_:
                t = threading.Thread(target=self.bstack1l11ll11ll_opy_)
                t.start()
                self.bstack1l11llll11_opy_()
    def bstack1l11ll11ll_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack1l11ll1ll1_opy_]
        del self.queue[:self.bstack1l11ll1ll1_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack1l11lll1l1_opy_()
        while len(self.queue) > 0:
            self.bstack1l11ll11ll_opy_()