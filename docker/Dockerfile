FROM victorcmoura/pade:paradigmas

ENV TZ=America/Sao_Paulo

WORKDIR /trust_and_game_theory

ADD docker/pade_config.json ./

COPY ./src/ ./

CMD pade start-runtime --config_file pade_config.json
