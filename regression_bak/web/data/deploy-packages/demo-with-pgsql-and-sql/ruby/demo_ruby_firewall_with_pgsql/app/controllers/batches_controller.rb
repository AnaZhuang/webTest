class BatchesController < ApplicationController
  
  before_filter :fetch_zone
  
  # GET /batches
  # GET /batches.json
  def index
    @batches = @zone.batches

    respond_to do |format|
      format.html # index.html.erb
      format.json { render json: @batches }
    end
  end

  protected
  def fetch_zone
    @zone = Zone.find params[:zone_id]
  end

end
