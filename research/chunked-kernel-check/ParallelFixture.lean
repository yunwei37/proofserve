import Init
set_option maxHeartbeats 200000
def MQual.a : Nat := 37
def MQual.b : Nat := 41
theorem MQual.pa : MQual.a = 37 := by decide +kernel
theorem MQual.pb : MQual.b = 41 := by decide +kernel
theorem MQual.joined : MQual.a + MQual.b = 78 := by decide +kernel
theorem MQual.closed : (List.range 15).length = 15 := by decide +kernel
