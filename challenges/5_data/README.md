# Challenge 5

![Project Design](./docs/project_design.png)

## Tratativa dados

Tratativa dos dados Levando em consideração que correlação não equivale a causalidade, preocupação na preparação dos dados para gerar modelo com baixo índice de vies.

### Application

#### Deletar Coluna

email_secundario (vazia)
cv_en: (vazia)
nome: (irrelevante, possibilidade vies)
email: (irrelevante, possibilidade vies)
inserido_por: (irrelevante, possibilidade vies)
data_nascimento (irrelevante, possibilidade vies por idade)
qualificacoes: (98% vazia)
experiencias: (98% vazia)
outro_curso: (98% vazia)
id_ibrati: (98% vazia)
email_corporativo: (98% vazia)
projeto_atual: (98% vazia)
cliente: (98% vazia)
unidade: (98% vazia)
nome_superior_imediato: (98% vazia)
email_superior_imediato: (98% vazia)
cargo_atual: (98% vazia)
telefone_recado (vazia)
telefone (irrelevante, possibilidade de vies por DDD)
cpf (vazia)
skype (vazia)
url_linkedin (vazia)
facebook (vazia)
download_cv (extensão arquivo, irrelevante para nossa analize)

#### Normalizar

data_aceite (muitos campos distintos cerca de 26%, buscar padrão com datas)
fonte_indicacao (muitos registros com ":")
sexo (muitos registros vazios, considerar apenas para vagas afirmativas, desconsiderar no modelo)
estado_civil (muitos registros vazios, considerar apenas para vagas afirmativas, desconsiderar no modelo)
pcd (muitos registros vazios, considerar apenas para vagas afirmativas, desconsiderar no modelo)

conhecimentos_tecnicos (criar lista de campos, separados por ';', ',' ou '|')
certificacoes (muitos registros vazios, separados por ';', ',' ou '|')
outras_certificacoes (muitos registros vazios, separados por ';', ',' ou '|')

nivel_academico (muitos registros vazios)
nivel_ingles (muitos registros vazios)
nivel_espanhol (muitos registros vazios)
outro_idioma (muitos registros com "-")

#### Tratativa especial

remuneracao (muitos registros vazios, variações entre padrões: "R$00,00, "1.000,00", "mensal / 1000", por hora e etc)
cv_pt (muitas variações, letras separadas por espaço, quebras de texto sem padrão, "em anexo" e vazios também estão presentes)

### Prospects

### OBS

Existem linha completamente vazias (aprox 5%)

#### Deletar Coluna

prospect_comentario (irrelevante)
prospect_recrutador_nome (irrelevante, possibilidade vies)
modalidade (97% vazio)
prospect_name (irrelevante, possibilidade vies)

#### Normalizar

prospect_situacao_candidado (registro com 21 campos distintos, possibilidade de ir manualmente entre eles e validar duplicidades)
titulo (registro com campo de texto aberto, quase 10k titulos diferentes, preenchido pelo candidato, padronizar senioridade complemento application `nivel_profissional` ) OBS: Possibilidade de comparar com titulo da vaga.

#### Tratativa especial

prospect_codigo (cuidado na tratativa, valor código porém está com ".0", modificar na hora de tabelar para ficar como código)

### Vagas

#### Deletar Coluna

solicitante_cliente (irrelevante, vies)
empresa_divisao (irrelevante, vies)
requisitante (irrelevante, vies)
analista_responsavel (irrelevante, vies)
superior_imediato (unico valor)
nome (99% vazio, vies)
telefone (99% vazio)
pais (unico valor)
bairro (92% vazio)
regiao (90% vazio)
faixa_etaria (vies)
horario_trabalho (99% vazio)
outro_idioma (97% vazio)
nome_substituto (irrelevante, vies)

#### Normalizar


tipo_contratacao (39 opções diferentes)
prazo_contratacao (2 opções diferentes)
objetivo_vaga (5 opções diferentes)
prioridade_vaga (definir vazios como "Média")
origem_vaga (definir vazios como "Nova posição")
estado
cidade
nivel profissional (14 opções diferentes, validar todas manualmente) OBS: Único campo com espaço no nome da coluna, tratar para colocar "_": `nivel_profissional`
nivel_academico (16 opções diferentes, validar todas manualmente)
nivel_ingles (6 opções diferentes, validar todas manualmente)
nivel_espanhol (6 opções diferentes, validar todas manualmente)
areas_atuacao (73 opções diferentes, remover "-" e " ")
viagens_requeridas (metade dos registros estão vazios, tratar vazios como não)
equipamentos_necessarios (6 opções diferentes, validar manualmente)

#### Tratativa especial

vaga_especifica_para_pcd (utilizar para filtros porém desconsiderar no modelo)
principais_atividades (campo de texto aberto, 83% distintos)
competencia_tecnicas_e_comportamentais (campo de texto aberto, 82% distintos)
demais_observacoes (campo texto aberto)
habilidades_comportamentais_necessarias (utilização no modelo para match de softskills)


#### Entender melhor

local_trabalho (entender coluna, dois valores numericos aparentemente aleatorios)
valor_venda (entender coluna, talvez seja para definição modelo de trabalho)
valor_compra_1
valor_compra_2
data_inicial
data_final