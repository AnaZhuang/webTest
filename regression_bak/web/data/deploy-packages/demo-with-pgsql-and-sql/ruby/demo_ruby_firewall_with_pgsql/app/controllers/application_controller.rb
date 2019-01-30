class ApplicationController < ActionController::Base
  protect_from_forgery :except => [ {:controller => :softwares, :action => :update_error}, 
    {:controller => :softwares, :action => :update_state}]
end
