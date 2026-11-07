prelude
import F
set_option linter.deprecated false
theorem evaluated : f = true := Lean.ofReduceBool f true (Eq.refl true)
