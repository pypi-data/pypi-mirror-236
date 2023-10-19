import os
import sys

##-- Declare ENV Variables from YML file
apikey = os.environ['TD_API_KEY'] 
tdserver = os.environ['TD_API_SERVER']
sink_database = os.environ['SINK_DB']
output_table = os.environ['OUTPUT_TABLE']
ps_to_scan = os.environ['ps_to_scan']
last_n_runs =  os.environ['last_n_runs']

#pip-install scan ps library
os.system(f"{sys.executable} -m pip install td-ml-ps-stats-scan")

#import all functions and variables from library
from  td_ml_ps_stats_scan import *

##################### TIME DIFF FUNCTION #####################################
#Function below calculates time diff between start and end date for each Activation WF run
def calculate_time_diff(start_time_str, end_time_str):
    # Convert the string timestamps to datetime objects
    start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%SZ')
    end_time = datetime.datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M:%SZ')

    # Calculate the time difference
    time_difference = end_time - start_time

    # Convert the time difference to minutes
    minutes = round(time_difference.total_seconds() / 60, 2)

    return minutes

##################### PARSE DAY #####################################
#Function below Parses Day of Week from Datetime
def day_of_week(date_string):
    date_object = datetime.datetime.fromisoformat(date_string)
    day_of_week = date_object.strftime("%A")
    time = date_object.time()
    return day_of_week[:3] + f', {time}'

##################### ACTIVATIONS STATS FUNCTION #####################################
#Function below extracts all activations info from various endpoints. It uses param `last_n_runs` to calcualte AVG activation runtime for the last n-runs
def get_activations(ps_df, last_n_runs):
  #empty list to store JSON responses
  all_activations = []

  #Get ps_id and ps_name from ps_df
  ps_id = ps_df['ps_id_v4'].unique().tolist()[0]
  ps_name = ps_df['ps_name'].unique().tolist()[0]

  ps_activations_v5 = f'https://api-cdp.treasuredata.com/entities/parent_segments/{ps_id}/syndications'
  activations_list = json_extract(ps_activations_v5)['data']

  #Loop through each activation and get list of executions to extract runtime, activation_channel etc.
  for item in activations_list:
      segment_id = item['relationships']['segment']['data']['id']
      activation_id = item['id']

      #Return JSON reponse for each activation_id and segment_id
      activations_by_id = f'https://api-cdp.treasuredata.com/entities/segments/{segment_id}/syndications/{activation_id}'
      act_info = json_extract(activations_by_id)
      
      #Parse activation data and user info
      activation = act_info['data']
      activation_included = act_info['included']
      last_n_runs = int(last_n_runs)
      
      #check if created user different than updated user
      if len(activation_included) < 2:
          created_by = updated_by = activation_included[0]['attributes']['name']
      else:
          created_by = activation_included[0]['attributes']['name']
          updated_by = activation_included[1]['attributes']['name']
      
      #check if 'startAt' param is proper datetime and extract schedule time
      start_at = activation['attributes']['startAt'] 
      if start_at:
          schedule_time = day_of_week(start_at)
      else:
          schedule_time = None

      #Parse executions list for last_n_runs
      executions = activation['attributes']['executions'][:last_n_runs]

      #check if there were any executions and extract executions stats
      if len(executions) > 0:
          last_run_date = executions[0]['createdAt']
          last_run_status = executions[0]['status']
          last_run_time = calculate_time_diff(executions[0]['createdAt'], executions[0]['finishedAt'])
          runtime_list = [calculate_time_diff(item['createdAt'], item['finishedAt']) for item in executions]
          avg_runtime = round(sum(runtime_list) / len(runtime_list), 2)
      else:
          last_run_date = None
          last_run_status = None
          last_run_time = None
          avg_runtime = None

      ##Get JSON response from activation workflow results to extract activations channel 
      workflow_queries = f'https://{segment_api}/audiences/{ps_id}/segments/{segment_id}/syndications/{activation_id}/workflow_queries'
      queries = json_extract(workflow_queries)
      
      #try to parse activation_channel
      try:
          con_type = queries['result_connection_type']
          con_name = queries['result_connection']
      except:
          con_type = None
          con_name = None
      
      all_activations.append({'ps_id': ps_id,
                          'ps_name': ps_name,
                          'activation_id': activation_id,
                          'activation_name': activation['attributes']['name'],
                          'con_id': activation['attributes']['connectionId'],
                          'con_name': con_name,
                          'activation_channel': con_type,
                          'segment_id' : segment_id,
                          'schedule': activation['attributes']['repeatUnit'],
                          'schedule_time': schedule_time,
                          'schedule_timezone' : activation['attributes']['timezone'],
                          'created_at': activation['attributes']['createdAt'][:19].replace('T', ' '),
                          'created_by': created_by,
                          'updated_at': activation['attributes']['updatedAt'][:19].replace('T', ' '),
                          'updated_by': updated_by,
                          'last_run_date': last_run_date,
                          'last_run_status': last_run_status,
                          'last_run_time': last_run_time,
                          'avg_runtime': avg_runtime
                          })

  activ_df = pd.DataFrame(all_activations)
    
  return activ_df 

##################### FINAL FUNCTION THAT RUNS ALL CODE #####################################
def main():
    #get Parent Segment DF
    ps_df = scan_parent_segments.get_ps_list()
    ps_df = ps_df[ps_df['ps_id_v4'] == ps_to_scan]
    
    #get Folder Info DF
    folders_df = scan_parent_segments.get_folder_list(ps_df)

    #Merge both DFs on ps_id
    combined_df = pd.merge(ps_df, folders_df, on="ps_id", how = 'left')

    #Get Folder Segments Info
    segments_df = scan_parent_segments.get_segment_list(combined_df)
    
    #Get CJO Journeys Info
    journey_df = scan_parent_segments.get_journey_list(combined_df)

    #If CJO Journeys exist, combine Segments and Journey DFs and get Journey Stage Stats
    if len(journey_df) > 0:
        journey_final = journey_df[['folder_id', 'journey_name', 'segment_id', 'segment_name', 'segment_population', 'segment_type', 'rule', 'stage_name', 'stage_id', 'stage_idx',  'stage_population', 'stage_rule']]
        segments_df = pd.concat([segments_df, journey_final])
        segments_df.reset_index(drop=True, inplace=True)

    #Merge Segments DF into combined on folder_id
    final_df = pd.merge(combined_df, segments_df, on="folder_id", how = 'right')

    #Replace NaN with 0 for numeric columns and drop duplicate columns caused by v4/v5 segment name overlap
    final_df.segment_population.fillna(0, inplace = True)
    final_df.realtime.fillna(0, inplace = True)
    final_df.dropna(subset = ['segment_id'], inplace = True)
    final_df.drop_duplicates(subset=['root_folder', 'folder_id', 'folder_name', 'segment_id', 'segment_name'], keep='first', inplace=True, ignore_index=False)

    #Ensure population columns are written as INTEGER
    final_df['segment_population'] = pd.to_numeric(final_df['segment_population'], errors='coerce').astype('Int64')
    
    try:
      final_df['stage_population'] = pd.to_numeric(final_df['stage_population'], errors='coerce').astype('Int64')
    except:
      print(f'######## No Journey Segments Were Found in Parent Segment ID: {ps_to_scan} ########')

    #Write final_df to TD
    client = pytd.Client(apikey=apikey, endpoint=tdserver, database=sink_database)
    client.load_table_from_dataframe(final_df, 'activation_stats_ps_objects', writer='bulk_import', if_exists='append')

    #Get Activations Info
    activations_df = get_activations(ps_df, last_n_runs)

    if len(activations_df) > 0:

      #Write activations_final to TD
      client = pytd.Client(apikey=apikey, endpoint=tdserver, database=sink_database)
      client.load_table_from_dataframe(activations_df, output_table, writer='bulk_import', if_exists='append')
      
    else:
        print(f'### EXCEPTION ### -> No Activations Were Found in Parent Segment ID: {ps_to_scan}')