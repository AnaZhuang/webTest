class DeployState < ActiveRecord::Base
  UNDEPLOY = 1
  PREPARING = 2
  DEPLOYING = 3
  FINISHED = 4
end
