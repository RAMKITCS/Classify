FROM python:3.8-slim
COPY . /
ENV bucket_name=intelligent_classifier
ENV secret_id=projects/393120312626/secrets/intelligent-service-key/versions/1
ENV gcp_secret=Service/noted-cortex-358103-caefed9e3bcf.json
ENV mongopass=Tcs@Projects2022
# RUN apk add --update-cache --no-cache libgcc libquadmath musl \
# && apk add --update-cache --no-cache libgfortran \
# && apk add --update-cache --no-cache lapack-dev
# RUN apk add --no-cache --update \
#     python3 python3-dev gcc \
#     gfortran musl-dev
# RUN pip install --upgrade pip
# RUN pip install pybind11 pandas
# WORKDIR /Classify
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]

# FROM gcr.io/google-appengine/python
# LABEL python_version="python3.8"
# COPY . /Classify
# WORKDIR /Classify
# RUN virtualenv --no-download /env -p python3.8
# ENV VIRTUAL_ENV /env
# ENV PATH /env/bin:$PATH
# RUN pip install -r Classify/requirements.txt
# EXPOSE 5000
# ENTRYPOINT [ "python" ]
# CMD [ "Classify/main.py" ]

