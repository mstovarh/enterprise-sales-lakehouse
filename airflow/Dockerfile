FROM apache/airflow:3.3.0

# Copiar Spark 3.5.3 desde la imagen que ya funciona
COPY --from=enterprise-sales-spark:3.5.3 /opt/spark /opt/spark

# Copiar Java 11 desde la imagen de Spark
COPY --from=enterprise-sales-spark:3.5.3 /opt/java/openjdk /opt/java/openjdk

USER root

# Spark necesita el comando ps
RUN apt-get update \
    && apt-get install -y --no-install-recommends procps \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/opt/java/openjdk
ENV SPARK_HOME=/opt/spark
ENV PATH="${JAVA_HOME}/bin:${SPARK_HOME}/bin:${PATH}"

USER airflow

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir \
    "apache-airflow==${AIRFLOW_VERSION}" \
    -r /requirements.txt