FROM ubuntu:bionic

WORKDIR /app

EXPOSE 8000

ENV LANG C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

RUN apt-get install -y curl
RUN apt-get install -y build-essential

RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN ln -s /usr/bin/python3 /bin/python
RUN ln -s /usr/bin/pip3 /bin/pip

RUN curl -O https://nodejs.org/dist/v12.13.0/node-v12.13.0-linux-x64.tar.xz
RUN tar -xf node-v12.13.0-linux-x64.tar.xz -C /opt
RUN ln -s /opt/node-v12.13.0-linux-x64/bin/node /bin
RUN ln -s /opt/node-v12.13.0-linux-x64/bin/npm /bin
RUN ln -s /opt/node-v12.13.0-linux-x64/bin/npx /bin

RUN apt-get install -y g++-mingw-w64-x86-64
RUN apt-get install -y gcc-mingw-w64-x86-64

RUN apt-get install -y g++-mingw-w64-i686
RUN apt-get install -y gcc-mingw-w64-i686

RUN pip install --upgrade pip
RUN pip install pipenv

COPY ./Pipfile /app/Pipfile
RUN pipenv install --skip-lock --system --dev

CMD ["python",  "manage.py", "runserver", "0.0.0.0:8000"]

