class DeployBatch < ActiveRecord::Base
  belongs_to :software
  has_many :deploy_logs, :order => 'id desc'
  PREPARE = 1
  INSTALLING = 2
  FINISHED = 3
  
  def state_name
    if self.state == PREPARE
      'preparing'
    elsif self.state == INSTALLING
      'installing'
    elsif self.state == FINISHED
      'finished'
    else
      'none'
    end
  end
  
  def deploy_name
    log = deploy_logs.first
    if log
      if log.deploy?
        'deploy'
      else
        'undeploy'
      end
    else
      ''
    end
  end
  
  def check_timeout
    conditions_arry = [ 'deploy_batch_id = ? and not machine_deploy_state_id in (?,?,?)', 
      id, MachineDeployState::SUCCESS, MachineDeployState::FAIL, MachineDeployState::TIMEOUT ]
    logs = DeployLog.find :all, :conditions => conditions_arry
       
    logs.each do |log|
      if Time.now - log.upload_file_at > software.timeout
        log.machine_deploy_state_id = MachineDeployState::TIMEOUT
        log.deploy_error_id = DeployError::TIMEOUT
        log.cause = "timeout after #{software.timeout}s"
        log.save
      end
    end
  
    if DeployLog.count(:conditions => conditions_arry) == 0 
      self.state = FINISHED
      self.save
    end
  end

end