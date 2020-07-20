FROM tensorflow/tensorflow:latest-gpu-py3
RUN apt-get update
RUN apt-get install -y libsm6 libxext6 libxrender-dev
RUN pip3 install tensorflow-gpu
RUN pip install --user --upgrade tensorflow-gpu
RUN pip3 install\
        numpy\
        keras\
        scikit-learn\
        opencv-python\
        pandas\
        tqdm\
        tensorflow-gpu\
        matplotlib\
        PyMySQL
COPY . .
RUN chmod +x run.sh
ENTRYPOINT ["./run.sh"]
