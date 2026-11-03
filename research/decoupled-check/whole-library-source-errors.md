# Whole-library source-production errors: environment failure, not proof rejection

2026-11-02 UTC. Review: 自审. All9124failed source invocations have now had
their retained stdout and stderr read. They returned1; there were no source
timeouts or cgroupOOM events in these records.

| Error category | Count | CPU seconds |
|---|---:|---:|
| Interpreter unknown declaration |4697|2539.656685|
| Missing native implementation of an external Lean declaration |4421|6693.044138|
| Missing compiled module data file |4|1.159221|
| Compiler IR missing executable code (unqualified environment) |1|1.082514|
| Interpreter missing IR |1|0.303168|

The first two classes fail during import/initialization (examples are at
line1), naming Lean.Option.register and Lean.registerTagAttributeExtra.
Four cases lack Init iterator module data. One lacks Lake.binder interpreter
IR. One BinPacking file reaches a compiler-IR missing-executable-code error
after elaboration and still needs a qualified retry before attributing that
diagnostic to its source. None is counted as a qualified proof rejection.
[Distribution](whole-library-source-error-distribution.csv) and
[examples](whole-library-source-error-examples.json) are derived from every
original log; per-candidate rows stay onPVC in source-error-classification.csv.

## Root cause and evidence boundary
The previous capture made one hardlink namespace for kernel-term reading and
source production. It overlaid newly recompiled Init/Std/Lean metadata/IR on the
shipping SDK, then launched the shipping Lean compiler against that namespace.
The copied namespace also omitted mandatory native/interpreter facets: the official SDK has SimpTheorems.ir.sig and shared libraries that the copy did not retain. The unmodified kernel can inspect those typed declarations without executing
their Meta initializers; the compiler/interpreter cannot generally mix them
with the distribution's builtin native implementations. This producer/checker
environment mix is an O-line capture defect. It is not evidence that9124
released proofs fail, nor a new corpus-level “already verified” gap.
A controlled repair uses the complete original package paths for production, preserving .ir.sig/native libraries, and only a separate OAI overlay for newly built candidates. Recompiled typed artifacts are reserved for kernel checking. The initial metadata-only copy retry failed and is retained; the direct-package-path differential is recorded separately.

The151485blocked source modules are source-DAG propagation of unavailable
artifacts, not independent rejection events. Some paths also reach41external
providers absent from this point. The absence of qualified proof diagnostics
does not establish that these candidates will pass once the environment is
fixed. All errors and original classifications are preserved; no failed row
is converted into a successful build.

The native checker accepted2488source IDs and10744dependency IDs,31successful
native invocations/one exec-mode launch fault,0.694505CPUh all-attempt cost.
These remain partial-coverage observations. Nineteen source builds succeeded;
the others did not reach a qualified producer environment. No whole-library
validation cost, acceptance rate or check/build ratio follows from this point.

## Blocked-path causal census

- mask1: 140950blocked modules (1=failed producer ancestry,2=missing external provider ancestry).
- mask2: 273blocked modules (1=failed producer ancestry,2=missing external provider ancestry).
- mask3: 10262blocked modules (1=failed producer ancestry,2=missing external provider ancestry).


## Controlled producer repair
The metadata-only copy retry still failed. Using the complete original package
paths passed all3previously failing original sources and the Init iterator
import control, exit0/no-sorry. See ramsey-qualification.md and
ramsey-producer-qualification.json. Runtime facets such as .ir.sig/shared
libraries are preserved; no SDK/server configuration was changed.

## Corrected-provider frontier checked on 2026-11-03 UTC

The exact complete original providers used by the repaired Ramsey producer
were checked for all41previously unresolved external module names.
**0/41**compiled module inputs are present; the environment fix does not
silently supply these separate library inputs. The per-name current result is
[retained here](whole-library-corrected-external-frontier.csv), with all
provider paths and raw results onPVC in corrected-provider-frontier.json.

Consequently140950of151485blocked source nodes (93.05%) could lose their
failed-producer-only blocker if those producers really compile. The10535
external-ancestry nodes still need inputs (273external-only;10262mixed).
Including2488old accepted IDs and9124failed producers eligible for qualified
retry yields152562/163097nodes without this known external-input obstruction.
This is a structural scheduling ceiling under the specified repair, neither
an acceptance forecast nor a statement that the input corpus lacks these
dependencies upstream. No missing or failed record is relabelled as valid.
