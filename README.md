# ZOWT

`docker compose up --build`

For unix the created data/mongo folder might have files with the wrong permissions to run the above docker command for a second time.
To fix this give the files in data/mongo the right permissions (`sudo chmod 755 data/mongo/*`)
