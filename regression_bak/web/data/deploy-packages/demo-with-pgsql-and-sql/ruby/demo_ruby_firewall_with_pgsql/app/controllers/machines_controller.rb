class MachinesController < ApplicationController

  def index
    @machines = Machine.all

    respond_to do |format|
      format.html # index.html.erb
      format.json { render json: @machines }
    end
  end

end
