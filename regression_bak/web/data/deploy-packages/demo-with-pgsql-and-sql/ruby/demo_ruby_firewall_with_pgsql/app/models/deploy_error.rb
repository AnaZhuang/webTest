class DeployError < ActiveRecord::Base
  SUCCESS = 1
  REFUSE = 2
  SSH_TIMEOUT = 3
  MD5CHK = 4
  SETUP = 5
  ALREADY_INSTALLED = 6
  CHECK = 7
  TIMEOUT = 8
  UNKNOWN = 9
end
