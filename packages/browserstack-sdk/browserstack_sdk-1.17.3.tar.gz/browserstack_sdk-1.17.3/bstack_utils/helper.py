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
import datetime
import json
import os
import re
import subprocess
import traceback
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import bstack1ll111lll1_opy_, bstack111ll1ll1_opy_, bstack11ll1ll1l_opy_, bstack1111111l_opy_
from bstack_utils.messages import bstack1111lll11_opy_
from bstack_utils.proxy import bstack1111l1ll1_opy_
bstack1lll1l11ll_opy_ = Config.get_instance()
def bstack1l1lll1lll_opy_(config):
    return config[bstack11l1l1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭໤")]
def bstack1l1lllllll_opy_(config):
    return config[bstack11l1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ໥")]
def bstack1ll1111111_opy_(obj):
    values = []
    bstack1l1ll1llll_opy_ = re.compile(bstack11l1l1_opy_ (u"ࡸࠢ࡟ࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤࡢࡤࠬࠦࠥ໦"), re.I)
    for key in obj.keys():
        if bstack1l1ll1llll_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1l1lllll1l_opy_(config):
    tags = []
    tags.extend(bstack1ll1111111_opy_(os.environ))
    tags.extend(bstack1ll1111111_opy_(config))
    return tags
def bstack1l1ll1l1l1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1l1ll11l11_opy_(bstack1ll1111l11_opy_):
    if not bstack1ll1111l11_opy_:
        return bstack11l1l1_opy_ (u"ࠧࠨ໧")
    return bstack11l1l1_opy_ (u"ࠣࡽࢀࠤ࠭ࢁࡽࠪࠤ໨").format(bstack1ll1111l11_opy_.name, bstack1ll1111l11_opy_.email)
def bstack1l1ll1lll1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1l1ll11lll_opy_ = repo.common_dir
        info = {
            bstack11l1l1_opy_ (u"ࠤࡶ࡬ࡦࠨ໩"): repo.head.commit.hexsha,
            bstack11l1l1_opy_ (u"ࠥࡷ࡭ࡵࡲࡵࡡࡶ࡬ࡦࠨ໪"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11l1l1_opy_ (u"ࠦࡧࡸࡡ࡯ࡥ࡫ࠦ໫"): repo.active_branch.name,
            bstack11l1l1_opy_ (u"ࠧࡺࡡࡨࠤ໬"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11l1l1_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࠤ໭"): bstack1l1ll11l11_opy_(repo.head.commit.committer),
            bstack11l1l1_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࡢࡨࡦࡺࡥࠣ໮"): repo.head.commit.committed_datetime.isoformat(),
            bstack11l1l1_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࠣ໯"): bstack1l1ll11l11_opy_(repo.head.commit.author),
            bstack11l1l1_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡡࡧࡥࡹ࡫ࠢ໰"): repo.head.commit.authored_datetime.isoformat(),
            bstack11l1l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦ໱"): repo.head.commit.message,
            bstack11l1l1_opy_ (u"ࠦࡷࡵ࡯ࡵࠤ໲"): repo.git.rev_parse(bstack11l1l1_opy_ (u"ࠧ࠳࠭ࡴࡪࡲࡻ࠲ࡺ࡯ࡱ࡮ࡨࡺࡪࡲࠢ໳")),
            bstack11l1l1_opy_ (u"ࠨࡣࡰ࡯ࡰࡳࡳࡥࡧࡪࡶࡢࡨ࡮ࡸࠢ໴"): bstack1l1ll11lll_opy_,
            bstack11l1l1_opy_ (u"ࠢࡸࡱࡵ࡯ࡹࡸࡥࡦࡡࡪ࡭ࡹࡥࡤࡪࡴࠥ໵"): subprocess.check_output([bstack11l1l1_opy_ (u"ࠣࡩ࡬ࡸࠧ໶"), bstack11l1l1_opy_ (u"ࠤࡵࡩࡻ࠳ࡰࡢࡴࡶࡩࠧ໷"), bstack11l1l1_opy_ (u"ࠥ࠱࠲࡭ࡩࡵ࠯ࡦࡳࡲࡳ࡯࡯࠯ࡧ࡭ࡷࠨ໸")]).strip().decode(
                bstack11l1l1_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ໹")),
            bstack11l1l1_opy_ (u"ࠧࡲࡡࡴࡶࡢࡸࡦ࡭ࠢ໺"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11l1l1_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡹ࡟ࡴ࡫ࡱࡧࡪࡥ࡬ࡢࡵࡷࡣࡹࡧࡧࠣ໻"): repo.git.rev_list(
                bstack11l1l1_opy_ (u"ࠢࡼࡿ࠱࠲ࢀࢃࠢ໼").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1l1lll1l11_opy_ = []
        for remote in remotes:
            bstack1l1ll1ll1l_opy_ = {
                bstack11l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨ໽"): remote.name,
                bstack11l1l1_opy_ (u"ࠤࡸࡶࡱࠨ໾"): remote.url,
            }
            bstack1l1lll1l11_opy_.append(bstack1l1ll1ll1l_opy_)
        return {
            bstack11l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣ໿"): bstack11l1l1_opy_ (u"ࠦ࡬࡯ࡴࠣༀ"),
            **info,
            bstack11l1l1_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩࡸࠨ༁"): bstack1l1lll1l11_opy_
        }
    except Exception as err:
        print(bstack11l1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡊ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤ༂").format(err))
        return {}
def bstack1lll1ll11_opy_():
    env = os.environ
    if (bstack11l1l1_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧ༃") in env and len(env[bstack11l1l1_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨ༄")]) > 0) or (
            bstack11l1l1_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣ༅") in env and len(env[bstack11l1l1_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤ༆")]) > 0):
        return {
            bstack11l1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ༇"): bstack11l1l1_opy_ (u"ࠧࡐࡥ࡯࡭࡬ࡲࡸࠨ༈"),
            bstack11l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ༉"): env.get(bstack11l1l1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ༊")),
            bstack11l1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ་"): env.get(bstack11l1l1_opy_ (u"ࠤࡍࡓࡇࡥࡎࡂࡏࡈࠦ༌")),
            bstack11l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ།"): env.get(bstack11l1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ༎"))
        }
    if env.get(bstack11l1l1_opy_ (u"ࠧࡉࡉࠣ༏")) == bstack11l1l1_opy_ (u"ࠨࡴࡳࡷࡨࠦ༐") and bstack1ll1111l1l_opy_(env.get(bstack11l1l1_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋࡃࡊࠤ༑"))):
        return {
            bstack11l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨ༒"): bstack11l1l1_opy_ (u"ࠤࡆ࡭ࡷࡩ࡬ࡦࡅࡌࠦ༓"),
            bstack11l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ༔"): env.get(bstack11l1l1_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ༕")),
            bstack11l1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ༖"): env.get(bstack11l1l1_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡊࡐࡄࠥ༗")),
            bstack11l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ༘"): env.get(bstack11l1l1_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐ༙ࠦ"))
        }
    if env.get(bstack11l1l1_opy_ (u"ࠤࡆࡍࠧ༚")) == bstack11l1l1_opy_ (u"ࠥࡸࡷࡻࡥࠣ༛") and bstack1ll1111l1l_opy_(env.get(bstack11l1l1_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࠦ༜"))):
        return {
            bstack11l1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ༝"): bstack11l1l1_opy_ (u"ࠨࡔࡳࡣࡹ࡭ࡸࠦࡃࡊࠤ༞"),
            bstack11l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ༟"): env.get(bstack11l1l1_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡘࡇࡅࡣ࡚ࡘࡌࠣ༠")),
            bstack11l1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ༡"): env.get(bstack11l1l1_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ༢")),
            bstack11l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ༣"): env.get(bstack11l1l1_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ༤"))
        }
    if env.get(bstack11l1l1_opy_ (u"ࠨࡃࡊࠤ༥")) == bstack11l1l1_opy_ (u"ࠢࡵࡴࡸࡩࠧ༦") and env.get(bstack11l1l1_opy_ (u"ࠣࡅࡌࡣࡓࡇࡍࡆࠤ༧")) == bstack11l1l1_opy_ (u"ࠤࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠦ༨"):
        return {
            bstack11l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣ༩"): bstack11l1l1_opy_ (u"ࠦࡈࡵࡤࡦࡵ࡫࡭ࡵࠨ༪"),
            bstack11l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ༫"): None,
            bstack11l1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ༬"): None,
            bstack11l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ༭"): None
        }
    if env.get(bstack11l1l1_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠦ༮")) and env.get(bstack11l1l1_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠧ༯")):
        return {
            bstack11l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣ༰"): bstack11l1l1_opy_ (u"ࠦࡇ࡯ࡴࡣࡷࡦ࡯ࡪࡺࠢ༱"),
            bstack11l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ༲"): env.get(bstack11l1l1_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡊࡍ࡙ࡥࡈࡕࡖࡓࡣࡔࡘࡉࡈࡋࡑࠦ༳")),
            bstack11l1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ༴"): None,
            bstack11l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸ༵ࠢ"): env.get(bstack11l1l1_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ༶"))
        }
    if env.get(bstack11l1l1_opy_ (u"ࠥࡇࡎࠨ༷")) == bstack11l1l1_opy_ (u"ࠦࡹࡸࡵࡦࠤ༸") and bstack1ll1111l1l_opy_(env.get(bstack11l1l1_opy_ (u"ࠧࡊࡒࡐࡐࡈ༹ࠦ"))):
        return {
            bstack11l1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ༺"): bstack11l1l1_opy_ (u"ࠢࡅࡴࡲࡲࡪࠨ༻"),
            bstack11l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ༼"): env.get(bstack11l1l1_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡍࡋࡑࡏࠧ༽")),
            bstack11l1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ༾"): None,
            bstack11l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ༿"): env.get(bstack11l1l1_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥཀ"))
        }
    if env.get(bstack11l1l1_opy_ (u"ࠨࡃࡊࠤཁ")) == bstack11l1l1_opy_ (u"ࠢࡵࡴࡸࡩࠧག") and bstack1ll1111l1l_opy_(env.get(bstack11l1l1_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࠦགྷ"))):
        return {
            bstack11l1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢང"): bstack11l1l1_opy_ (u"ࠥࡗࡪࡳࡡࡱࡪࡲࡶࡪࠨཅ"),
            bstack11l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢཆ"): env.get(bstack11l1l1_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡑࡕࡋࡆࡔࡉ࡛ࡃࡗࡍࡔࡔ࡟ࡖࡔࡏࠦཇ")),
            bstack11l1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ཈"): env.get(bstack11l1l1_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧཉ")),
            bstack11l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢཊ"): env.get(bstack11l1l1_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠧཋ"))
        }
    if env.get(bstack11l1l1_opy_ (u"ࠥࡇࡎࠨཌ")) == bstack11l1l1_opy_ (u"ࠦࡹࡸࡵࡦࠤཌྷ") and bstack1ll1111l1l_opy_(env.get(bstack11l1l1_opy_ (u"ࠧࡍࡉࡕࡎࡄࡆࡤࡉࡉࠣཎ"))):
        return {
            bstack11l1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦཏ"): bstack11l1l1_opy_ (u"ࠢࡈ࡫ࡷࡐࡦࡨࠢཐ"),
            bstack11l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦད"): env.get(bstack11l1l1_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡘࡖࡑࠨདྷ")),
            bstack11l1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧན"): env.get(bstack11l1l1_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤཔ")),
            bstack11l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦཕ"): env.get(bstack11l1l1_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡉࡅࠤབ"))
        }
    if env.get(bstack11l1l1_opy_ (u"ࠢࡄࡋࠥབྷ")) == bstack11l1l1_opy_ (u"ࠣࡶࡵࡹࡪࠨམ") and bstack1ll1111l1l_opy_(env.get(bstack11l1l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠧཙ"))):
        return {
            bstack11l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣཚ"): bstack11l1l1_opy_ (u"ࠦࡇࡻࡩ࡭ࡦ࡮࡭ࡹ࡫ࠢཛ"),
            bstack11l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣཛྷ"): env.get(bstack11l1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧཝ")),
            bstack11l1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤཞ"): env.get(bstack11l1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡑࡇࡂࡆࡎࠥཟ")) or env.get(bstack11l1l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧའ")),
            bstack11l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤཡ"): env.get(bstack11l1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨར"))
        }
    if bstack1ll1111l1l_opy_(env.get(bstack11l1l1_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢལ"))):
        return {
            bstack11l1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦཤ"): bstack11l1l1_opy_ (u"ࠢࡗ࡫ࡶࡹࡦࡲࠠࡔࡶࡸࡨ࡮ࡵࠠࡕࡧࡤࡱ࡙ࠥࡥࡳࡸ࡬ࡧࡪࡹࠢཥ"),
            bstack11l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦས"): bstack1l1ll1ll11_opy_ (u"ࠤࡾࡩࡳࡼ࠮ࡨࡧࡷ࡙࡙ࠬࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡉࡓ࡚ࡔࡄࡂࡖࡌࡓࡓ࡙ࡅࡓࡘࡈࡖ࡚ࡘࡉࠨࠫࢀࡿࡪࡴࡶ࠯ࡩࡨࡸ࠭࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡔࡗࡕࡊࡆࡅࡗࡍࡉ࠭ࠩࡾࠤཧ"),
            bstack11l1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧཨ"): env.get(bstack11l1l1_opy_ (u"ࠦࡘ࡟ࡓࡕࡇࡐࡣࡉࡋࡆࡊࡐࡌࡘࡎࡕࡎࡊࡆࠥཀྵ")),
            bstack11l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦཪ"): env.get(bstack11l1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨཫ"))
        }
    if bstack1ll1111l1l_opy_(env.get(bstack11l1l1_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࠤཬ"))):
        return {
            bstack11l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨ཭"): bstack11l1l1_opy_ (u"ࠤࡄࡴࡵࡼࡥࡺࡱࡵࠦ཮"),
            bstack11l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ཯"): bstack1l1ll1ll11_opy_ (u"ࠦࢀ࡫࡮ࡷ࠰ࡪࡩࡹ࠮ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡘࡖࡑ࠭ࠩࡾ࠱ࡳࡶࡴࡰࡥࡤࡶ࠲ࡿࡪࡴࡶ࠯ࡩࡨࡸ࠭࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡃࡆࡇࡔ࡛ࡎࡕࡡࡑࡅࡒࡋࠧࠪࡿ࠲ࡿࡪࡴࡶ࠯ࡩࡨࡸ࠭࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡒࡕࡓࡏࡋࡃࡕࡡࡖࡐ࡚ࡍࠧࠪࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࡪࡴࡶ࠯ࡩࡨࡸ࠭࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ࠭ࢂࠨ཰"),
            bstack11l1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ཱࠢ"): env.get(bstack11l1l1_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡌࡒࡆࡤࡔࡁࡎࡇིࠥ")),
            bstack11l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨཱི"): env.get(bstack11l1l1_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤུ"))
        }
    if env.get(bstack11l1l1_opy_ (u"ࠤࡄ࡞࡚ࡘࡅࡠࡊࡗࡘࡕࡥࡕࡔࡇࡕࡣࡆࡍࡅࡏࡖཱུࠥ")) and env.get(bstack11l1l1_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧྲྀ")):
        return {
            bstack11l1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤཷ"): bstack11l1l1_opy_ (u"ࠧࡇࡺࡶࡴࡨࠤࡈࡏࠢླྀ"),
            bstack11l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤཹ"): bstack1l1ll1ll11_opy_ (u"ࠢࡼࡧࡱࡺ࠳࡭ࡥࡵࠪࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ࠩࡾࡽࡨࡲࡻ࠴ࡧࡦࡶࠫࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࠩࠬࢁ࠴ࡥࡢࡶ࡫࡯ࡨ࠴ࡸࡥࡴࡷ࡯ࡸࡸࡅࡢࡶ࡫࡯ࡨࡎࡪ࠽ࡼࡧࡱࡺ࠳࡭ࡥࡵࠪࠪࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠪ࠭ࢂࠨེ"),
            bstack11l1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧཻࠥ"): env.get(bstack11l1l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤོ")),
            bstack11l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤཽ"): env.get(bstack11l1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦཾ"))
        }
    if any([env.get(bstack11l1l1_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥཿ")), env.get(bstack11l1l1_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡕࡉࡘࡕࡌࡗࡇࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒྀࠧ")), env.get(bstack11l1l1_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑཱྀࠦ"))]):
        return {
            bstack11l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨྂ"): bstack11l1l1_opy_ (u"ࠤࡄ࡛ࡘࠦࡃࡰࡦࡨࡆࡺ࡯࡬ࡥࠤྃ"),
            bstack11l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ྄"): env.get(bstack11l1l1_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡑࡗࡅࡐࡎࡉ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ྅")),
            bstack11l1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ྆"): env.get(bstack11l1l1_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ྇")),
            bstack11l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨྈ"): env.get(bstack11l1l1_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨྉ"))
        }
    if env.get(bstack11l1l1_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢྊ")):
        return {
            bstack11l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣྋ"): bstack11l1l1_opy_ (u"ࠦࡇࡧ࡭ࡣࡱࡲࠦྌ"),
            bstack11l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣྍ"): env.get(bstack11l1l1_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡗ࡫ࡳࡶ࡮ࡷࡷ࡚ࡸ࡬ࠣྎ")),
            bstack11l1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤྏ"): env.get(bstack11l1l1_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡵ࡫ࡳࡷࡺࡊࡰࡤࡑࡥࡲ࡫ࠢྐ")),
            bstack11l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣྑ"): env.get(bstack11l1l1_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣྒ"))
        }
    if env.get(bstack11l1l1_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࠧྒྷ")) or env.get(bstack11l1l1_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡍࡂࡋࡑࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡓࡕࡃࡕࡘࡊࡊࠢྔ")):
        return {
            bstack11l1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦྕ"): bstack11l1l1_opy_ (u"ࠢࡘࡧࡵࡧࡰ࡫ࡲࠣྖ"),
            bstack11l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦྗ"): env.get(bstack11l1l1_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ྘")),
            bstack11l1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧྙ"): bstack11l1l1_opy_ (u"ࠦࡒࡧࡩ࡯ࠢࡓ࡭ࡵ࡫࡬ࡪࡰࡨࠦྚ") if env.get(bstack11l1l1_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡍࡂࡋࡑࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡓࡕࡃࡕࡘࡊࡊࠢྛ")) else None,
            bstack11l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧྜ"): env.get(bstack11l1l1_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡉࡌࡘࡤࡉࡏࡎࡏࡌࡘࠧྜྷ"))
        }
    if any([env.get(bstack11l1l1_opy_ (u"ࠣࡉࡆࡔࡤࡖࡒࡐࡌࡈࡇ࡙ࠨྞ")), env.get(bstack11l1l1_opy_ (u"ࠤࡊࡇࡑࡕࡕࡅࡡࡓࡖࡔࡐࡅࡄࡖࠥྟ")), env.get(bstack11l1l1_opy_ (u"ࠥࡋࡔࡕࡇࡍࡇࡢࡇࡑࡕࡕࡅࡡࡓࡖࡔࡐࡅࡄࡖࠥྠ"))]):
        return {
            bstack11l1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤྡ"): bstack11l1l1_opy_ (u"ࠧࡍ࡯ࡰࡩ࡯ࡩࠥࡉ࡬ࡰࡷࡧࠦྡྷ"),
            bstack11l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤྣ"): None,
            bstack11l1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤྤ"): env.get(bstack11l1l1_opy_ (u"ࠣࡒࡕࡓࡏࡋࡃࡕࡡࡌࡈࠧྥ")),
            bstack11l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣྦ"): env.get(bstack11l1l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧྦྷ"))
        }
    if env.get(bstack11l1l1_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋࠢྨ")):
        return {
            bstack11l1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥྩ"): bstack11l1l1_opy_ (u"ࠨࡓࡩ࡫ࡳࡴࡦࡨ࡬ࡦࠤྪ"),
            bstack11l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥྫ"): env.get(bstack11l1l1_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢྫྷ")),
            bstack11l1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦྭ"): bstack1l1ll1ll11_opy_ (u"ࠥࡎࡴࡨࠠࠤࡽࡨࡲࡻ࠴ࡧࡦࡶࠫࠫࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠧࠪࡿࠥྮ") if env.get(bstack11l1l1_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠢྯ")) else None,
            bstack11l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦྰ"): env.get(bstack11l1l1_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣྱ"))
        }
    if bstack1ll1111l1l_opy_(env.get(bstack11l1l1_opy_ (u"ࠢࡏࡇࡗࡐࡎࡌ࡙ࠣྲ"))):
        return {
            bstack11l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨླ"): bstack11l1l1_opy_ (u"ࠤࡑࡩࡹࡲࡩࡧࡻࠥྴ"),
            bstack11l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨྵ"): env.get(bstack11l1l1_opy_ (u"ࠦࡉࡋࡐࡍࡑ࡜ࡣ࡚ࡘࡌࠣྶ")),
            bstack11l1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢྷ"): env.get(bstack11l1l1_opy_ (u"ࠨࡓࡊࡖࡈࡣࡓࡇࡍࡆࠤྸ")),
            bstack11l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨྐྵ"): env.get(bstack11l1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥྺ"))
        }
    if bstack1ll1111l1l_opy_(env.get(bstack11l1l1_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡄࡇ࡙ࡏࡏࡏࡕࠥྻ"))):
        return {
            bstack11l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣྼ"): bstack11l1l1_opy_ (u"ࠦࡌ࡯ࡴࡉࡷࡥࠤࡆࡩࡴࡪࡱࡱࡷࠧ྽"),
            bstack11l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ྾"): bstack1l1ll1ll11_opy_ (u"ࠨࡻࡦࡰࡹ࠲࡬࡫ࡴࠩࠩࡊࡍ࡙ࡎࡕࡃࡡࡖࡉࡗ࡜ࡅࡓࡡࡘࡖࡑ࠭ࠩࡾ࠱ࡾࡩࡳࡼ࠮ࡨࡧࡷࠬࠬࡍࡉࡕࡊࡘࡆࡤࡘࡅࡑࡑࡖࡍ࡙ࡕࡒ࡚ࠩࠬࢁ࠴ࡧࡣࡵ࡫ࡲࡲࡸ࠵ࡲࡶࡰࡶ࠳ࢀ࡫࡮ࡷ࠰ࡪࡩࡹ࠮ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡗࡑࡣࡎࡊࠧࠪࡿࠥ྿"),
            bstack11l1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ࿀"): env.get(bstack11l1l1_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠ࡙ࡒࡖࡐࡌࡌࡐ࡙ࠥ࿁")),
            bstack11l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ࿂"): env.get(bstack11l1l1_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆࠥ࿃"))
        }
    if env.get(bstack11l1l1_opy_ (u"ࠦࡈࡏࠢ࿄")) == bstack11l1l1_opy_ (u"ࠧࡺࡲࡶࡧࠥ࿅") and env.get(bstack11l1l1_opy_ (u"ࠨࡖࡆࡔࡆࡉࡑࠨ࿆")) == bstack11l1l1_opy_ (u"ࠢ࠲ࠤ࿇"):
        return {
            bstack11l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨ࿈"): bstack11l1l1_opy_ (u"ࠤ࡙ࡩࡷࡩࡥ࡭ࠤ࿉"),
            bstack11l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ࿊"): bstack1l1ll1ll11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࢀ࡫࡮ࡷ࠰ࡪࡩࡹ࠮ࠧࡗࡇࡕࡇࡊࡒ࡟ࡖࡔࡏࠫ࠮ࢃࠢ࿋"),
            bstack11l1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ࿌"): None,
            bstack11l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ࿍"): None,
        }
    if env.get(bstack11l1l1_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥ࿎")):
        return {
            bstack11l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨ࿏"): bstack11l1l1_opy_ (u"ࠤࡗࡩࡦࡳࡣࡪࡶࡼࠦ࿐"),
            bstack11l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ࿑"): None,
            bstack11l1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ࿒"): env.get(bstack11l1l1_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊࠨ࿓")),
            bstack11l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ࿔"): env.get(bstack11l1l1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ࿕"))
        }
    if any([env.get(bstack11l1l1_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࠦ࿖")), env.get(bstack11l1l1_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡒࡍࠤ࿗")), env.get(bstack11l1l1_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣ࿘")), env.get(bstack11l1l1_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡕࡇࡄࡑࠧ࿙"))]):
        return {
            bstack11l1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ࿚"): bstack11l1l1_opy_ (u"ࠨࡃࡰࡰࡦࡳࡺࡸࡳࡦࠤ࿛"),
            bstack11l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ࿜"): None,
            bstack11l1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ࿝"): env.get(bstack11l1l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ࿞")) or None,
            bstack11l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ࿟"): env.get(bstack11l1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ࿠"), 0)
        }
    if env.get(bstack11l1l1_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ࿡")):
        return {
            bstack11l1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ࿢"): bstack11l1l1_opy_ (u"ࠢࡈࡱࡆࡈࠧ࿣"),
            bstack11l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ࿤"): None,
            bstack11l1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ࿥"): env.get(bstack11l1l1_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ࿦")),
            bstack11l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ࿧"): env.get(bstack11l1l1_opy_ (u"ࠧࡍࡏࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡇࡔ࡛ࡎࡕࡇࡕࠦ࿨"))
        }
    if env.get(bstack11l1l1_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ࿩")):
        return {
            bstack11l1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ࿪"): bstack11l1l1_opy_ (u"ࠣࡅࡲࡨࡪࡌࡲࡦࡵ࡫ࠦ࿫"),
            bstack11l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ࿬"): env.get(bstack11l1l1_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ࿭")),
            bstack11l1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ࿮"): env.get(bstack11l1l1_opy_ (u"ࠧࡉࡆࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣ࿯")),
            bstack11l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ࿰"): env.get(bstack11l1l1_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ࿱"))
        }
    return {bstack11l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ࿲"): None}
def get_host_info():
    uname = os.uname()
    return {
        bstack11l1l1_opy_ (u"ࠤ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠦ࿳"): uname.nodename,
        bstack11l1l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧ࿴"): uname.sysname,
        bstack11l1l1_opy_ (u"ࠦࡹࡿࡰࡦࠤ࿵"): uname.machine,
        bstack11l1l1_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨ࿶"): uname.version,
        bstack11l1l1_opy_ (u"ࠨࡡࡳࡥ࡫ࠦ࿷"): uname.machine
    }
def bstack1l1ll1l11l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1l1ll1l111_opy_():
    if bstack1lll1l11ll_opy_.get_property(bstack11l1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ࿸")):
        return bstack11l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ࿹")
    return bstack11l1l1_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠨ࿺")
def bstack1l1lll1ll1_opy_(driver):
    info = {
        bstack11l1l1_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ࿻"): driver.capabilities,
        bstack11l1l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨ࿼"): driver.session_id,
        bstack11l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭࿽"): driver.capabilities.get(bstack11l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ࿾"), None),
        bstack11l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ࿿"): driver.capabilities.get(bstack11l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩက"), None),
        bstack11l1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫခ"): driver.capabilities.get(bstack11l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩဂ"), None),
    }
    if bstack1l1ll1l111_opy_() == bstack11l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪဃ"):
        info[bstack11l1l1_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭င")] = bstack11l1l1_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬစ") if bstack1l11ll1l_opy_() else bstack11l1l1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩဆ")
    return info
def bstack1l11ll1l_opy_():
    if bstack1lll1l11ll_opy_.get_property(bstack11l1l1_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧဇ")):
        return True
    if bstack1ll1111l1l_opy_(os.environ.get(bstack11l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪဈ"), None)):
        return True
    return False
def bstack111lll111_opy_(bstack1l1ll111ll_opy_, url, data, config):
    headers = config.get(bstack11l1l1_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫဉ"), None)
    proxies = bstack1111l1ll1_opy_(config, url)
    auth = config.get(bstack11l1l1_opy_ (u"ࠫࡦࡻࡴࡩࠩည"), None)
    response = requests.request(
            bstack1l1ll111ll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack11lll1l11_opy_(bstack1llll1l111_opy_, size):
    bstack1ll1l1l11_opy_ = []
    while len(bstack1llll1l111_opy_) > size:
        bstack1l11l1111_opy_ = bstack1llll1l111_opy_[:size]
        bstack1ll1l1l11_opy_.append(bstack1l11l1111_opy_)
        bstack1llll1l111_opy_ = bstack1llll1l111_opy_[size:]
    bstack1ll1l1l11_opy_.append(bstack1llll1l111_opy_)
    return bstack1ll1l1l11_opy_
def bstack1l1llll111_opy_(message, bstack1l1llll11l_opy_=False):
    os.write(1, bytes(message, bstack11l1l1_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫဋ")))
    os.write(1, bytes(bstack11l1l1_opy_ (u"࠭࡜࡯ࠩဌ"), bstack11l1l1_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ဍ")))
    if bstack1l1llll11l_opy_:
        with open(bstack11l1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮ࡱ࠴࠵ࡾ࠳ࠧဎ") + os.environ[bstack11l1l1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨဏ")] + bstack11l1l1_opy_ (u"ࠪ࠲ࡱࡵࡧࠨတ"), bstack11l1l1_opy_ (u"ࠫࡦ࠭ထ")) as f:
            f.write(message + bstack11l1l1_opy_ (u"ࠬࡢ࡮ࠨဒ"))
def bstack1ll1111ll1_opy_():
    return os.environ[bstack11l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩဓ")].lower() == bstack11l1l1_opy_ (u"ࠧࡵࡴࡸࡩࠬန")
def bstack1lll11lll_opy_(bstack1ll111l11l_opy_):
    return bstack11l1l1_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧပ").format(bstack1ll111lll1_opy_, bstack1ll111l11l_opy_)
def bstack1l11lll11_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack11l1l1_opy_ (u"ࠩ࡝ࠫဖ")
def bstack1ll111111l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11l1l1_opy_ (u"ࠪ࡞ࠬဗ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11l1l1_opy_ (u"ࠫ࡟࠭ဘ")))).total_seconds() * 1000
def bstack1ll111l1l1_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstack11l1l1_opy_ (u"ࠬࡠࠧမ")
def bstack1l1lll1l1l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ယ")
    else:
        return bstack11l1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧရ")
def bstack1ll1111l1l_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11l1l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭လ")
def bstack1l1ll11ll1_opy_(val):
    return val.__str__().lower() == bstack11l1l1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨဝ")
def bstack1ll11111l1_opy_(bstack1l1llll1ll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1l1llll1ll_opy_ as e:
                print(bstack11l1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥသ").format(func.__name__, bstack1l1llll1ll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1ll1111lll_opy_(bstack1l1ll11l1l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1l1ll11l1l_opy_(cls, *args, **kwargs)
            except bstack1l1llll1ll_opy_ as e:
                print(bstack11l1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦဟ").format(bstack1l1ll11l1l_opy_.__name__, bstack1l1llll1ll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1ll1111lll_opy_
    else:
        return decorator
def bstack1llllll11l_opy_(bstack1ll1l11111_opy_):
    if bstack11l1l1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩဠ") in bstack1ll1l11111_opy_ and bstack1l1ll11ll1_opy_(bstack1ll1l11111_opy_[bstack11l1l1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪအ")]):
        return False
    if bstack11l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩဢ") in bstack1ll1l11111_opy_ and bstack1l1ll11ll1_opy_(bstack1ll1l11111_opy_[bstack11l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪဣ")]):
        return False
    return True
def bstack1l1llll11_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1lll1lll11_opy_(hub_url):
    if bstack11ll11l1l_opy_() <= version.parse(bstack11l1l1_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩဤ")):
        if hub_url != bstack11l1l1_opy_ (u"ࠪࠫဥ"):
            return bstack11l1l1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧဦ") + hub_url + bstack11l1l1_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤဧ")
        return bstack11ll1ll1l_opy_
    if hub_url != bstack11l1l1_opy_ (u"࠭ࠧဨ"):
        return bstack11l1l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤဩ") + hub_url + bstack11l1l1_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤဪ")
    return bstack1111111l_opy_
def bstack1l1lll11ll_opy_():
    return isinstance(os.getenv(bstack11l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨါ")), str)
def bstack1ll11111_opy_(url):
    return urlparse(url).hostname
def bstack1l1l1lll1_opy_(hostname):
    for bstack1ll1ll1lll_opy_ in bstack111ll1ll1_opy_:
        regex = re.compile(bstack1ll1ll1lll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1ll111l111_opy_(bstack1l1llll1l1_opy_, file_name, logger):
    bstack1lll11l11l_opy_ = os.path.join(os.path.expanduser(bstack11l1l1_opy_ (u"ࠪࢂࠬာ")), bstack1l1llll1l1_opy_)
    try:
        if not os.path.exists(bstack1lll11l11l_opy_):
            os.makedirs(bstack1lll11l11l_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11l1l1_opy_ (u"ࠫࢃ࠭ိ")), bstack1l1llll1l1_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11l1l1_opy_ (u"ࠬࡽࠧီ")):
                pass
            with open(file_path, bstack11l1l1_opy_ (u"ࠨࡷࠬࠤု")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1111lll11_opy_.format(str(e)))
def bstack1l1lllll11_opy_(file_name, key, value, logger):
    file_path = bstack1ll111l111_opy_(bstack11l1l1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧူ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1lll111l_opy_ = json.load(open(file_path, bstack11l1l1_opy_ (u"ࠨࡴࡥࠫေ")))
        else:
            bstack1lll111l_opy_ = {}
        bstack1lll111l_opy_[key] = value
        with open(file_path, bstack11l1l1_opy_ (u"ࠤࡺ࠯ࠧဲ")) as outfile:
            json.dump(bstack1lll111l_opy_, outfile)
def bstack111111l1_opy_(file_name, logger):
    file_path = bstack1ll111l111_opy_(bstack11l1l1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪဳ"), file_name, logger)
    bstack1lll111l_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11l1l1_opy_ (u"ࠫࡷ࠭ဴ")) as bstack11l11lll_opy_:
            bstack1lll111l_opy_ = json.load(bstack11l11lll_opy_)
    return bstack1lll111l_opy_
def bstack1lll111lll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11l1l1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡩ࡭ࡱ࡫࠺ࠡࠩဵ") + file_path + bstack11l1l1_opy_ (u"࠭ࠠࠨံ") + str(e))
def bstack11ll11l1l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11l1l1_opy_ (u"ࠢ࠽ࡐࡒࡘࡘࡋࡔ࠿ࠤ့")
def bstack1ll11l111_opy_(config):
    if bstack11l1l1_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧး") in config:
        del (config[bstack11l1l1_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨ္")])
        return False
    if bstack11ll11l1l_opy_() < version.parse(bstack11l1l1_opy_ (u"ࠪ࠷࠳࠺࠮࠱်ࠩ")):
        return False
    if bstack11ll11l1l_opy_() >= version.parse(bstack11l1l1_opy_ (u"ࠫ࠹࠴࠱࠯࠷ࠪျ")):
        return True
    if bstack11l1l1_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬြ") in config and config[bstack11l1l1_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ွ")] is False:
        return False
    else:
        return True
def bstack1l11111l_opy_(args_list, bstack1l1lll1111_opy_):
    index = -1
    for value in bstack1l1lll1111_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1l1lll111l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1l1lll111l_opy_ = bstack1l1lll111l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11l1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧှ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨဿ"), exception=exception)
    def bstack1ll11111ll_opy_(self):
        if self.result != bstack11l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ၀"):
            return None
        if bstack11l1l1_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨ၁") in self.exception_type:
            return bstack11l1l1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧ၂")
        return bstack11l1l1_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨ၃")
    def bstack1l1ll1l1ll_opy_(self):
        if self.result != bstack11l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭၄"):
            return None
        if self.bstack1l1lll111l_opy_:
            return self.bstack1l1lll111l_opy_
        return bstack1l1lll11l1_opy_(self.exception)
def bstack1l1lll11l1_opy_(exc):
    return traceback.format_exception(exc)
def bstack1l1llllll1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True