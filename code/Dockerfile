FROM python
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN groupadd -r djangouser
RUN useradd -r -g djangouser djangouser
USER djangouser
