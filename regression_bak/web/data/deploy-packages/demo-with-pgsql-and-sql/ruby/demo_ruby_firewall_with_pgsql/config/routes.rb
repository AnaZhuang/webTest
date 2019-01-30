Sister::Application.routes.draw do
  
  resources :deploy_batches

  resources :softwares do
    post 'deploy', :on => :member
    post 'undeploy', :on => :member
    post 'update_error', :on => :collection
    post 'update_state', :on => :collection
    post 'import', :on => :collection
    post 'export', :on => :member
    get 'conf', :on => :member
    resources :deploy_batches do
      resources :deploy_logs do
        post 'update_state', :on => :collection
      end
    end
    resources :packages do
      put 'publish', :on => :member
      put 'unpublish', :on => :member
      resources :fs do
        put 'up', :on => :member
        put 'down', :on => :member
      end
    end
  end

  resources :management_servers

  resources :machines

  resources :zones do
    get 'download', :on => :member
    post 'deploy', :on => :member
    post 'clear', :on => :member
    resources :batches do
      resources :logs
    end
  end

  resources :protocols
  
  resources :rulesets do
    put 'change', :on => :member
  end  
  
  # The priority is based upon order of creation:
  # first created -> highest priority.

  # Sample of regular route:
  #   match 'products/:id' => 'catalog#view'
  # Keep in mind you can assign values other than :controller and :action

  # Sample of named route:
  #   match 'products/:id/purchase' => 'catalog#purchase', :as => :purchase
  # This route can be invoked with purchase_url(:id => product.id)

  # Sample resource route (maps HTTP verbs to controller actions automatically):
  #   resources :products

  # Sample resource route with options:
  #   resources :products do
  #     member do
  #       get 'short'
  #       post 'toggle'
  #     end
  #
  #     collection do
  #       get 'sold'
  #     end
  #   end

  # Sample resource route with sub-resources:
  #   resources :products do
  #     resources :comments, :sales
  #     resource :seller
  #   end

  # Sample resource route with more complex sub-resources
  #   resources :products do
  #     resources :comments
  #     resources :sales do
  #       get 'recent', :on => :collection
  #     end
  #   end

  # Sample resource route within a namespace:
  #   namespace :admin do
  #     # Directs /admin/products/* to Admin::ProductsController
  #     # (app/controllers/admin/products_controller.rb)
  #     resources :products
  #   end

  # You can have the root of your site routed with "root"
  # just remember to delete public/index.html.
  root :to => 'zones#index'

  # See how all your routes lay out with "rake routes"

  # This is a legacy wild controller route that's not recommended for RESTful applications.
  # Note: This route will make all actions in every controller accessible via GET requests.
  # match ':controller(/:action(/:id(.:format)))'
end
