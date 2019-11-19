# Postman Config
Postman is used to test the backend routes and endpoints. To use the config, simply import it into postman.

## Structure
The config is set up with the following structure
```
Scribble: Contains entire workspace
  | account/ : Contains tests endpoints of the accounts/ route
    | sample-api
    | register
    | login
```

## Route / Endpoint Descriptions
By right clicking on a route or endpoint and clicking edit, a description of the route / endpoint is available

## Variables
Many routes require data to be sent with the request. To handle the changing data, variables are provided that can be changed for testing. They are located in the workspace settings which can be accessed by right clicking the workspace (eg. Scribble) and clicking edit, then clicking the Variables tab. Be sure to only change the CURRENT VALUE column.