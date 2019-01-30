#!/home/clouder/programs/ruby192/bin/ruby
require 'socket'
require 'digest/sha1'
require File.dirname(__FILE__) + '/base_service'

CLEAR_FILE = '/home/clouder/vs/program/monitor_firewall/clear_firewall.sh'
addr = ['0.0.0.0', 12346]

BasicSocket.do_not_reverse_lookup = true


class ClearFirewallService < BaseService
end

LOG_FILE = File.dirname(__FILE__) + '/log/clear_firewall.log'
PID_FILE = File.dirname(__FILE__) + '/clear_firewall.pid'

ClearFirewallService.new.run(LOG_FILE, PID_FILE, 0, 0) do |log|
  begin
    # Create socket and bind to address
    udpsock = UDPSocket.new
    udpsock.bind(addr[0], addr[1])

    # if this number is too low it will drop the larger packets and never give them to you    
    data, addr = udpsock.recvfrom(256) 
    log.info "receive #{data}"
    if data == Digest::SHA1.hexdigest(Time.now.strftime('%Y%m%d%H') + 'clear')
      system CLEAR_FILE  
    end
  rescue
    log.error "---error:#{$!} ---at:#{$@}"
  ensure
    udpsock.close
  end
end