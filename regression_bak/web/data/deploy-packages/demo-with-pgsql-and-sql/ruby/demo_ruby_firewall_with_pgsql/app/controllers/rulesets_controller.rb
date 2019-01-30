class RulesetsController < ApplicationController

  def index
    @rulesets = Ruleset.all :order => :from_id
    @zones = Zone.all
  end
  
  # GET /rulesets/1/edit
  def edit
    @ruleset = Ruleset.find(params[:id])
    @protocols = Protocol.all
  end

  def change
    @ruleset = Ruleset.find(params[:id])
    @ruleset.protocols.clear
    
    if params[:ruleset] && params[:ruleset][:protocol]
      params[:ruleset][:protocol].keys.each do |x|
        p = Protocol.find x
        if p
          @ruleset.protocols << p
        end
      end
    end
    
    redirect_to rulesets_path
  end
  
end
