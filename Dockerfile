FROM public.ecr.aws/lambda/python:3.12

ENV LAMBDA_TASK_ROOT=/var/task

COPY requirements.txt .

RUN pip install -r requirements.txt
COPY . ${LAMBDA_TASK_ROOT}

CMD [ "app.lambda_handler" ]