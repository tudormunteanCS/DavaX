./algorithms_api - backend (Python + Flask)
./frontend algorithms - frontend (React + Typescript)

For backend exposed 3 endpoints using Flask for the 3 computations needed
For persistance used SQLModel (pydantic) that could easily validate and store in SQL lite.

For Frontend created a one page web app using React that creates requests to the server with the number wanted for computation, waiting for answer.

Also used Docker for containerization of the app