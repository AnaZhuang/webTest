class Batch < ActiveRecord::Base
  belongs_to :zone
  has_many :logs, :order => 'id desc'
  has_many :success_logs, :class_name => 'Log', :conditions => ['success = ?', true]
  has_many :fail_logs, :class_name => 'Log', :conditions => ['success = ?', false]
end
