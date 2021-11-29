# Driver Tracker API

<details>
  <summary>Inroduction</summary>
This project aims to create an REST-API to be used with an application to monitor a driver's work hours to follow federal regulations on how many hours a driver can work and operate behind a vehicle. According to federal regulations, professional drivers must refrain from working more than 14 hours per day, with no more than 11 of their work hours being driving hours. Furthermore, drivers must take 10 consecutive hours of "off-work" time prior to working each full shift. The API allows an application to request GET, POST, PUT, and DELETE work events, as well as request GET events summary. For the purpose of this project, this API considers only one driver.
</details>
<details>
  <summary>Technologies</summary>
- Python 3.8
- djangorestframework 3.12.4
 </details>

<details>
  <summary>Endpoints</summary>
  <p>
This API has coverage for retrieving, creating, updating and deleting work event data in JSON format. Moreover, you can get event summaries which presented as DRIVE_CLOCK and WORK_CLOCK in form of JSON data.

### Event
An event represents driver's activity and time duration
- #### Retrieve and create events
    This endpoint is for GET and POST requests of events in JSON format
    
    ```
    http://127.0.0.1:8000/api/v1/events/
    ```
    
- #### Retrieve, update and delete an existing event
    This endpoint is for GET, PUT, DELETE requests of an existing event in JSON format (partial updating is not supported)
    
    ```
    http://127.0.0.1:8000/api/v1/events/{event_id}/
    ```

### Events Summary
Events summary summarizes all events and present in forms of DRIVE_CLOCK and WORK_CLOCK. This endpoint gives you events summary data in JSON format

```
http://127.0.0.1:8000/api/v1/clocks/
```
  </p>
</details>

<details>
  <summary>Data Definitions</summary>
Defination of data in Driver Tracker API

### Event
- **_id_**: an event's id (integer)

- **_workStatus_**: driver's activity  
  **Possible values**
  - D (driving)
  - W (working)
  - OFF (off_duty)
  
- **_duration_**: time duration of the event (HH:MM:SS)

### Events Summary
Includes two clocks (DRIVE_CLOCK and WORK_CLOCK)

- **_type_**: type of clock  
  **Possible values**
  - DRIVE_CLOCK (count driving hours)
  - WORK_CLOCK (count driving + working + off_duty hours)

- **_timeValue_**: total time duration that counted against the clock (HH:MM:SS)

- **_violationStatus_**: status of driver according to the clock  
  **Possible values**
  - OK (driver's hours don't exceed limits, 11 hours for driving and 14 hours for working)
  - V (driver's hours exceed the limits)
</details>

<details>
  <summary>Getting Started</summary>
1. [Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) this repository to your local computer
2. Open a terminal and change directory to 'driver-tracker', you should see 'vevn' folder and 'requirements.txt' file here
3. Activate 'venv' virtual environment
4. Install 'requirements.txt' file by running

  ```
  pip install -r requirements.txt
  ```

5. Change directory to 'driverTracker' and run below command line to starts the development server

  ```
  python manage.py runserver
  ```

6. The server is now up and running and the endpoints are ready for you!

To work with the endpoints you migth need other tools such as [Postman](https://www.postman.com/)
  </details>
