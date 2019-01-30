class Package < ActiveRecord::Base
  belongs_to :software
  belongs_to :deploy_state
  has_many :machine_packages, :class_name => 'MachinePackage'
  has_many :fs, :order => 'sn'
  has_and_belongs_to_many :machines
  
  def deploy_logs
    ret = []
    machine_packages.each do |a|
      ret.push(a.deploy_logs)
    end
    ret.flatten
  end

  def deployed_logs
    ret = []
    deploy_logs.each do |log|
      if log.machine_deploy_state_id != MachineDeployState::PREPARE
        ret.push log
      end
    end
    ret
  end
  
  def conf_filename
    Rails.root.to_s + '/softwares/' + software.name + '/' + version.to_s + '/config.yml' 
  end
  
  def create_conf

    software_path = Rails.root.to_s + '/softwares/' + software.name 
    version_path = software_path + '/' + version.to_s 
    
    unless File.exists?(software_path)
      Dir.mkdir(software_path)
    end
    
    unless File.exists?(version_path)
      Dir.mkdir(version_path)
    end

    filename = version_path + '/config.yml'
    h = Hash.new
    h[:name] = software.name
    h[:description] = software.description
    h[:scope] = software.scope
    h[:check_type] = software.check_type.name
    h[:check_value] = software.check_value
    h[:groups] = software.groups
    h[:users] =  software.users
    h[:start_command] = software.start_command
    h[:stop_command] = software.stop_command
    h[:version] = version
    file_arr = []
    h[:files] = file_arr

    fs.each do |f|
      tmp_h = {}
      tmp_h['sn'] = f.sn
      tmp_h['name'] = f.name
      tmp_h['destine'] = f.destine
      tmp_h['md5sum'] = f.md5sum
      tmp_h['content_type'] = f.content_type
      file_arr.push(tmp_h)
    end
      
    file = File.new(filename, 'w+')
    file.write(h.to_yaml)
    file.close
  end
  
  def create_logs
    exist_ips = {}
    Machine.all.each do |x|
      exist_ips[x.ip] = x.id
    end
    
    orgin_ips = []
    deploy_logs.each do |x|
      orgin_ips.push x.machine.ip
    end
        
    software.ips.each do | ip |
      unless orgin_ips.include?(ip)
        DeployLog.create :machine_id => exist_ips[ip], :package_id => id, :machine_deploy_state_id => 8
      end
    end
  end
  
end
