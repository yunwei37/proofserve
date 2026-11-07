# Lean 4.34.1 官方检查器的三条观察

本目录为 blog 提供事实核实和最小复现，不涉及 ProofServe 的实现、性能或发布。结论来自官方发行版中的 lean、leanchecker 和公开的 Lean API；没有修改内核、官方程序或冻结的 checker。全部原生测量于 **2026-11-06 20:14:44 UTC** 完成，距 19:57 UTC 开始核实约 18 分钟。报告写入时间另见 version.json，不将晚写报告当作继续测量。

版本为 **Lean 4.34.1 / commit 5045d0056413266e57c625dcd7c365b10e377c52 / Linux x86-64 Release**，来源为[官方发行版](https://github.com/leanprover/lean4/releases/tag/v4.34.1)。SDK 随附的四个 Lean 源文件与从这个 commit 下载的上游文件逐字节一致。所有实验使用 CPUs 0–7，没有 -M、LD_PRELOAD 或 P 核锁。编排和结果分析在 CPUs 8–9；没有运行新一轮性能矩阵。

## 1. 同一产物在默认模式和 --fresh 下得到不同结果：已确认

这两种模式承担不同的检查工作，不能把退出码不同直接表述成同一逻辑内核自相矛盾。

### 1a. 缺少 private 分片

输入是 examples/Parts.lean。用官方编译器生成完整的模块系统产物时，默认和 fresh 都退出 0。随后只移走 Parts.olean.private，保留 .olean、.olean.server、.ir 和 .ir.sig，其余输入不变：

    lean -o Parts.olean Parts.lean
    mv Parts.olean.private Parts.olean.private.retained
    leanchecker -v Parts
    leanchecker -v --fresh Parts

运行前把该目录加入 LEAN_PATH。结果：

| 输入 | 默认退出码 | fresh 退出码 |
| --- | ---: | ---: |
| 完整编译产物 | 0 | 0 |
| 同一产物移走 private 分片 | 0 | 1 |

默认输出 replaying Parts，未报错。fresh 输出 replaying Parts with --fresh，随后报 failed to open file .../Parts.olean.private: No such file or directory。完整原始输出在 cases.csv。

原因：[LeanChecker.lean 12–34 行](https://github.com/leanprover/lean4/blob/5045d0056413266e57c625dcd7c365b10e377c52/src/LeanChecker.lean#L12-L34) 在目标模块上按文件是否存在读取可用分片，并重放最后一个可用分片。[36–38 行](https://github.com/leanprover/lean4/blob/5045d0056413266e57c625dcd7c365b10e377c52/src/LeanChecker.lean#L36-L38) 的 fresh 路径先正常导入目标；[Environment.lean 2078–2091 行](https://github.com/leanprover/lean4/blob/5045d0056413266e57c625dcd7c365b10e377c52/src/Lean/Environment.lean#L2078-L2091) 对模块系统产物读取三个分片，缺失 private 就失败。

**适用边界：这是人为不完整的序列化产物，不是正常编译出的错误定理。** 本例没有证明一个错误命题被内核接受，也没有断言默认模式对缺失部分检查了什么。可写的发现是“完整性检查路径不同，默认成功不等于 fresh 成功”。

### 1b. 显式原生求值

examples/F.lean 定义 f : Bool := true。examples/Eval.lean 导入 F，并声明：

    theorem evaluated : f = true :=
      Lean.ofReduceBool f true (Eq.refl true)

两文件均由官方编译器成功生成产物，所有分片和 IR 保持完整：

    lean -o F.olean F.lean
    lean -o Eval.olean Eval.lean
    leanchecker -v Eval
    leanchecker -v --fresh Eval

默认退出 0；fresh 退出 1，报：

    uncaught exception: while replaying declaration 'evaluated':
    (kernel) (interpreter) unknown declaration 'f'

[LeanChecker.lean 27–33 行](https://github.com/leanprover/lean4/blob/5045d0056413266e57c625dcd7c365b10e377c52/src/LeanChecker.lean#L27-L33) 的默认路径保留导入环境；fresh 在 36–38 行只把常量映射重放到空内核环境，没有把原环境的 IR 扩展搬过去。[type_checker.cpp 614–631 行](https://github.com/leanprover/lean4/blob/5045d0056413266e57c625dcd7c365b10e377c52/src/kernel/type_checker.cpp#L614-L631) 会对这个 primitive 调用 IR 求值器；[ir_interpreter.cpp 872–878 行](https://github.com/leanprover/lean4/blob/5045d0056413266e57c625dcd7c365b10e377c52/src/library/ir_interpreter.cpp#L872-L878) 在找不到 IR 声明时给出上述错误。

**适用边界：本例显式使用 deprecated 的 Lean.ofReduceBool 桥接公理，不是普通的 decide +kernel 样例。** 结论是 fresh 对这种 IR 依赖的支持限制，不是所证命题为假，也不能外推到所有计算型证明或 native_decide。

## 2. 同接口定理的合并与坏证明体：有限范围已确认，笼统说法不成立

可确认的是：导入环境可以只保留一个同接口定理体，fresh 检查的是合并后的映射，不能保证逐个复查原始模块中所有被覆盖的证明体。**“官方不会检查第二个坏证明体”这个不带条件的说法不成立。**

最小输入为 examples/Base.lean、A.lean、B.lean、C.lean。Base 仅声明 P : Prop 和 witness : P；A、B 各自声明同名定理 same : P := witness，C 依次导入 A 和 B。首先所有正常产物在两种模式下都通过。然后用 examples/Mutate.lean 的公开 readModuleDataParts/saveModuleData API，仅把 B 的 same 证明体改为未绑定的 bvar 0。这是故意无效的序列化测试输入，正常源文件 elaboration 不会生成它；没有改定理名、类型、宇宙参数、all 字段或导入顺序。

    lean -o Base.olean Base.lean
    lean -o A.olean A.lean
    lean -o B.olean B.lean
    lean -o C.olean C.lean
    lean --run Mutate.lean B.olean B B.changed
    cp B.changed B.olean

检查这同一个坏 B：

| 检查根 | 根的导入顺序 | 默认退出码 | fresh 退出码 |
| --- | --- | ---: | ---: |
| B | 只有 Base | 1 | 1 |
| C | A（好体），B（坏体） | 0 | 1 |
| Reverse | B（坏体），A（好体） | 0 | 0 |
| OnlyBad | 只有 B（坏体） | 0 | 1 |

Reverse 和 OnlyBad 也由官方编译器生成，源码分别为 prelude 后 import B / import A，以及仅 import B。每行的命令均为 leanchecker -v ROOT 和 leanchecker -v --fresh ROOT。拒绝时的诊断为：

    while replaying declaration 'same':
    (kernel) type checker does not support loose bound variables,
    replace them with free variables before invoking it

源码解释：

- [Environment.lean 2261–2274 行](https://github.com/leanprover/lean4/blob/5045d0056413266e57c625dcd7c365b10e377c52/src/Lean/Environment.lean#L2261-L2274) 的同接口比较不要求定理 value 相同；[2332–2343 行](https://github.com/leanprover/lean4/blob/5045d0056413266e57c625dcd7c365b10e377c52/src/Lean/Environment.lean#L2332-L2343) 可以用后面的记录替换已有记录。
- [LeanChecker.lean 36–38 行](https://github.com/leanprover/lean4/blob/5045d0056413266e57c625dcd7c365b10e377c52/src/LeanChecker.lean#L36-L38) 的 fresh 只重放最终 env.constants.map₁。被覆盖的 B 坏体不在 Reverse 的最终映射里；选中 B 坏体的 C 则确实被拒绝。
- 默认模式只重放目标模块自己的新常量，不递归重检导入依赖。C、Reverse、OnlyBad 没有自身定理，默认通过不能用来声称 A 或 B 已被验证。B 单独作为根时，两种模式都能发现坏体。
- [Replay.lean 84–97 行](https://github.com/leanprover/lean4/blob/5045d0056413266e57c625dcd7c365b10e377c52/src/Lean/Replay.lean#L84-L97) 确有遇到环境中同接口定理就跳过的分支；本轮没有为这个函数另造内部内核环境。官方 CLI 的实测结论主要由导入合并及最终映射解释，不能把每个 CLI 成功都归因于该分支。

**可用于 blog 的表述：**“检查最终合并环境，和逐个检查原始模块中的每份证明体，不是同一个验收目标。官方 fresh 能拒绝选中的坏体，但被同接口好体覆盖的坏体不一定还在它的检查输入中。”本例以序列化产物为对象，没有展示正常编译的 Lean 源码能证明假命题。

## 3. Nat.Basic 的大系统态成本：搜索路径处理已确认，‘主要在遍历目录’需修正

本轮一次大/小搜索路径对照检查同一个 Mathlib.Data.Nat.Basic 根。输入为 OAI 4eaee875 与 Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612 的既有构建环境，保留此前构建使用的兼容性改动；没有将这些产物称为未修改上游源的重新构建。其官方导入闭包有 1,330 个模块。小视图为这些模块的原始产物建立同设备、同 inode 的硬链接；包括存在的 olean/server/private/IR 分片，测量后再次逐个核对 inode。它没有重编译或修改任何产物。运行时仍附加官方 SDK 搜索路径。两次默认检查都退出 0，只输出 replaying Mathlib.Data.Nat.Basic。

| 官方默认检查，一次观测 | 墙钟 s | 用户 CPU s | 系统 CPU s |
| --- | ---: | ---: | ---: |
| 小搜索路径 | 0.394 | 0.217 | 0.176 |
| 原有大搜索路径 | 322.853 | 44.739 | 234.609 |

大路径这次的系统态占总 CPU 约 84%。**没有复现固定的“407 秒”这个数**，也没有把两个单次观测当作重复统计或普遍加速比。缓存、背景和环境会影响绝对墙钟。

进一步只调用官方 CLI 所用的两个发现步骤，不执行 replay；在 examples/Discovery.lean 内以 monoNanosNow 分别计时：

| 搜索路径 | 路径项 | 枚举到的 olean 路径条目 | 目录枚举 s | 模块名解析和前缀筛选 s |
| --- | ---: | ---: | ---: | ---: |
| 小路径 | 2 | 3,850 | 0.047 | 0.070 |
| 大路径 | 90 | 203,273 | 2.611 | 271.426 |

条目数不是唯一模块数：原有 LEAN_PATH 包含重复根。两个探针都只找到 Mathlib.Data.Nat.Basic 一个目标。探针整进程的大路径 CPU 为用户 44.736 秒、系统 230.391 秒，接近完整官方检查的 CPU 成本；这是分开的运行，且探针由官方 lean --run 执行，外围循环和启动可有额外开销，**不是在同一次检查中测得的精确占比**。它支持大部分系统态 CPU 来自模块发现，而不是这个根的证明检查。完整检查的剩余墙钟没有做系统调用级归因，不把差值硬塞给某个原因。

准确说，应写成“对搜索路径中所有候选执行发现和模块名解析”，而不能只说“遍历目录”：本轮绝大多数探针时间在逐路径的模块名解析。源码：

- [LeanChecker.lean 87–97 行](https://github.com/leanprover/lean4/blob/5045d0056413266e57c625dcd7c365b10e377c52/src/LeanChecker.lean#L87-L97)：先枚举整个搜索路径，再把文件名解析为模块名并筛选目标，而非先定位这个根。
- [Lean/Util/Path.lean 74–79 行](https://github.com/leanprover/lean4/blob/5045d0056413266e57c625dcd7c365b10e377c52/src/Lean/Util/Path.lean#L74-L79)：目录遍历。
- [该文件 141–169 行](https://github.com/leanprover/lean4/blob/5045d0056413266e57c625dcd7c365b10e377c52/src/Lean/Util/Path.lean#L141-L169)：文件名与搜索根的规范化、逐根尝试及模块名恢复。

这是已有约 16 万模块产物环境的一次 bounded diagnosis，不是 Lean 的固有固定成本，也不代表普通小项目会遇到这种开销。没有继续做 perf、分配器、系统调用矩阵或内核修改。

## 完整复现与数据

准备官方 Lean 4.34.1 SDK；SDK 指向官方压缩包解开的根目录。RUN 指向新的持久数据目录，所有输出均在它下面：

    export SDK=/path/to/lean-4.34.1-linux
    export RUN=/path/to/persistent/new-lean-observation-run
    mkdir -p "$RUN/results"
    python3 data/lean-observations/reproduce.py "$SDK" "$RUN" "$PWD/data/lean-observations/examples"

该命令依次生成上述三个最小输入族、运行官方命令并保留输出/退出码。它使用系统 taskset、timeout，以及 Python wait4 读取资源；不依赖本 Workspace 的路径，也不调用 ProofServe。同名输出目录应使用新的 RUN；无效产物只存在于该样例目录。

第三项复现另外运行：

    python3 data/lean-observations/discovery_timing.py "$SDK" "$RUN" "$PWD/data/lean-observations/examples" /path/to/search-path-config.json

配置仅需 lean_path 字符串，内容为目标项目真实、已构建的依赖搜索路径；必须能解析 Mathlib.Data.Nat.Basic。它先用官方 importModules 获取闭包，再建立硬链接小视图，比较大小路径并输出发现阶段计时。使用不同的空 RUN/results 目录。本文大路径来自既有 OAI/Mathlib 工程，而不是要求陌生人复制本机绝对路径；精确本机路径保留在原始 command.json 中。默认每条命令自限 900 秒，导入闭包 180 秒，无 -M。

- cases.csv：16 个官方模式结果，完整 stdout/stderr；构建、产物变换等完整 26 条命令记录在原始目录。
- timings.csv：5 条已完成的设置/对照记录，包括一次闭包获取；不把闭包获取当作 checker 成本。
- discovery.csv：两个发现探针的阶段、条目数和目标。
- version.json：版本、原始目录、完成时间和产物身份方式。
- examples/、reproduce.py、discovery_timing.py：本轮最小源码和执行器。

全部原始、失败和部分记录留在 version.json 所指的 PVC 目录。本轮保留了三个设置失败：最初缺少 /usr/bin/time（改为 wait4）；第一次小路径用软链接，规范化后无法定位该根（改为同 inode 硬链接）；第二次探针的 import Lean 被小视图的部分 Lean 命名空间遮住（仅将探针编译环境保持为原路径，测量的搜索路径显式传入）。失败不混入最终计时。未安装系统包，未改安全配置、宿主机参数或冻结 checker。

本报告为**自审**。没有对上游发 issue/PR，没有修改论文，没有发布 blog，也不把这里的有限样例扩大成 Lean 逻辑不可靠的主张。
