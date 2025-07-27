# **openrouter-commit 🚀 AI-Powered Git Commit Messages**  

**Generate smart, AI-driven Git commit messages** using OpenRouter models like **DeepSeek R1**. Automate your commit workflow and write meaningful commits effortlessly.

---

## **⚡ Quick Start**  

### **Run without installation**
```sh
npx openrouter-commit -run
```

### **Install globally**
```sh
npm install -g openrouter-commit
openrouter-commit -run
```

### **Use in a project (`package.json`)**
```json
{
    "scripts": {
        "commit": "npx openrouter-commit -run"
    }
}
```
Run it with:
```sh
npm run commit  # or yarn commit
```

---

## **🔄 Updating**
- **Global (del)**: `sudo npm uninstall -g openrouter-commit`
- **Global:** `sudo npm update -g openrouter-commit`  
- **npx users:** `npx clear-npx-cache`  
- **Project-based:** `npm update openrouter-commit`  

---

## **⚙️ Setup**
### **API Key & Model**
#### **Option 1: `.env.openrouter` file (recommended)**
```sh
OPENROUTER_API_KEY=your-api-key
OPENROUTER_MODEL=deepseek/deepseek-r1
```
#### **Option 2: Environment variables**
```sh
export OPENROUTER_API_KEY=your-api-key
export OPENROUTER_MODEL=deepseek/deepseek-r1
```
#### **Option 3: Custom `.env` path**
```sh
npx openrouter-commit -run --env-path /custom/path/.env
```

---

## **🚀 How It Works**
1️⃣ **Checks Git status**  
2️⃣ **Prompts to stage changes**  
3️⃣ **Generates an AI-powered commit message**  
4️⃣ **Lets you confirm or edit it**  
5️⃣ **Commits and pushes automatically**  

---

## **📂 Ignored Files**
By default, `openrouter-commit` **ignores common files** that shouldn't be in commits:

- `.env.openrouter`
- `node_modules/`, `.npm/`, `package-lock.json`
- `dist/`, `venv/`, `env/`, `__pycache__/`, `*.pyc`, `*.pyo`, `Pipfile.lock`, `poetry.lock`
- `logs/`, `*.log`, `debug.log*`, `*.swp`, `*.swo`
- `.cache/`, `.idea/`, `.editorconfig`
- `.DS_Store`, `Thumbs.db`

If needed, modify the `IGNORED_FILES` list in `openrouter-commit`'s source code.

---

## **🔥 Features**
✅ **AI-powered commit messages**  
✅ **Interactive CLI with confirmation prompts**  
✅ **Custom `.env` paths with `--env-path`**  
✅ **Handles large diffs intelligently**  
✅ **Failsafe exit handling (Ctrl+C won’t commit unfinished work)**  
✅ **Prevents accidental execution with `-run` flag**  
✅ **Ignores unnecessary files from commits**  

---

## **❓ Troubleshooting**
### **Not enough OpenRouter credits?**
🔗 [Top up here](https://openrouter.ai/credits)

### **Command not found?**
```sh
npx openrouter-commit -run
```
Or:
```sh
npm install -g openrouter-commit
openrouter-commit -run
```

### **Git push fails?**
Ensure your branch is tracking a remote branch:
```sh
git branch --set-upstream-to=origin/main
```

---

## **💡 About**
Built by [Unrealos.com](https://unrealos.com) – AI, SaaS, and PaaS solutions.

## **📜 License**
MIT © **Unrealos.com** 🚀
