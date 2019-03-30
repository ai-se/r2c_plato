FROM ubuntu:17.10

# Install packages
RUN apt update && apt install -y wget && apt install -y bzip2 && apt install -y tree && apt install -y libsm6 libxext6 && apt install -y git-core && apt install -y nodejs npm && apt install -y npm
#RUN npm i escomplex --save
#RUN npm install -g complexity-report
RUN npm install -g plato
RUN mkdir -p /analyzer
RUN groupadd -r analysis && useradd --no-log-init --system --gid analysis analysis -d /analyzer
RUN chown -R analysis:analysis /analyzer

# install Python
RUN apt install -y python3
RUN apt install -y python3-pip
USER analysis
COPY --chown=analysis:analysis src /analyzer

# installind other python packages
RUN pip3 install -r /analyzer/src/requirements.txt



WORKDIR /
CMD ["/analyzer/analyze.sh"]