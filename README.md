# Riff Run

Jogo desktop de plataforma 2D em pixel art, com temática de rock e heavy metal. Atravesse três fases, colete mini guitarras, recupere os instrumentos e enfrente Gustavo na arena final.

## Instalação e execução

Na raiz do repositório, crie um ambiente virtual e instale o pygame-ce a partir de `requirements.txt`.

**Windows (PowerShell)**

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

**macOS e Linux**

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

O jogo abre em tela cheia com resolução interna de 1280 × 720.

## Versão web

O Pygbag empacota o jogo para o navegador. O build compacta os fundos e as músicas e converte os efeitos sonoros de WAV para OGG em uma cópia dos assets. O menu abre assim que o jogo termina de carregar. O primeiro toque, clique ou comando de teclado permite que o navegador libere o áudio. No computador, jogue com teclado e mouse e use **F** para alternar a tela cheia. No celular, os botões **◀**, **▶**, **Pular** e **Atacar** ficam sobre o jogo. Você pode segurar uma direção enquanto pula ou ataca com outro dedo. Toque em **⛶** para alternar a tela cheia ou gire o celular para aproveitar a tela na horizontal. Os desbloqueios são gravados no navegador.

### Testar no próprio computador

Com o ambiente virtual ativado na raiz do repositório, execute:

```bash
python -m pip install -r requirements-web.txt
python scripts/build_web.py
python -m http.server 8000 --bind 127.0.0.1 --directory build/web
```

Abra [http://127.0.0.1:8000](http://127.0.0.1:8000). A primeira abertura precisa de internet para carregar o runtime do Pygbag.

### Publicar no GitHub Pages

1. No repositório do GitHub, abra **Settings → Pages** e, em **Build and deployment → Source**, selecione **GitHub Actions**.
2. Faça push das alterações para a branch `main`. O workflow **Riff Run no GitHub Pages** roda os testes, gera `build/web` e publica o pacote.
3. Abra a aba **Actions** para acompanhar o primeiro deploy. Quando concluir, o endereço esperado é [nelicearaujo.github.io/riffrun](https://nelicearaujo.github.io/riffrun/). O link oficial também aparece em **Settings → Pages**.

## Campanha e controles

1. Palco industrial com aranhas, nuvens e o Robô Roadie.
2. Percurso sobre lava com espinhos, jatos de fogo e checkpoints.
3. Cemitério com zumbis, morcegos ósseos e necromantes.
4. Duelo final contra Gustavo.

| Entrada | Ação |
| --- | --- |
| A/D ou setas esquerda/direita | Mover |
| Espaço, W ou seta para cima | Pular |
| Clique esquerdo | Atacar ou selecionar nos menus |
| Setas, A/D ou W/S no mapa | Alternar fase selecionada |
| Enter ou Espaço no mapa | Iniciar fase selecionada |
| 1, 2 ou 3 no mapa | Iniciar fase desbloqueada |
| V | Silenciar ou reativar o áudio |
| Esc | Voltar ou sair a partir do menu inicial |
| R após vitória ou derrota | Reiniciar a fase |
| Enter após vitória | Avançar ou voltar ao mapa depois do chefe |
| M após vitória | Voltar ao mapa |

Cada tentativa começa com três pontos de vida. A pontuação das fases laterais combina as mini guitarras coletadas e o bônus de tempo. O jogo salva os desbloqueios em `progress.json`.

### Nota da tentativa

A tela de resultado mostra até três estrelas junto da pontuação.

| Estrelas | Fases da campanha | Duelo final |
| --- | --- | --- |
| ★ | Concluir a fase | Derrotar Gustavo |
| ★★ | Fazer pelo menos 6.000 pontos | Vencer em até 2 min |
| ★★★ | Fazer pelo menos 10.000 pontos | Vencer em até 1 min |

Uma derrota vale zero estrelas. O tempo do duelo começa após a introdução do chefe.

## Estrutura

```text
main.py              Entrada desktop
riffrun/
  game.py            Loop, eventos, combate e transições
  settings.py        Constantes do jogo
  paths.py           Caminhos dos recursos e dados locais
  audio.py           Trilhas e efeitos sonoros
  scoring.py         Pontuação e tempo de tentativa
  progress.py        Leitura e gravação dos desbloqueios
  entities/         Jogador, inimigos e efeitos visuais de combate
  stages/           Fases, arena final, plataformas, colecionáveis e perigos
  ui/               Menus, HUD e telas de resultado
assets/             Imagens, trilhas e efeitos sonoros
tests/              Suíte automatizada
```

O [documento técnico coletivo](DOCUMENTO_TECNICO_COLETIVO.md) descreve a implementação e a entrega acadêmica.

## Testes

A suíte usa `unittest` com os drivers `dummy` do SDL para simular vídeo e áudio. Na raiz do projeto, use o comando do seu sistema.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

```bash
.venv/bin/python -m unittest discover -s tests -v
```
