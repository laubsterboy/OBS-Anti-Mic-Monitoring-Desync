import obspython as obs
import time

######## Global Variables ########
source_name = ""
update_interval = 60
mic_type = "wasapi_input_capture"

######## Config Variables ########
min_slider_value = 1
max_slider_value = 3600
slider_inverval = 1
default_update_interval = 60

######## Methods ########

def reset_monitoring():
  global source_name
  source = obs.obs_get_source_by_name(source_name)
  print(source_name)
  if source:
    obs.obs_source_set_monitoring_type(source, obs.OBS_MONITORING_TYPE_NONE)
    print("Monitoring disabled")
    obs.obs_source_set_monitoring_type(source, obs.OBS_MONITORING_TYPE_MONITOR_AND_OUTPUT)
    print("Monitoring enabled")
  else:
    print("Monitoring device not found with the name {source_name}.")

######## Main OBS functions ########

def script_defaults(settings):
  global default_update_interval
  obs.obs_data_set_default_int(settings, "update_interval", default_update_interval)

def script_update(settings):
  global update_interval, source_name
  source_name = obs.obs_data_get_string(settings, "source")
  update_interval = obs.obs_data_get_int(settings, "update_interval")
  obs.timer_remove(reset_monitoring)
  obs.timer_add(reset_monitoring, update_interval*1000)

def script_load(settings):
  global update_interval, source_name
  source_name = obs.obs_data_get_string(settings, "source")
  update_interval = obs.obs_data_get_int(settings, "update_interval")
  obs.timer_add(reset_monitoring, update_interval*1000)

def script_properties():
  props = obs.obs_properties_create()
  p = obs.obs_properties_add_list(props, "source", "Microphone", 
    obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
  obs.obs_properties_add_int_slider(props, "update_interval", "Update Interval (s):", min_slider_value, max_slider_value, slider_inverval)
  sources = obs.obs_enum_sources()
  if sources:
    for source in sources:
      source_id = obs.obs_source_get_id(source)
      if source_id == mic_type:
        name = obs.obs_source_get_name(source)
        obs.obs_property_list_add_string(p, name, name)
  obs.source_list_release(sources)
  return props

def script_description():
  return "Resets the audio monitoring for the selected microphone to mitigate the buffer buildup problem."