class MachinePackage < ActiveRecord::Base
  set_table_name 'machines_packages'
  belongs_to :machine
  belongs_to :package
  belongs_to :software
  has_many :deploy_logs, :order => 'id desc'
end
