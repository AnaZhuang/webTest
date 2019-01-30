class MachineDeployState < ActiveRecord::Base
  START = 1
  UPLOAD = 2
  MD5CHK = 3
  INSTALLING = 4
  SUCCESS = 5
  CHECK = 6
  TIMEOUT = 7
  FAIL = 8
  PREPARE = 9
end
