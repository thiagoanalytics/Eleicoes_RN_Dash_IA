/*
Query para configurar uma Stored Procedure no Postgree,
esta procedure alimenta a tabela historico.hist_bens_candidatos,
abaixo está o script que usei para criar a tabela:

CREATE TABLE historico.hist_bens_candidatos(
ano INT NOT NULL
,sigla_uf VARCHAR(2) NOT NULL
,id_eleicao BIGINT NOT NULL
,tipo_eleicao TEXT
,data_eleicao DATE NOT NULL
,titulo_eleitoral_candidato BIGINT
,sequencial_candidato BIGINT
,tipo_item TEXT
,descricao_item TEXT
,valor_item NUMERIC(14,2)

)

Oriento a criar esta tabela após modelar os dados ou converter os tipos,
pois os tipos de dados de destino tem que ser o mesmo da origem que vc está enviando.

*/

--##########################################################
--### Tabela historico.hist_bens_candidatos
--##########################################################


CREATE OR REPLACE PROCEDURE historico.atualiza_bens_candidatos()
LANGUAGE plpgsql
AS $$
DECLARE -- declaração das variáveis que serão usadas no loop
    ano_minimo BIGINT;
    ano_maximo BIGINT;
    registros_origem INT;
BEGIN
    -- Obter menor e maior ano da tabela origem
    SELECT MIN(ano), MAX(ano) INTO ano_minimo, ano_maximo
    FROM stage.stg_cotacoes_bens;

    -- Criar tabela temporária apenas uma vez
    CREATE TEMP TABLE IF NOT EXISTS tabela (
        ano BIGINT,
        sigla_uf TEXT,
        id_eleicao BIGINT,
        tipo_eleicao TEXT,
        data_eleicao DATE,
        titulo_eleitoral_candidato BIGINT,
        sequencial_candidato BIGINT,
        tipo_item TEXT,
        descricao_item TEXT,
        valor_item NUMERIC(14,2)
    ) ON COMMIT DROP;

    WHILE ano_minimo <= ano_maximo LOOP -- inicio do loop(enquanto o ano_minimo for menor igual o ano_maximo rode a sequencia abaixo)

        -- Limpar dados da tabela temporária
        TRUNCATE TABLE tabela;

        -- Inserir dados do ano atual, retirando as duplicadas
        INSERT INTO tabela
        SELECT ano, sigla_uf, id_eleicao, tipo_eleicao, data_eleicao,
               titulo_eleitoral_candidato, sequencial_candidato,
               tipo_item, descricao_item, valor_item
        FROM (
            SELECT 
                ano::BIGINT,
                sigla_uf,
                id_eleicao::BIGINT,
                tipo_eleicao,
                data_eleicao::DATE,
                titulo_eleitoral_candidato::BIGINT,
                sequencial_candidato::BIGINT,
                tipo_item,
                descricao_item,
                valor_item::NUMERIC(14,2),
                ROW_NUMBER() OVER (
                    PARTITION BY ano, sequencial_candidato,descricao_item,valor_item
                    ORDER BY valor_item DESC
                ) AS rn
            FROM stage.stg_cotacoes_bens
            WHERE ano = ano_minimo -- filtro para enviar dados em lote envitando processar muitos dados
        ) t
        WHERE rn = 1;

        GET DIAGNOSTICS registros_origem = ROW_COUNT; -- recebe a quantidade de linhas processadas

        -- MERGE para atualizar e inserir dados
        MERGE INTO historico.hist_bens_candidatos DESTINO --Mescla a tabela destino
        USING tabela ORIGEM -- Com a origem
        /*Verifica se existe itens repetidos entre a origem e o destino*/
        ON DESTINO.ano = ORIGEM.ano 
		   AND DESTINO.sequencial_candidato = ORIGEM.sequencial_candidato
		   AND DESTINO.descricao_item = ORIGEM.descricao_item
		   AND DESTINO.valor_item = ORIGEM.valor_item
        WHEN MATCHED THEN --Caso haja dados repetidos apenas atualize os dados abaixo
            UPDATE SET 
			   sigla_uf = ORIGEM.sigla_uf, 
			   id_eleicao = ORIGEM.id_eleicao, 
			   tipo_eleicao = ORIGEM.tipo_eleicao, 
			   data_eleicao = ORIGEM.data_eleicao,
               titulo_eleitoral_candidato = ORIGEM.titulo_eleitoral_candidato, 
               tipo_item = ORIGEM.tipo_item
        WHEN NOT MATCHED THEN -- Caso não tenha repetidos, no caso dados únicos, alimente a tabela destino
            INSERT (ano, sigla_uf, id_eleicao, tipo_eleicao, data_eleicao,
                    titulo_eleitoral_candidato, sequencial_candidato,
                    tipo_item, descricao_item, valor_item)
            VALUES (ORIGEM.ano, ORIGEM.sigla_uf, ORIGEM.id_eleicao,
                    ORIGEM.tipo_eleicao, ORIGEM.data_eleicao,
                    ORIGEM.titulo_eleitoral_candidato, ORIGEM.sequencial_candidato,
                    ORIGEM.tipo_item, ORIGEM.descricao_item, ORIGEM.valor_item);

        -- Mensagem de depuração
        RAISE NOTICE 'Ano: %, Registros processados: %', ano_minimo, registros_origem; -- printa a quantidade de linhas processadas por ciclo

        -- Próximo ano
        ano_minimo := ano_minimo + 1; --incrementa mais um no fim do loop para acrecentar mais um ano ser filtrado
    END LOOP; -- fim do loop

END;
$$;
