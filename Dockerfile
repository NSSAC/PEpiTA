FROM mambaorg/micromamba:1-bookworm-slim
USER 0

# RUN apt-get update \
# 	&& apt-get install -y --no-install-recommends \
# 		postgresql-client \
# 	&& rm -rf /var/lib/apt/lists/*

COPY environment.yml pepita.scif /
COPY webdesign /webdesign

RUN micromamba install --yes --name base --file /environment.yml

ENV MAMBA_ROOT_PREFIX="/opt/conda"
ENV PATH="${MAMBA_ROOT_PREFIX}/bin:${PATH}"

RUN pip install ipython scif
RUN scif install /pepita.scif

# RUN python manage.py migrate

EXPOSE 8000

ENTRYPOINT ["scif"]

CMD ["run", "webapp"]