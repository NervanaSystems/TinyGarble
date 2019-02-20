add_library(tiny_garble SHARED
  ../crypto/BN.cpp
  ../crypto/OT.cpp
  ../crypto/OT_extension.cpp
  ../garbled_circuit/garbled_circuit.cpp
  ../garbled_circuit/garbled_circuit_util.cpp
  ../garbled_circuit/garbled_circuit_high_mem.cpp
  ../garbled_circuit/garbled_circuit_low_mem.cpp
  ../garbled_circuit/garbled_circuit_testing.cpp
  ../scd/scd.cpp
  ../scd/v_2_scd.cpp
  ../scd/scd_evaluator.cpp
  ../scd/scheduling.cpp
  ../tcpip/tcpip.cpp
  ../tcpip/tcpip_testsuit.cpp
  ../util/util.cpp
  ../util/log.cpp
)