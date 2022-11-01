FROM amazon/aws-lambda-python:latest

# The next two need to match
ARG PYSPARK_VERSION=3.2.1
ARG HADOOP_VERSION=3.3.1
ARG AWS_SDK_VERSION=1.12.305

# Install Java 8
RUN yum install -y java-1.8.0-openjdk

# Install dependencies
RUN pip install pyspark==$PYSPARK_VERSION
RUN pip install boto3

# Set ENV vars
ARG EXPECTED_PY4J_ZIP=py4j-0.10.9.3-src.zip
ARG EXPECTED_JAVA_HOME_DIR=java-1.8.0-openjdk-1.8.0.342.b07-1.amzn2.0.1.x86_64
ENV SPARK_HOME="/var/lang/lib/python3.9/site-packages/pyspark"
ENV PATH=$PATH:$SPARK_HOME/bin
ENV PATH=$PATH:$SPARK_HOME/sbin
ARG PY4J_ZIP=$SPARK_HOME/python/lib/$EXPECTED_PY4J_ZIP
RUN test -f $PY4J_ZIP || { echo "Could not find $PY4J_ZIP, update your dockerfile"; echo "Found: $(find $SPARK_HOME/python/lib/ -type f -name 'py4j*.zip')"; exit 1; }
ENV PYTHONPATH=$SPARK_HOME/python:$PY4J_ZIP:$PYTHONPATH
ENV JAVA_HOME="/usr/lib/jvm/$EXPECTED_JAVA_HOME_DIR/jre"
RUN test -d $JAVA_HOME || { echo "Could not find $JAVA_HOME, update your dockerfile"; echo "Found: $(find /usr/lib/jvm/ -type d -name 'java-1.8.0-openjdk-1.8.0.*')/jre"; exit 1; }
ENV PATH=$SPARK_HOME/python:$PATH:$JAVA_HOME/bin

# Get jars to read from S3 into pyspark classpath
RUN yum install wget -y
RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_VERSION}/hadoop-aws-${HADOOP_VERSION}.jar \
  -P ${SPARK_HOME}/jars/
RUN wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_SDK_VERSION}/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar \
  -P ${SPARK_HOME}/jars/

# File to set up jvm env for spark
COPY spark-class $SPARK_HOME/bin/spark-class
RUN chmod 777 $SPARK_HOME/bin/spark-class

# Create entrypoint
COPY entrypoint.py $LAMBDA_TASK_ROOT
CMD ["entrypoint.lambda_handler"]