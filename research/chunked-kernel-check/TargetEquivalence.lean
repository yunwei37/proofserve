import ChunkBase
import OAI.Analysis.PlanarPacking.Grid
set_option maxHeartbeats 200000
set_option maxRecDepth 10000
open OAI.SharpPlanar.IntegerIntervals
theorem extracted_input_exact :
    ChunkBase.p0_0 = OAI.SharpPlanar.IntegerGrid.p0_0 := by rfl
theorem extracted_goal_exact :
    ChunkBase.rootGoal ↔
      (PointBox.calc OAI.SharpPlanar.IntegerGrid.p0_0.t =
        OAI.SharpPlanar.IntegerGrid.p0_0) := by rfl
#print axioms extracted_input_exact
#print axioms extracted_goal_exact
