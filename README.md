# Intranet

Sistema para apresentação Django/Python com gerenciamento de usuários, e arquivos.

#### Tecnologias utilizadas
* Django 2.0.6
* Python 3.6
* Materialize 1.0

#### O que é necessário para executar o projeto:
* Crie um superusuário Django
* Entre com o usuário em /admin e crie um perfil de usuário e associe ao super
usuario criado anteriormente
* Acesse a raiz da aplicação e todas as ações estarão disponíveis

#### O que poderia ser melhor neste projeto:
A Organização de apps não está perfeita. Poderia ser criado um app somente para a
gestão de arquivos e outro para o perfil do usuário. Este formato (com duas aplicações)
foi o primeiro adotado, porém, percebeu-se que todas as ações relacionadas aos arquivos
tinha origem no perfil de usuário. Com isso foi utilizada somente uma aplicação

#### URLs importantes:
* https://intranetlgsilva.herokuapp.com
* https://intranetlgsilva.herokuapp.com/admin
* https://intranetlgsilva.herokuapp.com/api/utilizacao/