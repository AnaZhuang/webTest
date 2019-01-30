class Software < ActiveRecord::Base
  validates_presence_of :name, :scope, :check_type_id
  validates_uniqueness_of :name

  has_many :packages
  has_many :publish_packages, :class_name => 'Package', :conditions => ['publish = ?', true], :order => 'version'
  has_many :deploy_batches, :order => 'id desc'
  has_many :deploying_batches, :class_name => 'DeployBatch', :conditions => ['state <> ?', DeployBatch::FINISHED]  
  has_many :deployed_machine_packages, :class_name => 'MachinePackage', :conditions => ['installed = ?', true]
      
  belongs_to :check_type
  
  def deployed_num
    ret = 0
    if publish_packages.size > 0
      package = publish_packages.last
      mps = MachinePackage.all(:conditions => ['package_id = ? and installed = ?', package.id, true])
      mps.each do |mp|
        if ips.include?(mp.machine.ip)
          ret += 1
        end
      end
    end
    ret
  end
  
  def undeployed_num
    ips.size - deployed_num
  end
  
  def last_version
    Package.maximum('version', :conditions => ['software_id = ?', id])
  end

  def last_package
    Package.find :first, :conditions => ['software_id = ?', id], :order => 'version desc'  
  end
  
  def machines
    Machine.find :all, :conditions => ["ip in ('#{self.ips.join("','")}')"]
  end
  
  def ips
    all = []
    scope.split(',').each do |s|
      if MineRegexp.ip?(s)
        unless all.include?(s)
          all.push s
        end
      else
        vals = s.split('.')
        ip_header = vals[0] + '.' + vals[1] + '.' + vals[2]
        
        range = Range.new(vals[3].to_i, vals[5].to_i)
        range.each do |x|
          ip = ip_header + '.' + x.to_s
          unless all.include?(ip)
            all.push ip
          end
        end 
      end
    end
    all
  end

  validates_each :scope do |model, attr, value|
    #first check value is composed by number or , or .
    if value =~ /^[\.|,|[0-9]]+$/
      value.split(',').each do |x|
        if !MineRegexp.ip?(x)
          strs = x.split('..')
          if strs.size != 2
            model.errors.add(attr, "must be ip or ip range format")
          else
            if !MineRegexp.ip?(strs.first)
              model.errors.add(attr, "must be ip range format")
            else
              if strs.last !~ /^[0-9]+$/
                model.errors.add(attr, "must be ip range format")
              else
                ip_vals = strs.first.split('.')
                if ip_vals.last.to_i >= strs.last.to_i
                  model.errors.add(attr, "must be ip range format")
                end
              end 
            end
          end
        end
      end
    else
      model.errors.add(attr, "must be composed of number or ',' or '.'")
    end
  end

  def conf_filename
    Rails.root.to_s + '/softwares/' + self.name + '/deploy.yml' 
  end
  
  def export_filename
    Rails.root.to_s + '/softwares/' + self.name + '.zip' 
  end
  
  def create_export_file
    `cd '#{Rails.root.to_s + '/softwares'}'; zip -r #{self.name + '.zip'} #{self.name}`
  end
  
  def import_file
    software_dir = Rails.root.to_s + '/softwares/' + self.name
    FileUtils.rm_r(software_dir)
    `cd '#{Rails.root.to_s + '/softwares'}'; unzip #{self.name}.zip`
    
    #update software
    h = YAML::load_file(conf_filename)
    h['scope'] = self.scope
    file = File.new(conf_filename, 'w+')
    file.write(h.to_yaml)
    file.close
    
    check_type = CheckType.find_by_name(h['check_type'])
    self.check_type_id = check_type.id
    self.check_value = h['check_value']
    self.groups = h['groups'] 
    self.users = h['users']
    self.description = h['description']
    self.start_command = h['start_command']
    self.stop_command = h['stop_command']
    self.save
    
    #update package and files
    h['packages'].each do |package_h|
      version = package_h.keys.first
      package = Package.find :first, :conditions => ['version = ? and software_id = ?', version, self.id]
      if package
        package.fs.clear
      else
        package = Package.new
        package.software_id = self.id
        package.version = version
      end
      package_h[version].each do |f_h|
        f = F.new
        f.sn = f_h['sn']
        f.name = f_h['name']
        f.destine = f_h['destine']
        f.md5sum = f_h['md5sum']
        f.content_type = f_h['content_type']
        f.save
        package.fs.push(f)
      end
      package.save
    end
  end  
  
  def create_conf
    software_path = Rails.root.to_s + '/softwares/' + self.name 
    
    unless File.exists?(software_path)
      Dir.mkdir(software_path)
    end
    filename = conf_filename

    h = Hash.new
    h['name'] = self.name
    h['description'] = self.description
    h['scope'] = self.scope
    h['check_type'] = self.check_type.name
    h['check_value'] = self.check_value
    h['groups'] = self.groups
    h['users'] =  self.users
    h['start_command'] = self.start_command
    h['stop_command'] = self.stop_command
    packages = []
    h['packages'] = packages
    
    publish_packages.each do |package|
      package_h = {}
      file_arr = Array.new
      package_h[package.version] = file_arr
      
      package.fs.each do |f|
        tmp_h = {}
        tmp_h['sn'] = f.sn
        tmp_h['name'] = f.name
        tmp_h['destine'] = f.destine
        tmp_h['md5sum'] = f.md5sum
        tmp_h['content_type'] = f.content_type
        file_arr.push(tmp_h)
      end
      
      packages.push(package_h)
    end
      
    file = File.new(filename, 'w+')
    file.write(h.to_yaml)
    file.close
  end
end
