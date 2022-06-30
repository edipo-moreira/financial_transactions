FROM python:3.9
# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code/
# Install dependencies
COPY ./requirements.txt /code/requirements.txt
COPY ./.env /code/.env
COPY ./backend_test.db /code/backend_test.db

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
EXPOSE 8081
CMD ["python", "app/main.py"]