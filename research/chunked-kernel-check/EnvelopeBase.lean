import OAI.Analysis.Triangular.Envelope.EnvelopePsiB
namespace MEnvelopeBase
open OAI OAI.AtomicTriangular OAI.AtomicTriangular.Interval OAI.AtomicTriangular.FiniteCertificate
set_option maxHeartbeats 2000000
set_option maxRecDepth 20000
abbrev predicate (j : Fin 31) : Prop := (CI.ofReal (((envelopePhase01 j).re.neg).neg.mul (RI.point 16))).exp.re=envelopeExpB16 j
def rootGoal : Prop := ∀ j : Fin 31, predicate j
def goal_1_0 : Prop := ∀ j : Fin 31, 0 ≤ j.val → j.val < 31 → predicate j
theorem merge_1 (p0 : goal_1_0) : rootGoal := by
  intro j
  have hj := j.isLt
  exact p0 j (Nat.zero_le _) hj
def goal_2_0 : Prop := ∀ j : Fin 31, 0 ≤ j.val → j.val < 15 → predicate j
def goal_2_1 : Prop := ∀ j : Fin 31, 15 ≤ j.val → j.val < 31 → predicate j
theorem merge_2 (p0 : goal_2_0) (p1 : goal_2_1) : rootGoal := by
  intro j
  have hj := j.isLt
  by_cases h0 : j.val < 15
  · exact p0 j (Nat.zero_le _) h0
  exact p1 j (Nat.le_of_not_lt h0) hj
def goal_4_0 : Prop := ∀ j : Fin 31, 0 ≤ j.val → j.val < 7 → predicate j
def goal_4_1 : Prop := ∀ j : Fin 31, 7 ≤ j.val → j.val < 15 → predicate j
def goal_4_2 : Prop := ∀ j : Fin 31, 15 ≤ j.val → j.val < 23 → predicate j
def goal_4_3 : Prop := ∀ j : Fin 31, 23 ≤ j.val → j.val < 31 → predicate j
theorem merge_4 (p0 : goal_4_0) (p1 : goal_4_1) (p2 : goal_4_2) (p3 : goal_4_3) : rootGoal := by
  intro j
  have hj := j.isLt
  by_cases h0 : j.val < 7
  · exact p0 j (Nat.zero_le _) h0
  by_cases h1 : j.val < 15
  · exact p1 j (Nat.le_of_not_lt h0) h1
  by_cases h2 : j.val < 23
  · exact p2 j (Nat.le_of_not_lt h1) h2
  exact p3 j (Nat.le_of_not_lt h2) hj
def goal_8_0 : Prop := ∀ j : Fin 31, 0 ≤ j.val → j.val < 3 → predicate j
def goal_8_1 : Prop := ∀ j : Fin 31, 3 ≤ j.val → j.val < 7 → predicate j
def goal_8_2 : Prop := ∀ j : Fin 31, 7 ≤ j.val → j.val < 11 → predicate j
def goal_8_3 : Prop := ∀ j : Fin 31, 11 ≤ j.val → j.val < 15 → predicate j
def goal_8_4 : Prop := ∀ j : Fin 31, 15 ≤ j.val → j.val < 19 → predicate j
def goal_8_5 : Prop := ∀ j : Fin 31, 19 ≤ j.val → j.val < 23 → predicate j
def goal_8_6 : Prop := ∀ j : Fin 31, 23 ≤ j.val → j.val < 27 → predicate j
def goal_8_7 : Prop := ∀ j : Fin 31, 27 ≤ j.val → j.val < 31 → predicate j
theorem merge_8 (p0 : goal_8_0) (p1 : goal_8_1) (p2 : goal_8_2) (p3 : goal_8_3) (p4 : goal_8_4) (p5 : goal_8_5) (p6 : goal_8_6) (p7 : goal_8_7) : rootGoal := by
  intro j
  have hj := j.isLt
  by_cases h0 : j.val < 3
  · exact p0 j (Nat.zero_le _) h0
  by_cases h1 : j.val < 7
  · exact p1 j (Nat.le_of_not_lt h0) h1
  by_cases h2 : j.val < 11
  · exact p2 j (Nat.le_of_not_lt h1) h2
  by_cases h3 : j.val < 15
  · exact p3 j (Nat.le_of_not_lt h2) h3
  by_cases h4 : j.val < 19
  · exact p4 j (Nat.le_of_not_lt h3) h4
  by_cases h5 : j.val < 23
  · exact p5 j (Nat.le_of_not_lt h4) h5
  by_cases h6 : j.val < 27
  · exact p6 j (Nat.le_of_not_lt h5) h6
  exact p7 j (Nat.le_of_not_lt h6) hj
end MEnvelopeBase
