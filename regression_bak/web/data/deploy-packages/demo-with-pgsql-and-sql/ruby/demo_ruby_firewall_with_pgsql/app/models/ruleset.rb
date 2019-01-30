class Ruleset < ActiveRecord::Base
  validates_presence_of :from_id, :to_id
  has_many :rules
  has_many :protocols, :through => :rules
  belongs_to :from, :class_name => 'Zone'
  belongs_to :to, :class_name => 'Zone'
  
  def from_ips_str
    if from.value == 'any'
      ''
    else
      "-s #{from.value}"
    end
  end
  
  def to_ips_str
    if to.value == 'any'
      ''
    else
      "-d #{to.value}"
    end
  end
end
