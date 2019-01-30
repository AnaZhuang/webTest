class F < ActiveRecord::Base
  belongs_to :package
  
  def pre
    F.find :first, :conditions => ['package_id = ? and sn = ?', package_id, sn-1]
  end
  
  def succ
    F.find :first, :conditions => ['package_id = ? and sn = ?', package_id, sn+1]
  end
end
