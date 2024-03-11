FROM python:3.8-alpine

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# App specific environnement variables.
ENV HOST=http://159.203.50.162
ENV TOKEN=fb5bdbf38ce5d1b4c43b
ENV T_MAX=30
ENV T_MIN=25
ENV PG_USER=user02eq1
ENV PG_HOST=157.230.69.113
ENV PG_DATABASE=db02eq1
ENV PG_PASSWORD=3EhMhvn5WRjYOw84
ENV PG_PORT=5432
#ENV DB_URL=...

WORKDIR /app

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8001

# Install dependecies
RUN pip install tomli --user
RUN pip install pipenv --user
RUN python -m pipenv install


# Run the application.
CMD python -m pipenv run start
