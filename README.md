# SSIN1920

Notes:

- We noticed a small bug during the "refresh token" process, it doesn't insert the "scope" into the new token, so the resource server won't accept it. Only an original token can be used, although the token is indeed refreshed

Instructions for setup:

    docker-compose up

After the services finish loading, simply access these endpoints for each service:

- Authentication server - http://localhost:8000/
- Client server - http://localhost:8001/
- Resources server - http://localhost:8002/

The project's report can be found in the main directory:

    report.pdf
