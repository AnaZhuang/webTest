#!/home/clouder/programs/ruby/bin/ruby
require 'socket'
require 'digest/sha1'

CLEAR_FILE = '/home/clouder/vs/program/monitor_firewall/clear_firewall.sh'
addr = ['0.0.0.0', 33333]

BasicSocket.do_not_reverse_lookup = true

# Create socket and bind to address
UDPSock = UDPSocket.new
UDPSock.bind(addr[0], addr[1])

while true

  data, addr = UDPSock.recvfrom(256) # if this number is too low it will drop the larger packets and never give them to you
  puts "receive #{data}"
  if data == Digest::SHA1.hexdigest(Time.now.strftime('%Y%m%d%H') + 'clear')
    system CLEAR_FILE  
  end

end

UDPSock.close
