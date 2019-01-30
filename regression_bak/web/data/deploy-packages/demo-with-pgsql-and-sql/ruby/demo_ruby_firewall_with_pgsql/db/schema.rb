# encoding: UTF-8
# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended to check this file into your version control system.

ActiveRecord::Schema.define(:version => 20120313094555) do

  create_table "batches", :force => true do |t|
    t.string   "desc"
    t.string   "result"
    t.integer  "zone_id"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "check_types", :force => true do |t|
    t.string   "name"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "deploy_batches", :force => true do |t|
    t.integer  "software_id"
    t.integer  "state",       :default => 1
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "deploy_errors", :force => true do |t|
    t.string   "name"
    t.string   "description"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "deploy_logs", :force => true do |t|
    t.integer  "deploy_batch_id"
    t.integer  "machine_package_id"
    t.integer  "deploy_error_id"
    t.integer  "machine_deploy_state_id"
    t.datetime "upload_file_at"
    t.string   "cause"
    t.boolean  "deploy"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "fs", :force => true do |t|
    t.integer  "sn"
    t.string   "name"
    t.integer  "package_id"
    t.string   "content_type"
    t.string   "destine"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.string   "md5sum"
  end

  create_table "logs", :force => true do |t|
    t.integer  "batch_id"
    t.string   "ip"
    t.boolean  "success"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "machine_deploy_states", :force => true do |t|
    t.string   "name"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "machines", :force => true do |t|
    t.string   "ip"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "machines_packages", :force => true do |t|
    t.integer  "machine_id"
    t.integer  "package_id"
    t.integer  "software_id"
    t.boolean  "installed",   :default => false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "management_servers", :force => true do |t|
    t.string   "ip"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "packages", :force => true do |t|
    t.integer  "version"
    t.integer  "software_id"
    t.boolean  "publish",     :default => false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "protocols", :force => true do |t|
    t.string   "name"
    t.string   "ports"
    t.boolean  "tcp"
    t.boolean  "udp"
    t.boolean  "sys"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "rules", :force => true do |t|
    t.integer  "ruleset_id"
    t.integer  "protocol_id"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "rulesets", :force => true do |t|
    t.integer  "from_id"
    t.integer  "to_id"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "softwares", :force => true do |t|
    t.string   "name"
    t.string   "description"
    t.string   "start_command"
    t.string   "stop_command"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.string   "scope"
    t.integer  "check_type_id", :default => 0
    t.string   "check_value"
    t.integer  "timeout",       :default => 60
    t.string   "groups"
    t.string   "users"
  end

  create_table "zones", :force => true do |t|
    t.string   "name"
    t.string   "desc"
    t.string   "value"
    t.boolean  "sys"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

end
