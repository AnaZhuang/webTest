class Rule < ActiveRecord::Base
  belongs_to :ruleset
  belongs_to :protocol
end
