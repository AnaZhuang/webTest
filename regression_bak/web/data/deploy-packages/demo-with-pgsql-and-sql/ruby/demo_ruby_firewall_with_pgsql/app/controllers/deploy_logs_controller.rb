class DeployLogsController < ApplicationController
  before_filter :fetch_deploy_batch
  
  # GET /deploy_logs
  # GET /deploy_logs.json
  def index
    @deploy_logs = @deploy_batch.deploy_logs

    respond_to do |format|
      format.html # index.html.erb
      format.json { render json: @deploy_logs }
    end
  end
  
  def update_state
    deploy_log_h = {}
    
    @deploy_batch.deploy_logs.each do |x|
      deploy_log_h[x.id] = x
    end
    updated_vals = []
    
    vals = params[:value].split(';')
    
    vals.each do |x|
      val = x.split(',')
      deploy_log = deploy_log_h[val[0].to_i]
      state = deploy_log.machine_deploy_state_id.nil? ? 0 : deploy_log.machine_deploy_state_id 
      error = deploy_log.deploy_error_id.nil? ? 0 : deploy_log.deploy_error_id
      cause = deploy_log.cause.nil? ? '' : deploy_log.cause

      if deploy_log && (val[1].to_i != state || val[2].to_i != error)
        updated_vals.push ({:id => deploy_log.id, :state => state, :error => error, :cause => deploy_log.cause })  
      end       
    end
    
    render :json => updated_vals.to_json
  end
  
  protected
  def fetch_deploy_batch
    @software = Software.find params[:software_id]
    @deploy_batch = DeployBatch.find params[:deploy_batch_id]
  end
end
