
# Tutorial Completo de Colaboração em Repositório Público

Este tutorial ensina passo a passo como colaborar em um repositório público usando **forks, branches e pull requests** no GitHub.

----------

## 1️⃣ Criar o Fork

1.  Acesse o repositório público no GitHub que deseja contribuir.
    
2.  Clique em **Fork** no canto superior direito.
    
3.  Agora você tem uma cópia do repositório em sua própria conta.
    

----------

## 2️⃣ Clonar o Fork para sua máquina

```bash
git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
cd NOME_DO_REPOSITORIO

```

----------

## 3️⃣ Configurar o repositório original como remoto (`upstream`)

```bash
git remote add upstream https://github.com/USUARIO_ORIGINAL/NOME_DO_REPOSITORIO.git
git fetch upstream

```

-   `origin` → seu fork
    
-   `upstream` → repositório original
    

----------

## 4️⃣ Atualizar a main do seu fork com o repositório original

```bash
git checkout main
git fetch upstream
git merge upstream/main
git push origin main

```

----------

## 5️⃣ Criar uma nova branch para trabalhar

```bash
git checkout -b feature/minha-alteracao

```

-   Faça suas alterações no código.
    
-   Adicione e faça commit das alterações:
    

```bash
git add .
git commit -m "Descrição clara do que foi feito"

```

----------

## 6️⃣ Enviar a branch para seu fork

```bash
git push origin feature/minha-alteracao

```

----------

## 7️⃣ Atualizar sua branch de feature com a main (opcional)

```bash
git checkout main
git pull origin main
git checkout feature/minha-alteracao
git merge main

```

-   Resolva conflitos se houver.
    

----------

## 8️⃣ Merge da branch de feature na main do seu fork

```bash
git checkout main
git merge feature/minha-alteracao
git push origin main

```

-   Sua main local e remota agora contém suas alterações.
    

----------

## 9️⃣ Abrir Pull Request para o repositório original

1.  No GitHub, vá até seu fork.
    
2.  Clique em **Compare & pull request**.
    
3.  Configure:
    
    -   **Base**: branch `main` do repositório original
        
    -   **Comparação**: sua branch de feature ou main do fork
        
4.  Adicione descrição das alterações, vincule issues se houver e envie o PR.
    

----------

## ✅ Resumo Visual do Fluxo

```
Repositório Original (upstream/main)
           ↑
        Pull Request
           ↑
      Seu Fork (origin/main)
           ↑
   Sua Branch de Funcionalidade → merge → main do fork

```

Seguindo este fluxo, você garante:

-   Que não altera diretamente o repositório original.
    
-   Que seu fork está sempre atualizado.
    
-   Que a colaboração via pull request seja organizada e segura.