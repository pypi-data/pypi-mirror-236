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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result
def _1l1ll11111_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1l1l1ll1l1_opy_:
    def __init__(self, handler):
        self._1l1ll111l1_opy_ = {}
        self._1l1l1lllll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        self._1l1ll111l1_opy_[bstack11ll11_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪၓ")] = Module._inject_setup_function_fixture
        self._1l1ll111l1_opy_[bstack11ll11_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩၔ")] = Module._inject_setup_module_fixture
        self._1l1ll111l1_opy_[bstack11ll11_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩၕ")] = Class._inject_setup_class_fixture
        self._1l1ll111l1_opy_[bstack11ll11_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫၖ")] = Class._inject_setup_method_fixture
        Module._inject_setup_function_fixture = self.bstack1l1l1l1lll_opy_(bstack11ll11_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧၗ"))
        Module._inject_setup_module_fixture = self.bstack1l1l1l1lll_opy_(bstack11ll11_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ၘ"))
        Class._inject_setup_class_fixture = self.bstack1l1l1l1lll_opy_(bstack11ll11_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ၙ"))
        Class._inject_setup_method_fixture = self.bstack1l1l1l1lll_opy_(bstack11ll11_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨၚ"))
    def bstack1l1ll111ll_opy_(self, bstack1l1l1ll11l_opy_, hook_type):
        meth = getattr(bstack1l1l1ll11l_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1l1l1lllll_opy_[hook_type] = meth
            setattr(bstack1l1l1ll11l_opy_, hook_type, self.bstack1l1l1lll1l_opy_(hook_type))
    def bstack1l1l1lll11_opy_(self, instance, bstack1l1l1ll1ll_opy_):
        if bstack1l1l1ll1ll_opy_ == bstack11ll11_opy_ (u"ࠣࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠦၛ"):
            self.bstack1l1ll111ll_opy_(instance.obj, bstack11ll11_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥၜ"))
            self.bstack1l1ll111ll_opy_(instance.obj, bstack11ll11_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠢၝ"))
        if bstack1l1l1ll1ll_opy_ == bstack11ll11_opy_ (u"ࠦࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠧၞ"):
            self.bstack1l1ll111ll_opy_(instance.obj, bstack11ll11_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠦၟ"))
            self.bstack1l1ll111ll_opy_(instance.obj, bstack11ll11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠣၠ"))
        if bstack1l1l1ll1ll_opy_ == bstack11ll11_opy_ (u"ࠢࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠢၡ"):
            self.bstack1l1ll111ll_opy_(instance.obj, bstack11ll11_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸࠨၢ"))
            self.bstack1l1ll111ll_opy_(instance.obj, bstack11ll11_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠥၣ"))
        if bstack1l1l1ll1ll_opy_ == bstack11ll11_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠦၤ"):
            self.bstack1l1ll111ll_opy_(instance.obj, bstack11ll11_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠥၥ"))
            self.bstack1l1ll111ll_opy_(instance.obj, bstack11ll11_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠢၦ"))
    @staticmethod
    def bstack1l1l1ll111_opy_(hook_type, func, args):
        if hook_type in [bstack11ll11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬၧ"), bstack11ll11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩၨ")]:
            _1l1ll11111_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1l1l1lll1l_opy_(self, hook_type):
        def bstack1l1l1l1l1l_opy_(arg=None):
            self.handler(hook_type, bstack11ll11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨၩ"))
            result = None
            exception = None
            try:
                self.bstack1l1l1ll111_opy_(hook_type, self._1l1l1lllll_opy_[hook_type], (arg,))
                result = Result(result=bstack11ll11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩၪ"))
            except Exception as e:
                result = Result(result=bstack11ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪၫ"), exception=e)
                self.handler(hook_type, bstack11ll11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪၬ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11ll11_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫၭ"), result)
        def bstack1l1ll1111l_opy_(this, arg=None):
            self.handler(hook_type, bstack11ll11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ၮ"))
            result = None
            exception = None
            try:
                self.bstack1l1l1ll111_opy_(hook_type, self._1l1l1lllll_opy_[hook_type], (this, arg))
                result = Result(result=bstack11ll11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧၯ"))
            except Exception as e:
                result = Result(result=bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨၰ"), exception=e)
                self.handler(hook_type, bstack11ll11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨၱ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11ll11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩၲ"), result)
        if hook_type in [bstack11ll11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪၳ"), bstack11ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧၴ")]:
            return bstack1l1ll1111l_opy_
        return bstack1l1l1l1l1l_opy_
    def bstack1l1l1l1lll_opy_(self, bstack1l1l1ll1ll_opy_):
        def bstack1l1l1l1ll1_opy_(this, *args, **kwargs):
            self.bstack1l1l1lll11_opy_(this, bstack1l1l1ll1ll_opy_)
            self._1l1ll111l1_opy_[bstack1l1l1ll1ll_opy_](this, *args, **kwargs)
        return bstack1l1l1l1ll1_opy_