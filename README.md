# Radarr Actions
Custom Home Assistant integration for interacting with Radarr via [Assist](https://www.home-assistant.io/voice_control/).
It creates services such as Add Movie and Remove Movie that can be configured using [intent scripts](https://www.home-assistant.io/integrations/intent_script) to interact with Radarr via voice and text.

![banner](https://media3.giphy.com/media/YHS3q6eeRAgvNmga6Z/giphy.gif)


## Requirements
- Radarr v3 or newer.
- Custom integration [yarvis](https://github.com/siemon-geeroms/yarvis). It enables you to pass dynamic tokens to your defined [intent scripts](https://www.home-assistant.io/integrations/intent_script)

*Vanilla Home Assistant [intent scripts](https://www.home-assistant.io/integrations/intent_script) don't allow wildcards. That's why yarvis is required.*

## Installation

Install this component via HACS using the custom repositories option. More information here: [install from custom repositories](https://hacs.xyz/docs/faq/custom_repositories/). 
Once you added the custom repository make sure to click Download to complete the installation.

## Configuration

### Enable Component
Add the component to your configuration.yaml.
```yaml
radarr_actions:
```

### Intent scripts
Add your intents to your configuration.yaml inside the intent_script domain.
```yaml
RadarrAddMovie:
  action:
    - service: radarr_actions.add_movie
      data_template:
        host: "http://192.168.1.101:7878" #replace with your host
        api_key: "YOUR_RADARR_API_KEY" 
        movie_title: '{{ movie }}'
        profile_id: 4 #replace with your profile_id. See Wiki for more info
        root_directory: "/path/to/directory" #replace with your root_directory
        search_release: True # True or False
        tmdbid_api_key_v3: "YOUR_TMDBID_API_KEY" #Optional. Remove field if not used.
      response_variable: result # get service response
    - stop: ""
      response_variable: result
  speech:
    text: "{{ action_response['message'] }}"

RadarrRemoveLastMovie:
  action:
    - service: radarr_actions.remove_movie
      data_template:
        host: "http://192.168.1.101:7878"  #replace with your host
        api_key: "YOUR_RADARR_API_KEY"
      response_variable: result # get service response
    - stop: ""
      response_variable: result
  speech:
    text: "{{ action_response['message'] }}"
```

*tmdbid_api_key_v3* is used for movie cast details in responses. It's optional, remove field completely if not used. It's free. You can get one at https://www.themoviedb.org/settings/api v3 auth. 

You can create more intents for specific tasks, or different Radarr instances. For example, an intent excluding movies older than 2 years would be great for adding new and upcoming movies with very high success rate.
```yaml
RadarrAddUpcomingMovie:
  action:
    - service: radarr_actions.add_movie
      data_template:
        host: "http://192.168.1.101:7878" #replace with your host
        api_key: "YOUR_RADARR_API_KEY" 
        movie_title: '{{ movie }}'
        profile_id: 4 #replace with your profile_id. See Wiki for more info
        root_directory: "/path/to/directory" #replace with your root_directory
        exclude_older_than_n_years: 2
        search_release: True # True or False
        tmdbid_api_key_v3: "YOUR_TMDBID_API_KEY" #Optional. Remove field if not used.
      response_variable: result # get service response
    - stop: ""
      response_variable: result
  speech:
    text: "{{ action_response['message'] }}"
```

### yarvis integration
1. Once yarvis is installed, go to Home Assistant > Settings > Devices & Services > Integrations > yarvis > Configure.
Add the sentences for the intents that you previously defined, so they can recieve a wildcard token via yarvis.
```yaml
RadarrAddMovie:
  sentences:
    - add movie (?P<movie>.*?$)
```
2. Go to Home Assistant > Settings > Voice Assistants. Add a voice assistant or change your current one to use the Yarvis conversation agent.
3. Restart HA.

### Test it
Go to your Home Assistant dashboard, click on the conversation bubble on the top right corner and type:
```
add movie children of men
```

## Services documentation

### Add Movie
Looks up for a movie title or partial title and add the best match to Radarr.
(It uses the Radarr lookup service).

| Fields                     | Description                                                                                                                 | Example                   | Required |
|----------------------------|-----------------------------------------------------------------------------------------------------------------------------|---------------------------|----------|
| host                       | Radarr host with protocol (http or https) and port                                                                          | http://127.0.0.1:7878     | Yes      |
| api_key                    | Radarr API Key                                                                                                              | XXXXXXXXXXXXX             | Yes      |
| movie_title                | Name of the movie or term (include year for best match)                                                                     | Children of men           | Yes      |
| profile_id                 | Quality profile id number. eg. 4 is 1080p                                                                                   | 4                         | Yes      |
| root_directory             | Path to Radarr root directory. Also knwon as rootFolderPath                                                                 | /path/to/movies/directory | Yes      |
| exclude_older_than_n_years | Exclude searching movies older than N years. (Remove field to include all years).                                                                             | 70                        | No       |
| search_release             | Ask Radarr to search for a release. (Default: False)                                                                        | True                      | No       |
| tmdbid_api_key_v3          | https://www.themoviedb.org API Key. Used for movie cast details in responses. It's free. Get one at https://www.themoviedb.org/settings/api v3 auth. (Remove field if not used)| XXXXXXXXXXXXX             | No       |


### Remove Movie
Removes the last added movie via this integration. Helpful for removing mismatched movies.

| Fields                     | Description                                                                                                                 | Example                   | Required |
|----------------------------|-----------------------------------------------------------------------------------------------------------------------------|---------------------------|----------|
| host                       | Radarr host with protocol (http or https) and port                                                                          | http://127.0.0.1:7878     | Yes      |
| api_key                    | Radarr API Key                                                                                                              | XXXXXXXXXXXXX             | Yes      |


## TODO
- Refactor code to make API calls through [aiopyarr](https://github.com/tkdrob/aiopyarr).
- Use translations.
- Add config flow for configuration fields such as host, api_key, etc.
- Unit tests.

## Did you find this useful and would like to support my work?
<a href="https://paypal.me/avrahamvr/"><img src="https://github.com/andreostrovsky/donate-with-paypal/blob/master/blue.svg" height="40"></a> 
