class ManagementServersController < ApplicationController

  # GET /management_servers/1/edit
  def edit
    @management_server = ManagementServer.find(params[:id])
  end

  # PUT /management_servers/1
  # PUT /management_servers/1.json
  def update
    @management_server = ManagementServer.find(params[:id])

    respond_to do |format|
      if @management_server.update_attributes(params[:management_server])
        format.html { redirect_to edit_management_server_path(@management_server), notice: 'Management server was successfully updated.' }
        format.json { head :ok }
      else
        format.html { render action: "edit" }
        format.json { render json: @management_server.errors, status: :unprocessable_entity }
      end
    end
  end

end
