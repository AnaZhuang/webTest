class FsController < ApplicationController
  before_filter :fetch_package
  
  # GET /fs
  # GET /fs.json
  def index
    @fs = @package.fs
    @f = F.new
  end
  
  def show
    @f = F.find params[:id]
    if @f
      filename = version_path + '/' + @f.name
      
      if File.exists?(filename)
        send_file filename, :type => @f.content_type
      else
        render :text => 'no this file' 
      end
    else
      render :text => 'no this file object'
    end
  end
  
  # POST /fs
  # POST /fs.json
  def create
    @f = F.new
    original_filename = params['upload'].original_filename 
    
    unless File.exists?(software_path)
      Dir.mkdir(software_path)
    end
    
    unless File.exists?(version_path)
      Dir.mkdir(version_path)
    end
    
    filename = version_path + '/' + original_filename
    file_object = File.open(filename, 'wb+')     
    file_object.write(params['upload'].read)
    file_object.close
    
    md5sum = Digest::MD5.file(filename).hexdigest
    
    @f.sn = @package.fs.size + 1
    @f.name = original_filename
    @f.content_type = params['upload'].content_type.chomp
    @f.package_id = @package.id
    @f.md5sum = md5sum
    @f.save

    redirect_to software_package_fs_path(@software, @package) 
  end

  # PUT /fs/1
  # PUT /fs/1.json
  def update
    @f = F.find(params[:id])

    respond_to do |format|
      if @f.update_attributes(params[:f])
        format.html { redirect_to software_package_fs_path(@software, @package) }
        format.js
        format.json { head :ok }
      else
        format.html { redirect_to software_package_fs_path(@software, @package) }
        format.js
        format.json { render json: @package.errors, status: :unprocessable_entity }
      end
    end
     
  end

  # DELETE /fs/1
  # DELETE /fs/1.json
  def destroy
    @f = F.find(params[:id])
    if @f
      filename = version_path + '/' + @f.name
      if File.exists?(filename)
        puts "delete #{filename}"
        puts File.delete(filename)
      end
      
      #if not delete last file, must reorder all file sn 
      if @f.sn != @package.fs.size
        @package.fs.each do |x|
          if x.sn > @f.sn
            x.sn -= 1
            x.save
          end
        end
      end
      
      @f.destroy
    end
    
    redirect_to software_package_fs_path(@software, @package) 
  end
  
  def up
    @f = F.find(params[:id])
    if @f && @f.sn > 1
      F.transaction do 
        pre = @f.pre
        pre.sn += 1
        @f.sn -= 1
        pre.save
        @f.save 
      end
    end
    redirect_to software_package_fs_path(@software, @package) 
  end
  
  def down
    @f = F.find(params[:id])
    if @f && @f.sn < @package.fs.size
      F.transaction do 
        succ = @f.succ
        succ.sn -= 1
        @f.sn += 1
        succ.save
        @f.save 
      end
    end

    redirect_to software_package_fs_path(@software, @package) 
  end
  
  protected
  def fetch_package
    @software = Software.find params[:software_id]
    @package = Package.find params[:package_id]
  end
  
  def software_path 
    Rails.root.to_s + '/softwares/' + @software.name
  end
  
  def version_path 
    Rails.root.to_s + '/softwares/' + @software.name + '/' + @package.version.to_s
  end
end
