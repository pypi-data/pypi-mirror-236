import platform
import os,sys
# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 将当前脚本所在的目录添加到 sys.path
if platform.system() == "Darwin":
    sys.path.append(script_dir + os.sep + '_mac')
    from fengmm521_blecam._mac import cvUtil
    from fengmm521_blecam._mac import capimg
    from fengmm521_blecam._mac import camUtil
    from fengmm521_blecam._mac import httpUtil
    from fengmm521_blecam._mac import serialUtil
    from fengmm521_blecam._mac import serialFind
else:
    sys.path.append(script_dir + os.sep + '_windows')
    from fengmm521_blecam._windows import cvUtil
    from fengmm521_blecam._windows import capimg
    from fengmm521_blecam._windows import camUtil
    from fengmm521_blecam._windows import httpUtil
    from fengmm521_blecam._windows import serialUtil
    from fengmm521_blecam._windows import serialFind
__all__ = []