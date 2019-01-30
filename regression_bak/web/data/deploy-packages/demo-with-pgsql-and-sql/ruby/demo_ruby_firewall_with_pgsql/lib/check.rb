require 'netaddr'
require 'socket'
require 'timeout'
require 'thread'

TIMEOUT = 3
PORT = 22

class Check
  def self.check(ip, port = PORT)
    ret = false
    begin
      s = timeout(TIMEOUT) { TCPSocket.open(ip, PORT) }
      s.shutdown
      ret = true
    rescue
#      puts "--error: #{$!} at: #{$@}"
    end
    ret
  end
  
  def self.get_all_ips(str)
    ips = []
    str.split(',').each do |x|
      cidr = NetAddr::CIDR.create(x)
      if cidr.size > 1 #netwok
        0.upto(cidr.size - 1) do |i|
          ips.push(cidr[i].ip)
        end
      else #unicast address
        ips.push(cidr[0].ip)
      end
    end

    ips
  end
    
  def self.get_real_ips(str)
    valid_ips = []
    threads = []
    Check.get_all_ips(str).each do |ip|
      t = Thread.new do
        valid_ips.push(ip) if Check.check(ip)
      end
      threads.push(t)  
    end
    
    threads.each do |t|
      t.join
    end
    valid_ips    
  end
end