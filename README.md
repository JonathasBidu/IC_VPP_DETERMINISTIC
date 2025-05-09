# Otimização de Despacho de Recursos Energéticos Distribuídos (REDs)

Este repositório faz parte do meu projeto de Iniciação Científica na Universidade Federal Fluminense (UFF), dentro do curso de Engenharia Elétrica. O objetivo da pesquisa é desenvolver métodos para agregar Recursos Energéticos Distribuídos (REDs) e coordenar seus despachos de forma otimizada, permitindo que operem como se fossem uma única usina virtual (Virtual Power Plant - VPP).

## 🔍 Descrição do Projeto

Este foi o **primeiro trabalho desenvolvido na linha de pesquisa**, e serviu como base para as abordagens mais avançadas que foram implementadas posteriormente, como a abordagem estocástica de dois níveis e a reformulação MILP (Mixed Integer Linear Programming).

A formulação aqui proposta é **determinística**, ou seja, assume que todas as variáveis (geração solar e eólica, demanda e preço da energia) são conhecidas com precisão. Portanto, **o modelo não leva em consideração as incertezas** associadas à variabilidade dessas fontes e preços.

A vantagem dessa abordagem é a menor complexidade computacional e a clareza conceitual, servindo como ponto de partida para a modelagem e desenvolvimento de ferramentas de despacho energético em ambientes com REDs.

## 🔗 Trabalhos Relacionados

- [ ] (https://github.com/JonathasBidu/IC_VPP_MILP)
- [ ] (https://github.com/JonathasBidu/IC_VPP_ESTOCASTIC)

## ⚙️ Principais Funcionalidades

- Modelagem determinística da operação de uma Virtual Power Plant (VPP).
- Despacho ótimo de REDs com base em programação matemática clássica.
- Geração e utilização de séries temporais de carga, geração e preços.
- Visualização gráfica dos resultados do despacho.

## 📁 Organização dos Arquivos

**1. Geração de Séries Temporais (`GENERATOR_SERIES/`):**  
Scripts responsáveis por gerar séries horárias de carga, geração solar, geração eólica e preço da energia. Utilizam dados históricos e técnicas de regressão ou interpolação.

**2. Base de Dados (`DATA_BASE/`):**  
Arquivos com os dados brutos de entrada, como séries de irradiância, temperatura e potência solar de diferentes cidades, histórico de preço horário (PLD) e dados de carga.

**3. Séries Geradas (`GENERATED_SERIES/`):**  
Séries horárias já processadas e prontas para uso na otimização (formato `.xlsx` ou `.csv`).

**4. Núcleo da Otimização (`VPP_DISPATCH_V1_APE/`):**  
Contém os scripts responsáveis por:
- Definir as restrições de igualdade e desigualdade;
- Implementar a função objetivo;
- Carregar os dados e executar o modelo de otimização;
- Aplicar o algoritmo genético (GA);
- Gerar gráficos e visualizar resultados.

## 🚀 Execução do Programa

1. Gere as séries temporais com os scripts da pasta `GENERATOR_SERIES/`.
2. Confirme os dados processados em `GENERATED_SERIES/`.
3. Execute o arquivo `script.py` na pasta `VPP_DISPATCH_V1_APE/`.
4. Os resultados do despacho ótimo serão apresentados graficamente e o lucro será exibido ao final.

## 🏆 Resultados Esperados

- Um plano de despacho ótimo da VPP para o período simulado.
- Maximização do lucro da operação da planta virtual.
- Atendimento de todas as restrições operacionais.
- Base conceitual e computacional para abordagens mais complexas.

## 🤝 Contribuição

Caso queira contribuir com este projeto, fique à vontade para abrir uma *issue* ou fazer um *pull request*! Sugestões para melhoria da modelagem, otimização ou visualização são muito bem-vindas.

## 💡 Contato

Sinta-se à vontade para contribuir ou entrar em contato para discussões sobre otimização energética distribuída! 🚀⚡
