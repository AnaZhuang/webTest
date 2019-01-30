#!/home/clouder/programs/ruby/bin/ruby

# Author: ly

# it's local monitor iptable service
# man function is in loop
# once SLEEP_TIME seconds, it check if newer configuration file
# and load new configration file

require 'yaml'

SLEEP_TIME = 10
SHELL_FILE = '/home/clouder/vs/program/monitor_firewall/rc.firewall.sh'
CLEAR_FILE = '/home/clouder/vs/program/monitor_firewall/clear_firewall.sh'
INIT_FILE = '/home/clouder/vs/program/monitor_firewall/init_firewall.sh'

# save last configuration file modified time
LAST_TIME_FILE = '/home/clouder/vs/program/monitor_firewall/last_time'

conf = {}

# if not exist 'last_time', then create last_time
# and let last modified time from now substract one day
# this can let first installing software can load configuration file
# before less than one day 
unless File.exist?(LAST_TIME_FILE)
  conf['last_modified_at'] = Time.now - 60*60*24 
  f = File.new(LAST_TIME_FILE, 'w')
  f.write(conf.to_yaml)
  f.close
end

conf = YAML::load_file(LAST_TIME_FILE)

# if shell first excute, must load firewall once
# so subtract last_modified_at 1 second
conf['last_modified_at'] -= 1

while true do
  
  if File.exist?(SHELL_FILE)	
    modified_at = File.mtime(SHELL_FILE)
    if modified_at > conf['last_modified_at']
# if SHEEL FILE empty, then clear firewall rulesets
# allow all visits      
      if File.size(SHELL_FILE) == 0
        system CLEAR_FILE
      else
        system INIT_FILE 
        system "chmod +x #{SHELL_FILE}"
        if system SHELL_FILE
          puts "execute #{SHELL_FILE} success"
          conf['last_modified_at'] = modified_at 
          f = File.new(LAST_TIME_FILE, 'w')
          f.write(conf.to_yaml)
          f.close
        else
          puts "execute #{SHELL_FILE} fail"
        end
      end 
    end
  end
  
  puts 'sleep...............'
  sleep(SLEEP_TIME) 
end
