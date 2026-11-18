# Documento Técnico Coletivo do Jogo

- **Jogo** — Riff Run
- **Versão documentada** — versão desktop com campanha completa e código organizado em pacotes
- **Repositório** — https://github.com/nelicearaujo/riffrun
- **Commit-base histórico** — `6975e69`, “Adiciona jogo Riff Run com mapa dark e fases progressivas”

> Este documento descreve o que foi localizado no código-fonte e validado no ambiente disponível. Informações que não aparecem no repositório, como integrantes, divisão de tarefas, cronograma oficial de sprints e vídeo de demonstração, estão identificadas como pendentes de preenchimento pela equipe.

## 1. Identificação do projeto

### 1.1 Caracterização

| Item | Descrição | Situação |
|---|---|---|
| Nome | Riff Run | Implementado |
| Gênero | Plataforma 2D com ação, exploração lateral e coleta de itens | Implementado |
| Motor/biblioteca | pygame-ce 2.5.8, executado sobre SDL | Validado no ambiente |
| Linguagem | Python 3.14.5 | Usado na validação local |
| Persistência | Arquivo local `progress.json` em formato JSON | Implementada |
| Resolução | 1280 × 720 pixels | Implementada |
| Taxa de atualização | 60 FPS | Configurada em `riffrun/settings.py` |
| Controle de versão | Git, repositório hospedado no GitHub | Identificado |

### 1.2 Integrantes e responsabilidades

O código e o histórico disponível não registram a composição completa da equipe nem a divisão individual das atividades. A tabela abaixo deve ser preenchida coletivamente antes da entrega, usando os nomes reais e as evidências correspondentes.

| Integrante | Responsabilidades realizadas | Componentes relacionados | Evidência |
|---|---|---|---|
| `[nome do integrante 1]` | `[descrever atividades efetivamente realizadas]` | `[arquivos, sistemas ou telas]` | `[commit, tarefa, branch ou outra evidência]` |
| `[nome do integrante 2]` | `[descrever atividades efetivamente realizadas]` | `[arquivos, sistemas ou telas]` | `[commit, tarefa, branch ou outra evidência]` |
| `[nome do integrante 3]` | `[descrever atividades efetivamente realizadas]` | `[arquivos, sistemas ou telas]` | `[commit, tarefa, branch ou outra evidência]` |
| `[nome do integrante 4, se houver]` | `[descrever atividades efetivamente realizadas]` | `[arquivos, sistemas ou telas]` | `[commit, tarefa, branch ou outra evidência]` |

O commit-base foi registrado no Git como autoria de `nelicearaujo`; esse dado é apenas metadado do repositório e não substitui o registro das contribuições individuais da equipe.

### 1.3 Cronograma de sprints

O cronograma fornecido pelo professor não está presente no repositório. Portanto, não é possível afirmar quais tarefas pertencem a cada sprint sem consultar o material oficial. A equipe deve substituir a tabela abaixo pelo cronograma real, mantendo a distinção entre concluído, parcial e pendente.

| Sprint oficial | Tarefas previstas | Entregas efetivamente realizadas | Pendências |
|---|---|---|---|
| `[Sprint 1]` | `[copiar do cronograma do professor]` | `[registrar o que foi entregue]` | `[registrar o que ficou pendente]` |
| `[Sprint 2]` | `[copiar do cronograma do professor]` | `[registrar o que foi entregue]` | `[registrar o que ficou pendente]` |
| `[Sprint 3]` | `[copiar do cronograma do professor]` | `[registrar o que foi entregue]` | `[registrar o que ficou pendente]` |
| `[outras sprints]` | `[copiar do cronograma do professor]` | `[registrar o que foi entregue]` | `[registrar o que ficou pendente]` |

## 2. Visão geral e regras do jogo

### 2.1 Objetivo

O jogador atravessa três fases laterais e recupera um instrumento em cada percurso. As fases passam por um palco industrial, um trajeto sobre lava com checkpoints e um cemitério com mortos-vivos. Após a terceira fase, a campanha segue para o duelo contra Gustavo. Na arena final, derrotar o chefe conclui o jogo.

### 2.2 Mecânicas implementadas

| Funcionalidade | Descrição | Situação |
|---|---|---|
| Movimentação | Movimento horizontal com velocidade constante, usando A/D ou setas esquerda/direita | Implementada |
| Pulo | Pulo condicionado ao personagem estar sobre uma plataforma, usando Espaço, W ou seta para cima | Implementado |
| Gravidade | Aplicação de aceleração vertical com limite de velocidade de queda | Implementada |
| Colisão com plataformas | Ajuste separado de colisões horizontais e verticais | Implementada |
| Câmera lateral | Câmera acompanha o personagem e é limitada à largura do nível | Implementada |
| Buracos | Trechos sem chão fazem o personagem cair; a queda causa dano e reposiciona o personagem | Implementada |
| Coleta | Mini guitarras desaparecem ao serem tocadas e somam um ponto | Implementada |
| Pontuação | O HUD mostra a coleta de riffs em relação a 10. O resultado soma 1.000 pontos por riff e um bônus por tempo na vitória | Implementada |
| Inimigos | Os inimigos patrulham, investem, mergulham, disparam ou invocam outros inimigos conforme o tipo | Implementada |
| Ataque | Clique esquerdo cria uma área de ataque temporária na direção do personagem e causa dano aos inimigos atingidos | Implementado |
| Vida/energia | O personagem inicia com 3 unidades de energia e recebe invulnerabilidade temporária após dano | Implementada |
| Game Over | Ao chegar a zero de energia, a tela de derrota é exibida | Implementado |
| Vitória | Alcançar o instrumento conclui a fase lateral. Derrotar Gustavo conclui a arena final | Implementada |
| Repetição | Tecla R reinicia a fase após vitória ou derrota | Implementada |
| Mapa de campanha | Seleção por teclado, mouse ou teclas 1, 2 e 3 | Implementada |
| Desbloqueio | Concluir uma fase libera a próxima e grava o progresso localmente | Implementado |
| Áudio | Trilhas em OGG, efeitos em WAV e controle pela tecla V | Implementado |
| Checkpoints | As plataformas de descanso da fase 2 registram o ponto de retorno após contato com a lava | Implementado na fase 2 |
| Seleção de personagem | Não foi encontrada tela ou sistema de seleção | Não implementado |

### 2.3 Entradas do jogador

| Entrada | Ação |
|---|---|
| A ou seta esquerda | Mover para a esquerda |
| D ou seta direita | Mover para a direita |
| Espaço, W ou seta para cima | Pular quando estiver no chão |
| Clique esquerdo durante a fase | Atacar |
| Setas, A/D ou W/S no mapa | Alterar fase selecionada |
| Enter ou Espaço no mapa | Iniciar a fase selecionada, se desbloqueada |
| Teclas 1, 2 e 3 no mapa | Selecionar e iniciar diretamente uma fase desbloqueada |
| Esc | Voltar à tela anterior ou sair pelo menu inicial |
| R | Reiniciar após vitória ou Game Over |
| M após vitória | Voltar ao mapa |
| Enter após vitória | Avançar ou voltar ao mapa após o chefe |
| V | Alternar o áudio |

### 2.4 Regras e resultados observáveis

1. O personagem começa com 3 unidades de energia.
2. O contato com um inimigo reduz uma unidade, desde que a invulnerabilidade não esteja ativa.
3. Após receber dano, o personagem fica invulnerável por 80 frames e recebe impulso vertical para cima.
4. Cair abaixo da tela reposiciona o personagem em `(120, 500)`. Na fase 2, tocar na lava retorna ao checkpoint. A perda de vida respeita a invulnerabilidade.
5. O ataque só pode ser iniciado quando o contador de ataque está zerado; a área de dano fica ativa durante uma janela intermediária da animação.
6. Cada mini guitarra coletada soma 1 ponto e não reaparece durante a execução atual da fase.
7. A coleta de guitarras é opcional para concluir as fases.
8. Concluir as duas primeiras fases libera o próximo nó no mapa. Concluir a terceira permite avançar ao duelo final.
9. O encerramento pelo evento de janela termina o laço principal e chama `pygame.quit()`.

## 3. Arquitetura e organização do código

### 3.1 Arquivos e módulos

| Caminho | Responsabilidade |
|---|---|
| `main.py` | Inicializar o Pygame, abrir a tela cheia e executar o jogo |
| `riffrun/game.py` | Coordenar o loop, entrada, coleta, combate e transições |
| `riffrun/entities/` | Jogador, inimigos, indicadores de vida e animações de derrota |
| `riffrun/stages/` | Campanha, arena final, plataformas, perigos e objetivos |
| `riffrun/ui/` | Menus, fundos, HUD e telas de resultado |
| `riffrun/audio.py` | Trilhas, efeitos e controle de volume |
| `riffrun/scoring.py` e `riffrun/progress.py` | Pontuação e persistência dos desbloqueios |
| `riffrun/settings.py` e `riffrun/paths.py` | Constantes e localização dos recursos |
| `assets/` e `tests/` | Recursos audiovisuais e testes automatizados |

### 3.2 Interação entre os componentes

`Game` recebe a superfície criada em `main.py` e coordena o jogador, a fase ou arena, o áudio e a interface. A atualização fornece as plataformas ao jogador, avança os inimigos e resolve coleta, acertos e dano. Em seguida, `GameView` desenha o cenário, as entidades, o HUD e o resultado.

### 3.3 Estados principais

`Game.screen_mode` representa o menu inicial, as opções, os créditos, o mapa ou a partida. `Game.start_phase()` cria um jogador e um percurso ou arena, reinicia o resultado da tentativa e limpa o registro de inimigos atingidos. Durante a partida, os indicadores de vitória e derrota determinam a atualização e o desenho da tela de resultado.

## 4. Linguagem, bibliotecas e ambiente

Python é uma linguagem de alto nível, interpretada, de tipagem dinâmica e com suporte a orientação a objetos. No projeto, ela organiza o jogo em módulos e classes, facilitando a separação entre o laço principal, o personagem, os objetos e a construção dos níveis.

O jogo utiliza:

- **pygame-ce 2.5.8** — janela, eventos, teclado, mouse, relógio, superfícies, imagens, retângulos de colisão, desenho 2D e sprites.
- **SDL, por meio do Pygame:** camada de janela e entrada utilizada pelo motor.
- **`pathlib`:** construção de caminhos portáveis para os assets e para `progress.json`.
- **`json`:** serialização e leitura do progresso local.
- **`os`** — leitura da variável opcional de captura de tela.
- **Git/GitHub:** versionamento e distribuição do código.

A validação local usa Python 3.14.5 e pygame-ce 2.5.8. O README documenta a instalação por meio de `requirements.txt`.

## 5. Persistência de dados

### 5.1 Informação armazenada

O arquivo `progress.json` armazena o campo `unlocked_phases`, que indica quantas fases estão desbloqueadas. No estado observado do projeto, o arquivo contém:

```json
{
  "unlocked_phases": 3
}
```

O valor é limitado entre 1 e 3 ao ser carregado. Quando uma fase é concluída, o jogo grava o maior valor entre o progresso atual e a próxima fase liberada.

### 5.2 Justificativa técnica

A persistência local é necessária para que o desbloqueio das fases permaneça entre execuções, sem exigir banco de dados, servidor ou conta de usuário. JSON é suficiente para esse único número e mantém a implementação simples, legível e compatível com um protótipo desktop.

Pontuação, vida, estado dos inimigos e guitarras coletadas não são persistidos: eles pertencem à execução atual e são reiniciados ao iniciar ou repetir uma fase.

### 5.3 Limitações observadas

Se `progress.json` estiver ausente ou inválido, o jogo abre com apenas a fase 1 desbloqueada. O progresso fica no arquivo local da instalação.

## 6. Fluxo de execução

1. `main.py` inicializa o Pygame, abre a janela em tela cheia e instancia `Game`.
2. `Game` prepara os recursos de desenho e áudio e carrega os desbloqueios.
3. O menu inicial permite abrir o mapa, consultar opções e créditos ou sair.
4. Ao iniciar uma fase desbloqueada, o jogo atualiza jogador, cenário e inimigos a cada quadro e desenha a partida.
5. A vitória atualiza os desbloqueios da campanha. A derrota exibe o resultado e permite reiniciar pela tecla R.
6. O encerramento libera o Pygame com `pygame.quit()`.

## 7. Testes e qualidade

### 7.1 Validação automatizada

A suíte `unittest` reside em `tests/`. Os **69 testes** cobrem construção das fases, entidades e animações, obstáculos e checkpoints, combate e áudio do chefe, HUD, pontuação e nota por estrelas. O comando para cada sistema está no README.

A inicialização desktop também foi verificada em modo headless, com captura da tela inicial em 1280 × 720.

### 7.2 Validação manual pendente

Uma partida completa em ambiente interativo pode confirmar a sensação dos controles, a mixagem com a trilha, a apresentação em tela cheia e a persistência ao fechar e reabrir o jogo.

## 8. Contribuições individuais e integração

### 8.1 Componentes integrados

A camada de execução em `riffrun/game.py` integra as entidades, os três percursos, a arena final, os menus, a pontuação, o áudio e a persistência local. Os arquivos de imagem e som ficam em `assets/`.

### 8.2 Registro individual

Não é tecnicamente seguro atribuir cada componente a uma pessoa somente a partir do código atual. Para atender à exigência de contribuição individual, a equipe deve completar esta tabela com base no histórico do Git, nas tarefas do professor e no relato de cada integrante.

| Integrante | Atividade específica | Decisão técnica ou resultado | Evidência para anexar |
|---|---|---|---|
| `[nome]` | `[ex.: implementação do movimento e colisão]` | `[descrever decisão efetivamente tomada]` | `[commit/arquivo/tarefa]` |
| `[nome]` | `[ex.: criação dos objetos e obstáculos]` | `[descrever decisão efetivamente tomada]` | `[commit/arquivo/tarefa]` |
| `[nome]` | `[ex.: menu, mapa e persistência]` | `[descrever decisão efetivamente tomada]` | `[commit/arquivo/tarefa]` |
| `[nome]` | `[ex.: arte, testes ou integração]` | `[descrever decisão efetivamente tomada]` | `[commit/arquivo/tarefa]` |

### 8.3 Integração

A integração ocorre no loop de `Game`. O jogador e os inimigos usam retângulos `pygame.Rect` nas colisões, e os perigos com sprites também usam máscaras. `GameView` desenha os resultados da tentativa.

## 9. Entregas, evidências e pendências

### 9.1 Situação das funcionalidades

| Item | Estado atual | Evidência |
|---|---|---|
| Plataforma 2D jogável | Implementada | `main.py`, `riffrun/game.py` |
| Fases 1, 2 e 3 com percursos próprios | Implementadas | `riffrun/stages/level.py` |
| Duelo final contra Gustavo | Implementado | `riffrun/stages/boss.py` |
| Mapa e desbloqueios persistentes | Implementados | `riffrun/ui/game_view.py`, `riffrun/progress.py` |
| Música e efeitos sonoros | Implementados | `riffrun/audio.py`, `assets/sounds/` |
| Checkpoints na fase 2 | Implementados | `Level.handle_hazards()` |
| Validação automatizada | 69 testes aprovados | `tests/` |

### 9.2 Links e materiais

- **Repositório:** https://github.com/nelicearaujo/riffrun
- **Vídeo de demonstração:** `[inserir link real; não localizado no repositório]`
- **Cronograma de sprints:** `[inserir link ou referência ao arquivo fornecido pelo professor]`
- **Versão entregue:** `[inserir tag, commit ou data da versão final efetivamente submetida]`

As imagens existentes no projeto são evidências de recursos visuais implementados. A captura de inicialização realizada durante a validação deve ser anexada somente se a equipe desejar utilizá-la como evidência adicional e se ela for disponibilizada junto da entrega.

## 10. Utilização de inteligência artificial

### 10.1 Declaração referente a este documento

Foi utilizada assistência de inteligência artificial para inspecionar a organização do repositório, sintetizar o funcionamento observável do código, estruturar este documento e apoiar a validação de compilação e inicialização. A IA não substitui a revisão da equipe: os integrantes devem conferir cada descrição no código, executar os testes interativos pendentes e corrigir qualquer informação que não corresponda ao trabalho efetivamente realizado.

### 10.2 Revisão humana e validações

Os resultados documentados foram confrontados com os arquivos do projeto, o estado do Git e uma execução headless do jogo. A equipe deve acrescentar, antes da submissão, a declaração sobre qualquer uso anterior de IA na criação, implementação, arte, testes ou depuração do jogo, indicando:

- qual ferramenta foi utilizada;
- em qual etapa foi utilizada;
- quais sugestões foram aceitas, adaptadas ou rejeitadas;
- quais testes e revisões humanas confirmaram o funcionamento;
- quais partes foram produzidas integralmente pela equipe.

Não devem ser atribuídas à IA funcionalidades que não estejam presentes no código nem testes que não tenham sido executados.

## 11. Conclusão do estado atual

Riff Run reúne três fases com percursos próprios, um duelo final, pontuação, áudio, desbloqueio local e uma suíte de testes. A versão documentada é desktop. A equipe ainda precisa preencher integrantes, responsabilidades, cronograma e links da entrega acadêmica.
