# RUN

## Downloading Activities from Garmin and Running

1. Login into [Garmin Connect]() and navigate to the activities page.
2. Open DevTools and run the following code in the console tab. Change 'running' to 'walking' for desired activity type.

```
jQuery.getJSON(
    'https://connect.garmin.com/modern/proxy/activitylist-service/activities/search/activities?limit=5000',
    function(act_list)
    {
        var t=0;
        act_list.forEach(
        function(act)
            {
                setTimeout(function() {
                    console.dir(act['activityId'], act['activityName'], act['startTimeLocal']);
                    if (act.activityType.typeKey == 'running') {
                        location = 'https://connect.garmin.com/modern/proxy/download-service/export/gpx/activity/' + act['activityId'];
                    }
                }, t+=1000);
            }
        );
    }
);
```

3. Move all downloaded files into the Data folder of the project.
4. Run the program.