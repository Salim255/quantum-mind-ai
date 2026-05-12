# 🧠 Dev Diary — Setting Up a Python Virtual Environment (venv)

## 📌 Why do we need a virtual environment?

When working with Python projects (like a FastAPI API), you’ll install packages such as:

- `fastapi`
- `uvicorn`
- `pydantic`
- etc.

If you install them **globally**, you can run into problems:

- ❌ Version conflicts between projects
- ❌ Breaking other apps
- ❌ Hard-to-reproduce environments

👉 A **virtual environment (`venv`)** solves this by isolating dependencies **per project**.

---

## ⚙️ Step 1 — Create a virtual environment

```bash
python3 -m venv venv
```

### 🔍 What this does:

- Creates a folder named `venv/`
- Inside it:
  - A local Python interpreter
  - A separate `site-packages` (where dependencies go)

👉 Think of it as a **mini Python installation just for your project**

---

## 🚀 Step 2 — Activate the environment

### On macOS / Linux:

```bash
source venv/bin/activate
```

### On Windows:

```bash
venv\Scripts\activate
```

### ✅ After activation:

Your terminal will show something like:

```bash
(venv) user@machine project-folder %
```

👉 This means:

- All `pip install` commands now install **inside this project only**

---

## 📦 Step 3 — Install dependencies

```bash
pip install fastapi uvicorn
```

- FastAPI → the web framework

- Uvicorn → the server that runs FastAPI

👉 These are now installed **only inside `venv/`**, not globally.

---

## 🧾 Step 4 — Save dependencies

```bash
pip freeze > requirements.txt
```

👉 This creates a file listing all installed packages.

Example:

```
fastapi==0.115.0
uvicorn==0.30.0
```

---

## 🔁 Step 5 — Recreate environment (on another machine)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

👉 Now the project runs exactly the same anywhere.

---

## 🧹 Step 6 — Deactivate when done

```bash
deactivate
```

---

## 🧠 Key Concept (Important)

| Without venv ❌     | With venv ✅          |
| ------------------- | --------------------- |
| Shared dependencies | Isolated dependencies |
| Risk of conflicts   | Safe per project      |
| Hard to reproduce   | Fully reproducible    |

---

## 💡 Mental Model

Think of `venv` like:

> 🧪 A sandbox where your project lives independently from the rest of your system

---

## 🧰 Bonus — FastAPI run example

```bash
uvicorn main:app --reload
```

---

## ✅ TL;DR

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn
pip freeze > requirements.txt
```

---

## 🚨 Best Practice

- Always create a `venv` per project
- Never commit the `venv/` folder
- Add this to `.gitignore`:

```
venv/
```

---

## 🎯 Final Thought

Using `venv` is not optional in professional projects —
it’s the foundation for **clean, reproducible, and maintainable Python apps**.

## DB
