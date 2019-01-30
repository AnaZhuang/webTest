class DeployBatchesController < ApplicationController
  before_filter :fetch_software

  # GET /deploy_batches
  # GET /deploy_batches.json
  def index
    @deploy_batches = @software.deploy_batches

    respond_to do |format|
      format.html # index.html.erb
      format.json { render json: @deploy_batches }
    end
  end

  protected
  def fetch_software
    @software = Software.find params[:software_id]
  end
end
