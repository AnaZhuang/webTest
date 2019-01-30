class LogsController < ApplicationController
  # GET /logs
  # GET /logs.json
  def index
    @batch = Batch.find params[:batch_id]
    @logs = @batch.logs

    respond_to do |format|
      format.html # index.html.erb
      format.json { render json: @logs }
    end
  end

end
