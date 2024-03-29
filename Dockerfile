FROM ubuntu:18.04

# Install dependencies
RUN apt-get update -y && \
apt install -y python3-pip && \
apt-get -y install unzip && \
pip3 install ipynb-py-convert && \
pip3 install awswrangler && \
pip3 install great_expectations

# Downloading data + code from github
RUN echo 'git clone https://github.com/vaishalijadhav15/trivago_usecase.git'

# One time Deployment for Data creation
RUN echo 'make deploy'

#installing python-3 for running notebook
RUN echo 'sudo apt install python3-pip'
RUN echo 'cd trivago_usecase/'
RUN echo 'unzip package.zip'

#converting python notebook into python code(single file)
RUN echo 'ipynb-py-convert usp.ipynb usp.py'

#running python notebook script
RUN echo 'python3 usp.py'

#running data validation script
RUN echo 'python3 check.py --bucket tvg-poc-data --date 2019-08-01'
