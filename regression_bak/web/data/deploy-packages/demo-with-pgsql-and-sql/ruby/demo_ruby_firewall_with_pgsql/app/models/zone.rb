class Zone < ActiveRecord::Base
  validates_presence_of :name, :value
  validates_uniqueness_of :name
  has_many :from_rulesets, :class_name => 'Ruleset', :foreign_key => :to_id 
  has_many :to_rulesets, :class_name => 'Ruleset', :foreign_key => :from_id 
  has_many :batches, :order => 'id desc'

  validates_each :value do |model, attr, value|
    #first check value is composed by number or , or .
    if value != 'any'
      if value =~ /^[\/||\.|,|[0-9]]+$/
        value.split(',').each do |x|
          if !MineRegexp.ip?(x) && !MineRegexp.cidr?(x)
            model.errors.add(attr, "must be ip or cidr format")
          end
        end
      else
        model.errors.add(attr, "must be composed by number or ',' or '.'")
      end
    end
  end
    
  after_create do |it|
    zones = Zone.where("id <> #{it.id}")
    zones.each do |x|
      Ruleset.create :from_id => id, :to_id => x.id
      Ruleset.create :from_id => x.id, :to_id => id
    end
  end
  
  after_destroy do |it|
    Ruleset.delete("from_id = #{it.id} || to_id = #{it.id}")        
  end
  
  def local_ports
    if name == 'internet'
      '1024:65535'
    else
      '32768:61000'
    end
  end
end
