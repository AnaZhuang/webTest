class DeployLog < ActiveRecord::Base
  belongs_to :machine_package, :class_name => 'MachinePackage', :foreign_key => 'machine_package_id'
  belongs_to :deploy_batch
  belongs_to :deploy_error
  belongs_to :machine_deploy_state
end