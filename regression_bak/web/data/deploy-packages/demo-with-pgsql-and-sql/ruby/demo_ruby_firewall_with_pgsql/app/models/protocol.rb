class Protocol < ActiveRecord::Base
  validates_presence_of :name, :ports
  validates_presence_of :tcp, :udp, :unless => "tcp || udp", :message => "must select a protocol"
  validates_uniqueness_of :name
  
  validates_each :ports do |model, attr, value|
    #first check value is composed by number or , or :
    if value =~ /^[:|,|[0-9]]+$/
      value.split(',').each do |x|
        if x.include?(':')
          nums = x.split(':')
          if nums.size == 2
            first = nums.first.to_i
            second = nums.last.to_i
            if first < 1 || second > 65535
              model.errors[:ports] << "with ':' < 1 or > 65535"
            elsif first >= second  
              model.errors[:ports] << "with ':' first must less than second"
            end
          else
            model.errors[:ports] << "one port can only have a ':'"
          end 
        else
          if x.to_i < 1 || x.to_i > 65535
            model.errors[:ports] << "the port < 1 or > 65535"
          end
        end
      end
    else
      model.errors.add(attr, "must be composed by number or ',' or ':'")
    end
  end
  
  def type
    val = ''
    if tcp?
      val += 'tcp,'
    end
    if udp?
      val += 'udp,'
    end
    val[0..val.size - 2]
  end
end
