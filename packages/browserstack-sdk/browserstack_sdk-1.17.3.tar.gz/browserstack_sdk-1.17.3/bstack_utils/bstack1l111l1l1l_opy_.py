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
from uuid import uuid4
from bstack_utils.helper import bstack1l11lll11_opy_, bstack1ll111111l_opy_
from bstack_utils.bstack1l1l111l1l_opy_ import bstack1l11llllll_opy_
class bstack1l111ll1ll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack1l111l1111_opy_=None, framework=None, tags=[], scope=[], bstack1l111ll11l_opy_=None, bstack1l11l111ll_opy_=True, bstack1l1111llll_opy_=None, bstack11l1llll1_opy_=None, result=None, duration=None, meta={}):
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1l11l111ll_opy_:
            self.uuid = uuid4().__str__()
        self.bstack1l111l1111_opy_ = bstack1l111l1111_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1l111ll11l_opy_ = bstack1l111ll11l_opy_
        self.bstack1l1111llll_opy_ = bstack1l1111llll_opy_
        self.bstack11l1llll1_opy_ = bstack11l1llll1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack1l11l111l1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1l111l11ll_opy_(self):
        bstack1l111lllll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11l1l1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪᄞ"): bstack1l111lllll_opy_,
            bstack11l1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪᄟ"): bstack1l111lllll_opy_,
            bstack11l1l1_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧᄠ"): bstack1l111lllll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11l1l1_opy_ (u"࡙ࠥࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡹࡲ࡫࡮ࡵ࠼ࠣࠦᄡ") + key)
            setattr(self, key, val)
    def bstack1l11l1111l_opy_(self):
        return {
            bstack11l1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᄢ"): self.name,
            bstack11l1l1_opy_ (u"ࠬࡨ࡯ࡥࡻࠪᄣ"): {
                bstack11l1l1_opy_ (u"࠭࡬ࡢࡰࡪࠫᄤ"): bstack11l1l1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᄥ"),
                bstack11l1l1_opy_ (u"ࠨࡥࡲࡨࡪ࠭ᄦ"): self.code
            },
            bstack11l1l1_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩᄧ"): self.scope,
            bstack11l1l1_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᄨ"): self.tags,
            bstack11l1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᄩ"): self.framework,
            bstack11l1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᄪ"): self.bstack1l111l1111_opy_
        }
    def bstack1l111l1lll_opy_(self):
        return {
         bstack11l1l1_opy_ (u"࠭࡭ࡦࡶࡤࠫᄫ"): self.meta
        }
    def bstack1l11l11l11_opy_(self):
        return {
            bstack11l1l1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪᄬ"): {
                bstack11l1l1_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬᄭ"): self.bstack1l111ll11l_opy_
            }
        }
    def bstack1l111ll111_opy_(self, bstack1l1111lll1_opy_, details):
        step = next(filter(lambda st: st[bstack11l1l1_opy_ (u"ࠩ࡬ࡨࠬᄮ")] == bstack1l1111lll1_opy_, self.meta[bstack11l1l1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᄯ")]), None)
        step.update(details)
    def bstack1l111ll1l1_opy_(self, bstack1l1111lll1_opy_):
        step = next(filter(lambda st: st[bstack11l1l1_opy_ (u"ࠫ࡮ࡪࠧᄰ")] == bstack1l1111lll1_opy_, self.meta[bstack11l1l1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᄱ")]), None)
        step.update({
            bstack11l1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᄲ"): bstack1l11lll11_opy_()
        })
    def bstack1l11l11l1l_opy_(self, bstack1l1111lll1_opy_, result):
        bstack1l1111llll_opy_ = bstack1l11lll11_opy_()
        step = next(filter(lambda st: st[bstack11l1l1_opy_ (u"ࠧࡪࡦࠪᄳ")] == bstack1l1111lll1_opy_, self.meta[bstack11l1l1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᄴ")]), None)
        step.update({
            bstack11l1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᄵ"): bstack1l1111llll_opy_,
            bstack11l1l1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬᄶ"): bstack1ll111111l_opy_(step[bstack11l1l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᄷ")], bstack1l1111llll_opy_),
            bstack11l1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᄸ"): result.result,
            bstack11l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᄹ"): str(result.exception) if result.exception else None
        })
    def bstack1l111lll11_opy_(self):
        return {
            bstack11l1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᄺ"): self.bstack1l11l111l1_opy_(),
            **self.bstack1l11l1111l_opy_(),
            **self.bstack1l111l11ll_opy_(),
            **self.bstack1l111l1lll_opy_()
        }
    def bstack1l111l1ll1_opy_(self):
        data = {
            bstack11l1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᄻ"): self.bstack1l1111llll_opy_,
            bstack11l1l1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᄼ"): self.duration,
            bstack11l1l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᄽ"): self.result.result
        }
        if data[bstack11l1l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᄾ")] == bstack11l1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᄿ"):
            data[bstack11l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᅀ")] = self.result.bstack1ll11111ll_opy_()
            data[bstack11l1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᅁ")] = [{bstack11l1l1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᅂ"): self.result.bstack1l1ll1l1ll_opy_()}]
        return data
    def bstack1l111llll1_opy_(self):
        return {
            bstack11l1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᅃ"): self.bstack1l11l111l1_opy_(),
            **self.bstack1l11l1111l_opy_(),
            **self.bstack1l111l11ll_opy_(),
            **self.bstack1l111l1ll1_opy_(),
            **self.bstack1l111l1lll_opy_()
        }
    def bstack1l11l11111_opy_(self, event, result=None):
        if result:
            self.result = result
        if event == bstack11l1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᅄ"):
            return self.bstack1l111lll11_opy_()
        elif event == bstack11l1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᅅ"):
            return self.bstack1l111llll1_opy_()
    def bstack1l111l1l11_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l1111llll_opy_ = time if time else bstack1l11lll11_opy_()
        self.duration = duration if duration else bstack1ll111111l_opy_(self.bstack1l111l1111_opy_, self.bstack1l1111llll_opy_)
        if result:
            self.result = result
class bstack1l111l111l_opy_(bstack1l111ll1ll_opy_):
    def __init__(self, *args, hooks=[], **kwargs):
        self.hooks = hooks
        super().__init__(*args, **kwargs, bstack11l1llll1_opy_=bstack11l1l1_opy_ (u"ࠬࡺࡥࡴࡶࠪᅆ"))
    @classmethod
    def bstack1l111lll1l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11l1l1_opy_ (u"࠭ࡩࡥࠩᅇ"): id(step),
                bstack11l1l1_opy_ (u"ࠧࡵࡧࡻࡸࠬᅈ"): step.name,
                bstack11l1l1_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩᅉ"): step.keyword,
            })
        return bstack1l111l111l_opy_(
            **kwargs,
            meta={
                bstack11l1l1_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪᅊ"): {
                    bstack11l1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨᅋ"): feature.name,
                    bstack11l1l1_opy_ (u"ࠫࡵࡧࡴࡩࠩᅌ"): feature.filename,
                    bstack11l1l1_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᅍ"): feature.description
                },
                bstack11l1l1_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨᅎ"): {
                    bstack11l1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᅏ"): scenario.name
                },
                bstack11l1l1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᅐ"): steps,
                bstack11l1l1_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫᅑ"): bstack1l11llllll_opy_(test)
            }
        )
    def bstack1l111l11l1_opy_(self):
        return {
            bstack11l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᅒ"): self.hooks
        }
    def bstack1l111llll1_opy_(self):
        return {
            **super().bstack1l111llll1_opy_(),
            **self.bstack1l111l11l1_opy_()
        }
    def bstack1l111l1l11_opy_(self):
        return bstack11l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ᅓ")