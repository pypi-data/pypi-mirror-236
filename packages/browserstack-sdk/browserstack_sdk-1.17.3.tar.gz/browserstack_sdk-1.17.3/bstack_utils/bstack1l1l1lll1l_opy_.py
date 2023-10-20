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
class bstack1l1ll111l1_opy_:
    def __init__(self, handler):
        self._1l1l1ll11l_opy_ = {}
        self._1l1l1ll1ll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        self._1l1l1ll11l_opy_[bstack11l1l1_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ၅")] = Module._inject_setup_function_fixture
        self._1l1l1ll11l_opy_[bstack11l1l1_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ၆")] = Module._inject_setup_module_fixture
        self._1l1l1ll11l_opy_[bstack11l1l1_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ၇")] = Class._inject_setup_class_fixture
        self._1l1l1ll11l_opy_[bstack11l1l1_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ၈")] = Class._inject_setup_method_fixture
        Module._inject_setup_function_fixture = self.bstack1l1l1llll1_opy_(bstack11l1l1_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ၉"))
        Module._inject_setup_module_fixture = self.bstack1l1l1llll1_opy_(bstack11l1l1_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭၊"))
        Class._inject_setup_class_fixture = self.bstack1l1l1llll1_opy_(bstack11l1l1_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭။"))
        Class._inject_setup_method_fixture = self.bstack1l1l1llll1_opy_(bstack11l1l1_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ၌"))
    def bstack1l1l1l1ll1_opy_(self, bstack1l1l1ll1l1_opy_, hook_type):
        meth = getattr(bstack1l1l1ll1l1_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1l1l1ll1ll_opy_[hook_type] = meth
            setattr(bstack1l1l1ll1l1_opy_, hook_type, self.bstack1l1l1l1l11_opy_(hook_type))
    def bstack1l1l1ll111_opy_(self, instance, bstack1l1ll1111l_opy_):
        if bstack1l1ll1111l_opy_ == bstack11l1l1_opy_ (u"ࠣࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠦ၍"):
            self.bstack1l1l1l1ll1_opy_(instance.obj, bstack11l1l1_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥ၎"))
            self.bstack1l1l1l1ll1_opy_(instance.obj, bstack11l1l1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠢ၏"))
        if bstack1l1ll1111l_opy_ == bstack11l1l1_opy_ (u"ࠦࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠧၐ"):
            self.bstack1l1l1l1ll1_opy_(instance.obj, bstack11l1l1_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠦၑ"))
            self.bstack1l1l1l1ll1_opy_(instance.obj, bstack11l1l1_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠣၒ"))
        if bstack1l1ll1111l_opy_ == bstack11l1l1_opy_ (u"ࠢࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠢၓ"):
            self.bstack1l1l1l1ll1_opy_(instance.obj, bstack11l1l1_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸࠨၔ"))
            self.bstack1l1l1l1ll1_opy_(instance.obj, bstack11l1l1_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠥၕ"))
        if bstack1l1ll1111l_opy_ == bstack11l1l1_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠦၖ"):
            self.bstack1l1l1l1ll1_opy_(instance.obj, bstack11l1l1_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠥၗ"))
            self.bstack1l1l1l1ll1_opy_(instance.obj, bstack11l1l1_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠢၘ"))
    @staticmethod
    def bstack1l1l1l1lll_opy_(hook_type, func, args):
        if hook_type in [bstack11l1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬၙ"), bstack11l1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩၚ")]:
            _1l1ll11111_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1l1l1l1l11_opy_(self, hook_type):
        def bstack1l1l1lllll_opy_(arg=None):
            self.handler(hook_type, bstack11l1l1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨၛ"))
            result = None
            exception = None
            try:
                self.bstack1l1l1l1lll_opy_(hook_type, self._1l1l1ll1ll_opy_[hook_type], (arg,))
                result = Result(result=bstack11l1l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩၜ"))
            except Exception as e:
                result = Result(result=bstack11l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪၝ"), exception=e)
                self.handler(hook_type, bstack11l1l1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪၞ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l1l1_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫၟ"), result)
        def bstack1l1l1lll11_opy_(this, arg=None):
            self.handler(hook_type, bstack11l1l1_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ၠ"))
            result = None
            exception = None
            try:
                self.bstack1l1l1l1lll_opy_(hook_type, self._1l1l1ll1ll_opy_[hook_type], (this, arg))
                result = Result(result=bstack11l1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧၡ"))
            except Exception as e:
                result = Result(result=bstack11l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨၢ"), exception=e)
                self.handler(hook_type, bstack11l1l1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨၣ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l1l1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩၤ"), result)
        if hook_type in [bstack11l1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪၥ"), bstack11l1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧၦ")]:
            return bstack1l1l1lll11_opy_
        return bstack1l1l1lllll_opy_
    def bstack1l1l1llll1_opy_(self, bstack1l1ll1111l_opy_):
        def bstack1l1l1l1l1l_opy_(this, *args, **kwargs):
            self.bstack1l1l1ll111_opy_(this, bstack1l1ll1111l_opy_)
            self._1l1l1ll11l_opy_[bstack1l1ll1111l_opy_](this, *args, **kwargs)
        return bstack1l1l1l1l1l_opy_