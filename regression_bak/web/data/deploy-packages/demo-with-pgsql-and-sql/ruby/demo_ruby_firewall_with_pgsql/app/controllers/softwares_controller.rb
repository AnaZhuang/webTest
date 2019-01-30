class SoftwaresController < ApplicationController
  # GET /softwares
  # GET /softwares.json
  def index
    @softwares = Software.all

    respond_to do |format|
      format.html # index.html.erb
      format.json { render json: @softwares }
    end
  end
  
  def deploy
    @software = Software.find(params[:id])
    batch = nil
    @software.create_conf
    if @software.machines.size > 0 && @software.publish_packages.size > 0 
      @software.publish_packages.each do |package|
        @software.machines.each do |machine|
          mp = MachinePackage.find :first, 
            :conditions => ['package_id = ? and machine_id =?', package.id, machine.id]
          
          if mp.nil?
            mp = MachinePackage.new 
            mp.package_id = package.id
            mp.machine_id = machine.id
            mp.software_id = @software.id
            mp.save
          end
            
          if package.version > machine.last_deploy_version(@software.id)
            log = DeployLog.new
            log.deploy = true
            if batch.nil?
              batch = DeployBatch.new
              batch.software_id = @software.id
              batch.save
            end
            log.deploy_batch_id = batch.id
            log.machine_package_id = mp.id
            log.machine_deploy_state_id = MachineDeployState::PREPARE
            log.save
          end              
        end
      end
    end

    if batch
      redirect_to software_deploy_batch_deploy_logs_url(@software, batch)
    else
      redirect_to softwares_url
    end
  end
  
  def undeploy
    @software = Software.find(params[:id])
    batch = nil 
    
    if @software.machines.size > 0 && @software.publish_packages.size > 0 
      DeployBatch.transaction do 
        @software.machines.each do |machine|
          @software.publish_packages.each do |package|
            mp = MachinePackage.find :first, 
              :conditions => ['package_id = ? and machine_id =?', package.id, machine.id]
            if mp
              if package.version <= machine.last_deploy_version(@software.id)
                log = DeployLog.new
                log.deploy = false
                if batch.nil?
                  batch = DeployBatch.new
                  batch.software_id = @software.id
                  batch.save
                end
                log.deploy_batch_id = batch.id
                log.machine_package_id = mp.id
                log.machine_deploy_state_id = MachineDeployState::PREPARE
                log.save
              end
            end
          end              
        end
      end
    end
    
    if batch
      redirect_to software_deploy_batch_deploy_logs_url(@software, batch)
    else
      redirect_to softwares_url
    end
  end

  # GET /softwares/1
  # GET /softwares/1.json
  def show
    @software = Software.find(params[:id])

    respond_to do |format|
      format.html # show.html.erb
      format.json { render json: @software }
    end
  end

  # GET /softwares/new
  # GET /softwares/new.json
  def new
    @software = Software.new

    respond_to do |format|
      format.html # new.html.erb
      format.json { render json: @software }
    end
  end

  # GET /softwares/1/edit
  def edit
    @software = Software.find(params[:id])
  end

  # POST /softwares
  # POST /softwares.json
  def create
    @software = Software.new(params[:software])

    respond_to do |format|
      if @software.save
        Machine.create_all(@software.ips)
        format.html { redirect_to @software, notice: 'Software was successfully created.' }
        format.json { render json: @software, status: :created, location: @software }
      else
        format.html { render action: "new" }
        format.json { render json: @software.errors, status: :unprocessable_entity }
      end
    end
  end

  # PUT /softwares/1
  # PUT /softwares/1.json
  def update
    @software = Software.find(params[:id])
    old_scope = @software.scope
        
    respond_to do |format|
      if @software.update_attributes(params[:software])
        if old_scope != @software.scope
          Machine.create_all(@software.ips)
        end 
        
        format.html { redirect_to @software, notice: 'Software was successfully updated.' }
        format.json { head :ok }
      else
        format.html { render action: "edit" }
        format.json { render json: @software.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /softwares/1
  # DELETE /softwares/1.json
  def destroy
    @software = Software.find(params[:id])
    @software.destroy

    respond_to do |format|
      format.html { redirect_to softwares_url }
      format.json { head :ok }
    end
  end
  
  def update_error
    software_name = params[:software]
    version = params[:version].to_i
    error_code = params[:error_code].to_i
    error_msg = params[:error_msg]
    ip = request.remote_ip
    
    deploy_log = get_deploylog(software_name, version, ip)
    deploy_log.update_attributes(:deploy_error_id => error_code, :cause => error_msg)
    
    head :ok
  end

  def update_state
    software_name = params[:software]
    version = params[:version].to_i
    state = params[:state].to_i
    ip = request.remote_ip
    
    deploy_log = get_deploylog(software_name, version, ip)
    if deploy_log    
      deploy_log.update_attributes(:machine_deploy_state_id => state)
      if MachineDeployState::SUCCESS == state
        m = deploy_log.machine_package
        if deploy_log.deploy?
          m.installed = true
        else
          m.installed = false
        end
        m.save  
      end
    end
    
    head :ok
  end
  
  def conf
    @software = Software.find(params[:id])
    
    @software.create_conf
    
    send_file @software.conf_filename
  end
  
  def export
    @software = Software.find(params[:id])
    @software.create_export_file
    
    send_file @software.export_filename
  end
  
  def import
    original_filename = params['upload'].original_filename
    software_name = original_filename.split('.').first
    @software = Software.find_by_name(software_name)     
    
    if @software
      filename = Rails.root.to_s + '/softwares/' + original_filename
      file_object = File.open(filename, 'wb+')     
      file_object.write(params['upload'].read)
      file_object.close
    
      @software.import_file
    else
      flash[:notice] = "not exist software:#{software_name}"
    end    
    redirect_to softwares_url
  end
  
  private
  def get_deploylog(software_name, version, remote_ip)
    ret = nil
    machine = Machine.find_by_ip(remote_ip)
    software = Software.find_by_name(software_name)
    package = Package.find :first, :conditions => ['software_id = ? and version = ?', software.id, version]
    p machine
    p software
    p package
    if !machine.nil? && !software.nil? && !package.nil?
      machine_package = MachinePackage.find :first, 
        :conditions => ['machine_id = ? and package_id = ?', machine.id, package.id]
      if machine_package
        ret = machine_package.deploy_logs.first
      end
    end
    ret
  end  
end
