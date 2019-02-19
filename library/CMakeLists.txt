add_library(tiny_garble
  ../crypto/BN.cpp
  ../crypto/OT.cpp
  ../crypto/OT_extension.cpp
  ../scd/scd.cpp
  ../util/util.cpp
  ../tcpip/tcpip.cpp
  ../util/log.cpp
)

if (OPENSSL_FOUND)
  target_link_libraries(tiny_garble ${OPENSSL_LIBRARIES})
endif (OPENSSL_FOUND)
if (Boost_FOUND)
  target_link_libraries(tiny_garble ${Boost_LIBRARIES})
endif (Boost_FOUND)