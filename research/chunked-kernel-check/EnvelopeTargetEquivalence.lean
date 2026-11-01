import EnvelopeBase
open OAI.AtomicTriangular.FiniteCertificate
set_option maxHeartbeats 200000
theorem MEnvelopeTargetEquality :
  MEnvelopeBase.rootGoal = (∀ j : Fin 31,
    (OAI.AtomicTriangular.Interval.CI.ofReal
      (((envelopePhase01 j).re.neg).neg.mul
        (OAI.AtomicTriangular.Interval.RI.point 16))).exp.re = envelopeExpB16 j) := rfl
