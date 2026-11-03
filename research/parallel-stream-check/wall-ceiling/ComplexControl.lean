prelude
import Init.Prelude
set_option maxHeartbeats 2000000
def bound : Nat := 1
inductive Box : Nat → Type where
 | mk : Box bound
theorem good : Eq bound bound := Eq.refl bound
theorem good2 : Eq bound bound := good
