import EnvelopeBase
set_option maxHeartbeats 2000000
example : Decidable (∀ j : Fin 31, MEnvelopeBase.predicate j) := inferInstance
example : Decidable (∀ j : Fin 31, 0 ≤ j.val → j.val < 31 → MEnvelopeBase.predicate j) := inferInstance
example : Decidable (∀ j : Fin 31, 0 ≤ j.val → j.val < 15 → MEnvelopeBase.predicate j) := inferInstance
example : Decidable (∀ j : Fin 31, 15 ≤ j.val → j.val < 31 → MEnvelopeBase.predicate j) := inferInstance
example : Decidable (∀ j : Fin 31, 0 ≤ j.val → j.val < 7 → MEnvelopeBase.predicate j) := inferInstance
example : Decidable (∀ j : Fin 31, 7 ≤ j.val → j.val < 15 → MEnvelopeBase.predicate j) := inferInstance
example : Decidable (∀ j : Fin 31, 15 ≤ j.val → j.val < 23 → MEnvelopeBase.predicate j) := inferInstance
example : Decidable (∀ j : Fin 31, 23 ≤ j.val → j.val < 31 → MEnvelopeBase.predicate j) := inferInstance
example : Decidable (∀ j : Fin 31, 0 ≤ j.val → j.val < 3 → MEnvelopeBase.predicate j) := inferInstance
example : Decidable (∀ j : Fin 31, 3 ≤ j.val → j.val < 7 → MEnvelopeBase.predicate j) := inferInstance
example : Decidable (∀ j : Fin 31, 7 ≤ j.val → j.val < 11 → MEnvelopeBase.predicate j) := inferInstance
example : Decidable (∀ j : Fin 31, 11 ≤ j.val → j.val < 15 → MEnvelopeBase.predicate j) := inferInstance
example : Decidable (∀ j : Fin 31, 15 ≤ j.val → j.val < 19 → MEnvelopeBase.predicate j) := inferInstance
example : Decidable (∀ j : Fin 31, 19 ≤ j.val → j.val < 23 → MEnvelopeBase.predicate j) := inferInstance
example : Decidable (∀ j : Fin 31, 23 ≤ j.val → j.val < 27 → MEnvelopeBase.predicate j) := inferInstance
example : Decidable (∀ j : Fin 31, 27 ≤ j.val → j.val < 31 → MEnvelopeBase.predicate j) := inferInstance
