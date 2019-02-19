add_library(tiny_garble SHARED
  ../crypto/BN.cpp
  ../crypto/OT.cpp
  ../crypto/OT_extension.cpp
  ../garbled_circuit/garbled_circuit.cpp
  ../garbled_circuit/garbled_ciruit_util.cpp
  ../garbled_circuit/garbled_circuit_high_mem.cpp
  ../garbled_circuit/garbled_circuit_low_mem.cpp
  ../scd/scd.cpp
  ../tcpip/tcpip.cpp
  ../util/util.cpp
  ../util/log.cpp
)

if (OPENSSL_FOUND)
  target_link_libraries(tiny_garble ${OPENSSL_LIBRARIES})
endif (OPENSSL_FOUND)
if (Boost_FOUND)
  target_link_libraries(tiny_garble ${Boost_LIBRARIES})
endif (Boost_FOUND)