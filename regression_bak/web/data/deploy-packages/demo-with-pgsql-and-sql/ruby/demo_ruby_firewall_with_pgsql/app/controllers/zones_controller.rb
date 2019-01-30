class ZonesController < ApplicationController
  # GET /zones
  # GET /zones.json
  def index
    @zones = Zone.all

    respond_to do |format|
      format.html # index.html.erb
      format.json { render json: @zones }
    end
  end

  # GET /zones/new
  # GET /zones/new.json
  def new
    @zone = Zone.new

    respond_to do |format|
      format.html # new.html.erb
      format.json { render json: @zone }
    end
  end

  # GET /zones/1/edit
  def edit
    @zone = Zone.find(params[:id])
  end

  # POST /zones
  # POST /zones.json
  def create
    @zone = Zone.new(params[:zone])

    respond_to do |format|
      if @zone.save
        format.html { redirect_to zones_url, notice: 'Zone was successfully created.' }
        format.json { render json: @zone, status: :created, location: @zone }
      else
        format.html { render action: "new" }
        format.json { render json: @zone.errors, status: :unprocessable_entity }
      end
    end
  end

  # PUT /zones/1
  # PUT /zones/1.json
  def update
    @zone = Zone.find(params[:id])

    respond_to do |format|
      if @zone.update_attributes(params[:zone])
        format.html { redirect_to zones_url, notice: 'Zone was successfully updated.' }
        format.json { head :ok }
      else
        format.html { render action: "edit" }
        format.json { render json: @zone.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /zones/1
  # DELETE /zones/1.json
  def destroy
    @zone = Zone.find(params[:id])
    @zone.destroy

    respond_to do |format|
      format.html { redirect_to zones_url }
      format.json { head :ok }
    end
  end

  def download
    send_file generate_firewall(params[:id])
  end
  
  def deploy
    @zone = Zone.find params[:id]
    file = generate_firewall(params[:id])
    deploy_file(@zone, file, 'deploy')
    
    redirect_to zone_batches_url(@zone)
  end

  def clear
    @zone = Zone.find params[:id]
    file = File.dirname(__FILE__) + "/../views/rulesets/empty.sh"
    deploy_file(@zone, file, 'clear')
    
    redirect_to zone_batches_url(@zone)
  end  

  private
  def deploy_file(zone, file, desc)
    batch = nil
    success_ips = []
    
    threads = []
    Check.get_real_ips(zone.value).each do |ip|
      unless batch
        batch = Batch.new
        batch.zone = zone
        batch.desc = desc
        batch.save 
      end 
      
      t = Thread.new do
        begin
          Net::SCP.start(ip, "clouder", :password => "engine") do |scp|
            scp.upload! file, "/home/clouder/vs/program/monitor_firewall/rc.firewall.sh"      
          end
          success_ips.push [ip, true]
        rescue
          logger.error("#{$!} at:#{$@}")
          success_ips.push [ip, false]
        end
      end
      threads.push(t)  
    end
    
    threads.each do |t|
      t.join
    end
    
    puts file
    success_ips.each do |arr|
      Log.create :batch_id => batch.id, :ip => arr.first, :success => arr.last
    end
  end
  
  def generate_firewall(id_str)
    @zone = Zone.find id_str
    @admin_ip = ManagementServer.all.first.ip
    @from_rulesets = Ruleset.all :conditions => ['from_id = ?', id_str.to_i], :order => 'to_id desc' 
    @to_rulesets = Ruleset.all :conditions => ['to_id = ?', id_str.to_i], :order => 'from_id desc'
    
    f = File.open(File.dirname(__FILE__) + "/../views/rulesets/rc.firewall.erb", 'r')
    r = ERB.new(f.read, 0, '%<>')
    f.close
    out = File.open(File.dirname(__FILE__) + "/../../tmp/#{@zone.name}_rc.firewall", "w+")
    out.write(r.result(binding))
    out.close
    
    File.dirname(__FILE__) + "/../../tmp/#{@zone.name}_rc.firewall"
  end
  
end
