class PackagesController < ApplicationController

  before_filter :fetch_software

  # GET /packages
  # GET /packages.json
  def index
    @packages = @software.packages
  end

  # GET /packages/1
  # GET /packages/1.json
  def show
    @package = Package.find(params[:id])
  end

  # POST /packages
  # POST /packages.json
  def create
    @package = Package.new(params[:package])
    @package.software = @software
    if @software.last_version    
      @package.version = @software.last_version + 1
    else
      @package.version = 1
    end
    
    @package.save
    redirect_to software_packages_path(@software)
  end

  # PUT /packages/1
  # PUT /packages/1.json
  def update
    @package = Package.find(params[:id])

    respond_to do |format|
      if @package.update_attributes(params[:package])
        format.html { redirect_to @package, notice: 'Package was successfully updated.' }
        format.json { head :ok }
      else
        format.html { render action: "edit" }
        format.json { render json: @package.errors, status: :unprocessable_entity }
      end
    end
  end

  def conf
    @package = Package.find(params[:id])
    
    if @package.deploy_state_id == 1
      @package.create_conf
    end
    
    send_file @package.conf_filename
  end

  # DELETE /packages/1
  # DELETE /packages/1.json
  def destroy
    @package = Package.find(params[:id])
    @package.destroy
    
    @package.deploy_logs.each do |log|
      if log.machine_deploy_state_id != MachineDeployState::PREPARE
        log.destroy
      end
    end
       
    F.delete_all(['package_id = ?', @package.id])
    
    redirect_to software_packages_path(@software) 
  end
  
  def publish
    package = Package.find(params[:id])
    package.publish = true
    package.save
    
    redirect_to software_packages_path(@software) 
  end
  
  def unpublish
    package = Package.find(params[:id])
    package.publish = false
    package.save
    
    redirect_to software_packages_path(@software) 
  end

  protected
  def fetch_software
    @software = Software.find params[:software_id]
  end
end
