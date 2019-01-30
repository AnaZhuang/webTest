class Machine < ActiveRecord::Base
  has_and_belongs_to_many :packages
  has_many :machine_packages, :class_name => 'MachinePackage', :order => 'id desc'  
  
  def softwares
    ret = {}
    machine_packages.each do |m|
      software_name = m.software.name
      unless ret.has_key?(software_name)
        if m.installed?
          ret[software_name] = m.package.version 
        end
      end
    end
    ret
  end
  
  def softwares_str
    arr = []
    softwares.each do |key, val|
      arr.push(key + ':' + val.to_s)
    end
    arr.join(',')
  end
  
  def self.create_all(ips)
    exist_ips = []
    Machine.all.each do |x|
      exist_ips.push x.ip
    end
    
    the_id = 0
    ips.each do | ip |
      unless exist_ips.include?(ip)
        a = Machine.new
        a.ip = ip
        a.save
      end
    end
  end
  
  def last_deploy_version(software_id)
    machine_package = MachinePackage.find :first, 
      :conditions => ['software_id = ? and machine_id = ? and installed = ?', software_id, self.id, true], 
      :order => 'package_id desc'
    
    if machine_package
      machine_package.package.version
    else
      0
    end
  end
end
