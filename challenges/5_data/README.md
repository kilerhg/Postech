# Challenge 5

![Project Design](./docs/project_design.png)


## Tratativa dados - Dataset Application

### Deletar Coluna


email_secundario (vazia)
cv_en: (vazia)
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
cpf (vazia)
skype (vazia)
url_linkedin (vazia)
facebook (vazia)
download_cv (extensão arquivo, irrelevante para nossa analize)

### Normalizar

fonte_indicacao (muitos registros com ":")
sexo (muitos registros vazios)
estado_civil (muitos registros vazios)
pcd (muitos registros vazios)

conhecimentos_tecnicos (criar lista de campos, separados por ';', ',' ou '|')
certificacoes (muitos registros vazios, separados por ';', ',' ou '|')
outras_certificacoes (muitos registros vazios, separados por ';', ',' ou '|')

nivel_academico (muitos registros vazios)
nivel_ingles (muitos registros vazios)
nivel_espanhol (muitos registros vazios)
outro_idioma (muitos registros com "-")

### Tratativa especial

data_nascimento (gerar idade, existem registros com "0000-00-00")
remuneracao (muitos registros vazios, variações entre padrões: "R$00,00, "1.000,00", "mensal / 1000", por hora e etc)
cv_pt (muitas variações, letras separadas por espaço, quebras de texto sem padrão, "em anexo" e vazios também estão presentes)
