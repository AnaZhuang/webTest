#!/home/clouder/programs/ruby/bin/ruby
require 'socket'
require 'digest/sha1'

addr = ['<broadcast>', 33333]
UDPSock = UDPSocket.new
UDPSock.setsockopt(Socket::SOL_SOCKET, Socket::SO_BROADCAST, true)
data = Digest::SHA1.hexdigest(Time.now.strftime('%Y%m%d%H') + 'clear')  
UDPSock.send(data, 0, addr[0], addr[1])
UDPSock.close